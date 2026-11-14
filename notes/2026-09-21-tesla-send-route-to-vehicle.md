# Tesla: Sending a Planned Route to the Vehicle

- **Date researched:** 2026-09-21
- **Question:** Can charge-line push a planned multi-stop EV trip — including third-party (non-Supercharger) charging stops — into the user's own Tesla so it appears in the car's native navigation?
- **Status:** Yes in principle, no off-the-shelf today. Tesla's in-car nav supports multi-stop routes and Tesla's Fleet API documents a `navigation_waypoints_request` endpoint that sends an ordered list of stops. But that endpoint is **only reachable as a signed Tesla Vehicle Command Protocol (TVCP) message**, and Tesla's own signing SDK/proxy (`teslamotors/vehicle-command`) has never implemented it — so the documented endpoint is non-functional through the official toolchain and has been broken since at least Dec 2024. There is an open community PR against Tesla's repo (#443) that implements it, which a Tesla maintainer has reviewed and corrected against Tesla's *internal* proto definition, and which the author verified end-to-end on a real Model 3. The buildable path today is to vendor that proto message into your own signing proxy. Everything else (partner registration, virtual-key pairing, pay-per-use billing) is a hard gate that applies regardless.
- **Field-tested:** 2026-10-09 and 2026-10-13, on a real car. The results are below and override the desk research wherever they disagree.

---

## Field results: what we confirmed on a real car

**Setup.** The owner's own Model Y on firmware 2026.28.5, in Australia, using the Fleet API's North America/Asia-Pacific region. Commands came from [`poc/tesla-send-route`](../../poc/tesla-send-route/), which signs them in TypeScript and posts straight to the Fleet API. Neither Tesla's Go SDK nor `tesla-http-proxy` was used. Results were read off photos of the car's screen.

**Answer to the question: yes.** One signed `navigation_waypoints_request` (VehicleAction tag 90) put a whole multi-stop route into the car's own navigation. The stops were Evie Wangaratta, Gundagai Supercharger, Chargefox Goulburn and Bennelong Point (Sydney), and two of them are third-party chargers. Navigation started on its own, and every stop appeared in order with its real name and street address.

| What we tested | Result | What the car did |
| --- | --- | --- |
| Personal developer app and partner registration on a free `github.io` domain | ✅ | The app was Active immediately, and registration succeeded |
| Virtual-key pairing (`tesla.com/_ak/<domain>` link opened on the phone) | ✅ | Approved in the Tesla app, after which `fleet_status` reported the key as paired |
| Signed commands from our own TypeScript code | ✅ | A no-op `Vehicle.Ping` returned OK. The anti-replay counter carried over correctly between sessions |
| `navigation_request`, unsigned, on a car that requires signed commands | ✅ | Navigated to the address. Trip Planner then added Superchargers by itself |
| `navigation_gps_request` (tag 53), one REPLACE then APPENDs | ❌ | Accepted, but showed only a pin ("Unknown Location") at the **last** stop, and navigation didn't start |
| `navigation_waypoints_request` (tag 90), 4 Google place IDs | ✅ | The whole route appeared, named and in order, and navigation started by itself |
| A Supercharger sent as a waypoint | ✅ | Became a charging stop with a planned charge time |
| A third-party charger sent as a waypoint | ⚠️ | Treated as an **ordinary stop**: no charging planned there. Trip Planner then added a Supercharger after each one (Albury or Wangaratta after Evie, Exeter after Chargefox) |
| `trip_plan_options.destination_arrival_soe = 28` | ✅ while Trip Planner is on | Showed 28% arrival and planned charging to meet it. With Trip Planner off, or after the Remove tap, arrival fell to 10% |
| `trip_plan_options.destination_start_soe = 90` | ❓ | No visible effect. The car used its real charge |
| Driver taps "Remove all charging stops" | ✅ workaround | Removed only the car's added Superchargers and kept every stop we sent, and nothing was re-added. The car then shows a red "Charging needed to reach destination" warning (−24% at Gundagai), because it still assumes no charging at Evie |
| Car's Trip Planner setting off (Controls → Navigation) | ✅ workaround, but affects every trip | Same result as the tap, with the same warning. No command in the protocol can change this setting |

**What this changes in the recommendation** (the sections below are annotated where they're affected):

1. **Fallback order: waypoints, then `navigation_request`, then the share sheet.** Drop the GPS chain (tier 2). It does less than `navigation_request`, which at least starts navigation and plans charging.
2. **No proxy is needed.** Signing inside our own code works on a real car, so forking `tesla-http-proxy` is optional.
3. **Tell the driver what the car will do.** After sending, the app should say something like: *"On the car screen, tap Remove all charging stops. Your Tesla will warn that charging is needed. That's expected, because it doesn't know you'll charge at Evie and Chargefox."*
4. **Don't count on `destination_arrival_soe`** once the driver has removed charging stops. It only applies while Trip Planner is planning.
5. **A command being accepted doesn't mean the route appeared.** The GPS chain was accepted and still failed. Anything that reports "sent to car" should rely on confirmation from the car, such as Fleet Telemetry `RouteLine` / `DestinationName`.

**Still unverified:**
- Whether the warning clears and the route continues normally after actually charging at a third-party stop on a real drive.
- Unsigned `navigation_request` before the key is paired.
- Waypoint string tokens other than `refId:`.
- Tag 90 on other firmware versions or models.
- Whether PR #443 gets merged upstream.

**Cost of the whole field test:** three wakes plus about a dozen commands and status checks, a few cents in total and well within Tesla's $10 monthly credit.

---

## Bottom line up front

1. **Multi-waypoint IS in Tesla's API surface.** `POST /api/1/vehicles/{vin}/command/navigation_waypoints_request` — "Sends a list of waypoints to the vehicle's navigation system" ([Tesla Fleet API → Vehicle Commands](https://developer.tesla.com/docs/fleet-api/endpoints/vehicle-commands)). It is *not* single-destination-only. The payload is a single string field: `{"waypoints": "refId:<placeId>,refId:<placeId>,..."}`, last entry = final destination ([vehicle-command PR #443](https://github.com/teslamotors/vehicle-command/pull/443)).

2. **But it does not work through any official path today.** Plain REST returns `"Tesla Vehicle Command Protocol required"`; Tesla's own signing proxy returns `invalid_command` because the command isn't in its switch statement ([issue #334](https://github.com/teslamotors/vehicle-command/issues/334), closed as dupe of the still-open [#188](https://github.com/teslamotors/vehicle-command/issues/188), last bumped 2025-09-14: *"Endpoints such as navigation_waypoints_request are documented clearly on the fleet api, yet are still non-functional."*). Verified against the current repo HEAD (`e35ef16`, 2026-08-30) — no navigation command exists in `pkg/vehicle/` or the proxy routing table.

3. **The gap is closeable by you, without Tesla.** The command is a plain `VehicleAction` oneof member at tag 90. You sign it with *your own* private key; Tesla's servers are only a transport. PR #443 adds a 10-line proto hunk + a 47-line Go file, and a Tesla maintainer (`sethterashima`) replied in review with the **exact internal message layout** — which is the strongest corroboration of the schema short of Tesla merging it. PR author reports a successful end-to-end test on a Model 3 running firmware 2026.14.1: three waypoints, full multi-leg route rendered in-dash in order.
   **Field-confirmed 2026-10-09 by our POC** (TypeScript signer, straight to Fleet API, firmware 2026.28.5). One signed tag-90 command with 4 place IDs (Evie Wangaratta, Gundagai Supercharger, Chargefox Goulburn, Bennelong Point) started navigation on its own. Every stop appeared in order, by name and street address.

4. **Third-party chargers: yes, with a caveat.** `navigation_waypoints_request` takes Google Maps place IDs (`refId:ChIJ...`), so any POI with a place ID works — including Chargefox/Evie sites. `navigation_gps_request` takes raw `lat`/`lon` (`double`), so arbitrary coordinates work too. Only `navigation_sc_request` is Supercharger-restricted (it takes a numeric Supercharger `id`). **Caveat:** Tesla's Trip Planner will insert *its own* Supercharger stops into your route if it thinks range is insufficient — observed in PR #443's test.
   **Field test 2026-10-09:** the car treats a third-party charger as a plain stop. It plans **no charging** there, so it inserted a Supercharger after each one (Albury after Evie, Exeter after Chargefox). A Supercharger sent as a waypoint *was* recognised as a charging stop, with a charge time. Getting the car to plan charging at third-party sites is the remaining problem.
   **Workaround, tested 2026-10-13:** the driver taps "Remove all charging stops" once. That leaves exactly the stops we sent, and Trip Planner doesn't re-add Superchargers. The car then shows a "Charging needed to reach destination" warning, because it still expects no charging at the third-party stops. Turning the car's Trip Planner setting off gives the same result without the tap, but it affects every trip, and the app can't change it.

5. **One navigation command does work over plain REST today: `navigation_request`.** Tesla's proxy explicitly refuses to sign it and forwards it to the Fleet API instead, with the comment *"Sharing options. These endpoints often require server-side processing, which prevents strict end-to-end authentication"* (`pkg/proxy/command.go:543-546`). It takes a free-text address string and is **single destination only** (`{"type":"share_ext_content_raw","value":{"android.intent.extra.TEXT":"<address>"},"locale":...,"timestamp_ms":...}`). This is the safe, boring fallback.

6. **The premise about `fleet-telemetry` is wrong** and worth correcting: [`teslamotors/fleet-telemetry`](https://github.com/teslamotors/fleet-telemetry) is a **server you host** that vehicles push telemetry *to* over mTLS WebSocket. It sends nothing to the car. It is read-only and complementary — useful to charge-line for `RouteLine`, `DestinationLocation`, `MinutesToArrival`, `ExpectedEnergyPercentAtTripArrival`, which let you detect leg completion and re-send the next stop.

7. **Gates are real and non-trivial for a consumer app:** partner account registration, a public domain hosting a P-256 public key at a fixed `.well-known` path, per-user virtual-key pairing in the car (the user has to tap through a Tesla-app deep link), OAuth with `vehicle_cmds`, pay-per-use billing ($1 per 1,000 commands, $10/mo credit), 30 commands/min/vehicle rate limit, and **no staging environment or simulator at all**.

8. **BLE is viable but only as a proximity feature.** Tesla publishes the full GATT profile and protocol; navigation commands terminate on the Infotainment domain and are ordinary signed `VehicleAction`s, so BLE carries them. Constraints: you must reimplement the protocol natively (Tesla's SDK is Go and explicitly doesn't run on Windows; there is no iOS/Android SDK), the car allows only ~3 concurrent BLE connections shared with keyfobs/phone keys, and it requires physical proximity.

9. **Incumbents confirm the practical ceiling.** ABRP's own release notes describe "Send to Tesla" as sending *charger details* (enough for preconditioning), i.e. a single charging stop, not the whole trip; ABRP's forum guidance is "send one leg at a time." PlugShare has no Tesla send-to-car at all — its in-vehicle story is CarPlay/Android Auto, which Teslas don't have.

10. **Watch CarPlay.** iOS 27 added `CPNavigationSession.isRouteSharingSupported` / `addRouteSegments(_:)` — a first-party API for a third-party nav app to hand its **full route geometry** to the vehicle's built-in systems. If Tesla ships CarPlay, this becomes a cleaner multi-stop path than the Fleet API. Tesla has not shipped it as of this writing.

---

## 1. What "send to car" mechanisms actually exist

Tesla's Fleet API documents exactly four navigation commands. All are `POST /api/1/vehicles/{vin}/command/<name>` ([Vehicle Commands](https://developer.tesla.com/docs/fleet-api/endpoints/vehicle-commands)):

| Command | Tesla's description (verbatim) | Payload | Transport |
|---|---|---|---|
| `navigation_request` | "Sends a location to the in-vehicle navigation system." | free text / address | **Unsigned REST** (Tesla's proxy forwards it) |
| `navigation_gps_request` | "Start navigation to given coordinates. Order can be used to specify order of multiple stops." | `lat`, `lon`, `order` | Signed TVCP |
| `navigation_sc_request` | "Start navigation to a supercharger." | `id`, `order` | Signed TVCP |
| `navigation_waypoints_request` | "Sends a list of waypoints to the vehicle's navigation system." | `waypoints` | Signed TVCP |

There is no `share` command in Fleet API (that was Owner API). There is no `get_active_route` in Fleet API either — that endpoint exists only in legacy Owner API wrappers ([TeslaPy `endpoints.json`](https://github.com/tdorssers/TeslaPy/blob/master/teslapy/endpoints.json), community). Route readback in Fleet API is `vehicle_data` or Fleet Telemetry.

**Tesla does not publish request bodies for any of these.** I verified this by rendering the docs page in a browser and expanding every disclosure control: the vehicle-commands page carries only heading + path + one-line description per command, with no parameter tables, no scope labels, and no "Pricing Category" blocks (unlike other endpoint pages). Tesla's own [Postman collection](https://www.postman.com/crimson-space-512892/workspace/fleet-api/collection/33220881-5d29d2ee-0aad-494c-b469-c2d510125f5b) linked from the auth docs contains only five auth/registration requests — no navigation commands. **This is a real documentation hole and the root cause of the ecosystem confusion.**

### The proto layer

Navigation commands are `CarServer.VehicleAction` oneof members delivered to `Domain_DOMAIN_INFOTAINMENT`. The generic dispatch in Tesla's SDK is:

```go
// vehicle-command/pkg/vehicle/infotainment.go
func (v *Vehicle) executeCarServerAction(ctx context.Context, action *carserver.Action_VehicleAction) error
```
which wraps the action in `carserver.Action{ActionMsg: action}`, marshals it, and calls `v.Send(ctx, universal.Domain_DOMAIN_INFOTAINMENT, encodedPayload, v.authMethod)` ([`pkg/vehicle/infotainment.go`](https://github.com/teslamotors/vehicle-command/blob/main/pkg/vehicle/infotainment.go)).

**Tesla's published `car_server.proto` contains no navigation messages at all.** The `VehicleAction` oneof jumps straight from `vehicleControlResetPinToDriveAdminAction = 89` (line 71) to `addChargeScheduleAction = 97` (line 72) ([`pkg/protocol/protobuf/car_server.proto`](https://github.com/teslamotors/vehicle-command/blob/main/pkg/protocol/protobuf/car_server.proto)) — tag 90 is simply absent. The only navigation-adjacent types Tesla ships are read-side: `GetNearbyChargingSites` / `NearbyChargingSites` / `Superchargers` (with `int64 id = 1` and `LatLong location = 10`), exposed via `(*Vehicle) GetNearbyCharging(ctx)`.

The real message definitions (tags 21, 22, 53, 69, 90, 106) are reconstructed from the Tesla mobile app. Two independent reconstructions agree:

- [Teslemetry `tesla-protocol`](https://github.com/Teslemetry/tesla-protocol/blob/main/proto/command/car_server.proto), marked `TESLEMETRY-EXT` (their marker for local additions to upstream-tracked files, per their `AGENTS.md`).
- [vehicle-command PR #443](https://github.com/teslamotors/vehicle-command/pull/443), whose author states: *"I derived the protobuf schema by inspecting the Tesla Android app."*

Composite (field numbers/types as both sources give them):

```proto
// VehicleAction oneof members
NavigationRequest                navigationRequest                = 21;
NavigationSuperchargerRequest    navigationSuperchargerRequest    = 22;
NavigationGpsRequest             navigationGpsRequest             = 53;
NavigationRouteAction            navigationRouteAction            = 69;
NavigationWaypointsRequest       navigationWaypointsRequest       = 90;
NavigationGpsDestinationRequest  navigationGpsDestinationRequest  = 106;

message NavigationRequest { string destination = 1; int32 order = 2; }

message NavigationSuperchargerRequest {
  reserved "order";                      // trip order lives at tag 2
  enum RemoteNavTripOrder {
    REMOTE_NAV_TRIP_ORDER_UNKNOWN = 0;
    REMOTE_NAV_TRIP_ORDER_REPLACE = 1;
    REMOTE_NAV_TRIP_ORDER_PREPEND = 2;
    REMOTE_NAV_TRIP_ORDER_APPEND  = 3;
  }
  int64 id = 1;                          // matches Superchargers.id
  RemoteNavTripOrder remote_nav_trip_order = 2;
}

message NavigationGpsRequest { double lat = 1; double lon = 2; RemoteNavTripOrder order = 3; }

message NavigationGpsDestinationRequest {
  double lat = 1; double lon = 2; string destination = 3; RemoteNavTripOrder order = 4;
}

message NavigationWaypointsRequest {
  message TripPlanOptions {
    int32 destination_start_soe   = 1;   // state-of-energy %, at start
    int32 destination_arrival_soe = 2;   // state-of-energy %, on arrival
  }
  string waypoints = 1;
  TripPlanOptions trip_plan_options = 2;
}

message NavigationRouteAction {}         // "triggers vehicle route navigation"
```

**The strongest evidence that this matches Tesla's internal definition:** in PR #443's review, Tesla maintainer `sethterashima` left the comment *"Rearrange to match internal order"* and pasted the exact `NavigationWaypointsRequest` layout above ([PR #443 review comments](https://github.com/teslamotors/vehicle-command/pull/443)). A Tesla employee comparing the reconstruction against Tesla's internal proto and correcting only the *field ordering* is a de-facto confirmation of the field names, types and tags.

---

## 2. Is multi-waypoint routing possible? (the crux)

**Yes. The API accepts a route with multiple stops. It is not single-destination-only.**

Three separate mechanisms support multiple stops:

**(a) `navigation_waypoints_request` — a whole ordered route in one call.**
```
POST https://<your-proxy>/api/1/vehicles/<VIN>/command/navigation_waypoints_request
Content-Type: application/json

{"waypoints": "refId:ChIJaaa...,refId:ChIJbbb...,refId:ChIJccc..."}
```
"The last entry is the final destination; preceding entries are intermediate stops. `refId:` values are Google Maps place IDs." ([PR #443](https://github.com/teslamotors/vehicle-command/pull/443)). The PR's Go helper:
```go
func (v *Vehicle) NavigateToWaypoints(ctx context.Context, waypoints string) error
func (v *Vehicle) NavigateToWaypointsWithOptions(ctx context.Context, waypoints string, startSoePct, arrivalSoePct int32) error
```
Test result reported in the PR, on a Model 3 running firmware 2026.14.1 with three waypoints: API returned `{"result":true,"reason":""}`; *"In-dash nav correctly shows the full multi-leg route in order"*; *"Trip planner automatically inserts a Supercharger stop when range is insufficient."*

**(b) `order` on the GPS/SC commands — incremental route building.** `REMOTE_NAV_TRIP_ORDER_REPLACE=1` replaces the trip, `PREPEND=2` inserts the stop before the current route, `APPEND=3` adds it at the end. So you can build an N-stop route with N calls: one REPLACE followed by N-1 APPENDs. Tesla's own doc for `navigation_gps_request` says as much: *"Order can be used to specify order of multiple stops."*

> **Field test 2026-10-09: this didn't work.** Firmware 2026.28.5, signed tag 53, one REPLACE followed by three APPENDs. The car acknowledged all four commands, but the screen showed only a dropped pin, "Unknown Location", at the **last** coordinate (`33.856800 S, 151.215300 E`, exactly what was sent). There was no route and no stops, and navigation didn't start until the driver tapped it. The lat/lon fields decode correctly. The REPLACE/APPEND values had no visible effect: each command seems to replace the previous pin. It's still unknown whether `order` is ignored, encoded wrongly in the reconstruction, or depends on navigation already being active.

**(c) The car itself already does multi-stop.** Tesla's owner's manual, "Adding Stops to a Route": *"After entering a destination, edit your route by adding, deleting or reordering stops… Edit Stop allows you to set up a complex trip by adding or deleting stops on your route."* And Tesla's own app already does remote multi-stop send: *"In the Tesla mobile app, go to Locations > Navigate and enter a destination, touch Edit Trip > Add Stop to edit your route, then touch Send to Car to share the trip with your vehicle. NOTE: Requires Tesla mobile app version 4.27.5 or newer."* ([Model X/Y Owner's Manual → Maps and Navigation](https://www.tesla.com/ownersmanual/modely/en_us/GUID-01F1A582-99D1-4933-B5FB-B2F0203FFE6F.html)). That app feature *is* `navigation_waypoints_request` — which is exactly why the schema could be lifted from the Android app.

### Why it doesn't work today

Two dead ends, both verified in source:

1. **Fleet API REST rejects it.** Reported verbatim in [issue #334](https://github.com/teslamotors/vehicle-command/issues/334):
   ```
   POST https://fleet-api.prd.na.vn.cloud.tesla.com/api/1/vehicles/[vin]/command/navigation_waypoints_request
   {"response":null,"error":"Tesla Vehicle Command Protocol required, please refer to the documentation here: ...","error_description":"","txid":"..."}
   ```
2. **Tesla's signing proxy rejects it.** `navigation_gps_request`, `navigation_sc_request` and `navigation_waypoints_request` are not cases in `ExtractCommandAction`, so they hit the `default:` branch which returns HTTP 400 with `{"response":null,"error":"invalid_command","error_description":""}` (`pkg/proxy/command.go:562`). Same issue #334: *"But Vehicle Command Protocol returns invalid_command."* Issue #334 was closed as a duplicate of [#188 "Missing proxy commands"](https://github.com/teslamotors/vehicle-command/issues/188), which is **still open** (last activity 2025-09-14).

Note the asymmetry in the proxy's fallback logic: `ErrCommandUseRESTAPI` makes `ServeHTTP` forward the original request to Tesla (`pkg/proxy/proxy.go:371`, `:509`), but an unrecognised command is a hard 400 that never reaches Tesla. So the three signed navigation commands fail *earlier* than an unimplemented-but-known command would.

### What to do about it

**Option 1 (recommended): vendor the message into your own signing proxy.** Nothing about TVCP requires Tesla's blessing — the vehicle validates a signature over a `RoutableMessage` using *your* enrolled public key. Adding a oneof member at tag 90 and signing it is entirely within your control. This is precisely what [`nappa85/ElectricEel`](https://github.com/nappa85/ElectricEel/blob/master/docs/vehicle-command-patch.md) does: a local copy of vehicle-command v0.4.1 with PR #443 applied verbatim (proto hunk, regenerated `.pb.go`, `pkg/vehicle/navigation.go`), plus hand-encoded tag-21 `NavigationRequest` and tag-53 `NavigationGpsRequest` actions built with `protowire`. Risk: if Tesla's internal tag numbers change, your command silently no-ops or errors — but the maintainer's review comment on #443 makes tag 90 about as safe as an unmerged schema gets.

**Option 2: sequential single-stop sends ("send next leg").** Use `navigation_gps_request` with `order=REPLACE` for the next charging stop, then re-send on progress. Limitations: (a) it's still blocked by the same proxy gap unless you vendor tag 53 too; (b) each send is a billable command and each consumes rate-limit budget; (c) the driver loses the whole-trip overview in the car; (d) you need a trigger for "leg complete."

**Option 3: `navigation_request` only.** Works through official tooling today, single destination, free-text address. Zero multi-stop.

**Detecting leg completion** (needed for options 2 and 3) is the one place `fleet-telemetry` genuinely helps — see §4.

---

## 3. Third-party (non-Supercharger) charger support

| Input form | Command | Accepts non-Tesla POIs? |
|---|---|---|
| Free-text address / share payload | `navigation_request` | **Yes** — server-side geocoded. Any address string. |
| `lat` / `lon` (`double`) | `navigation_gps_request`, `navigation_gps_destination_request` | **Yes** — arbitrary coordinates, no POI database lookup. `navigation_gps_destination_request` additionally carries a `string destination` label so the car shows a name rather than a coordinate. |
| Google Maps place ID (`refId:ChIJ...`) | `navigation_waypoints_request` | **Yes**, for any POI with a place ID — which covers essentially all public Chargefox/Evie/Ampol sites. **No** for a charger with no Google presence; fall back to the nearest addressable POI. |
| Supercharger `int64 id` | `navigation_sc_request` | **No** — Superchargers only. IDs come from `GET /api/1/vehicles/{vin}/nearby_charging_sites` or the on-board `GetNearbyChargingSites` action (`Superchargers.id`). |

Behavioural differences that matter:

- **Preconditioning.** Tesla's owner's manual: *"When navigating to a Supercharger or, in some regions, a third-party fast charger using Trip Planner, Model Y may allocate some energy to pre-heat the Battery."* So third-party DC chargers *can* trigger battery preconditioning, but it is region-gated and Tesla decides — you can't force it. `navigation_sc_request` is the only command that deterministically targets a Supercharger site object (and ABRP's release notes tie their preconditioning behaviour to sending "actual charger details").
- **Trip Planner overrides.** With Trip Planner on, the car may add Supercharger stops to your route on its own if it computes insufficient range (observed in PR #443's test). The manual documents a user-facing "Remove all charging stops" control — you cannot suppress it from the API. **This is the single biggest UX risk for charge-line:** you plan a Chargefox-based route, push it, and the car inserts Superchargers anyway.
- **`TripPlanOptions`.** `destination_start_soe` / `destination_arrival_soe` (integer percent) let you tell the car the state-of-energy you expect at the start and want on arrival. This is the closest thing to charge-line's own SoC model reaching the car's planner. Untested by me; only PR #443 and the Teslemetry protos describe it.

---

## 4. Which API/stack is required

### `teslamotors/vehicle-command` — the SDK and the proxy

This is the Go implementation of TVCP plus `tesla-http-proxy`, which "converts REST API calls to the new vehicle-command protocol" (repo README). The proxy is the intended integration point: you point your backend at it, it signs with your private key, forwards to Fleet API.

Routing behaviour (`pkg/proxy/proxy.go:356-382`): for `POST /api/1/vehicles/{VIN}/command/{cmd}`, if the VIN is known-unsupported → forward raw; else sign and send; if signing returns `ErrCommandUseRESTAPI` → forward raw; if `StartSession` returns `ErrProtocolNotSupported` → mark VIN unsupported and forward raw.

Navigation-specific behaviour (`pkg/proxy/command.go:543-546`):
```go
// Sharing options. These endpoints often require server-side processing, which prevents strict
// end-to-end authentication.
case "navigation_request":
    return nil, ErrCommandUseRESTAPI
```
That is Tesla asserting, in its own code, that `navigation_request` is meant to go over plain REST. The other three navigation commands have no case at all → 400 `invalid_command`.

### `teslamotors/fleet-telemetry` — **premise correction**

This is **not** the Fleet API and it cannot send anything to a car. Per its README: *"Fleet Telemetry is a server reference implementation for Tesla's telemetry protocol… devices establish a WebSocket connection to push configurable telemetry records."* You host it (FQDN, mTLS terminated on the service, Kafka behind it, Helm chart provided), register your app, pair your virtual key, then configure vehicles via `fleet_telemetry_config` — which itself must be signed through the vehicle-command proxy. It is strictly inbound.

It is still useful to charge-line as the *read* side of a send-next-leg loop. Relevant signals ([`protos/vehicle_data.proto`](https://github.com/teslamotors/fleet-telemetry/blob/main/protos/vehicle_data.proto)):

| Field | Tag | Note |
|---|---|---|
| `RouteLastUpdated` | 107 | firmware 2024.26+ |
| `RouteLine` | 108 | full route geometry, 2024.26+ |
| `MilesToArrival` | 109 | 2024.26+ |
| `MinutesToArrival` | 110 | 2024.26+ |
| `DestinationLocation` | 112 | 2024.26+ |
| `DestinationName` | 163 | 2024.26+ |
| `ExpectedEnergyPercentAtTripArrival` | 192 | the car's own arrival-SoC estimate — directly comparable to charge-line's |
| `RouteTrafficMinutesDelay` | 215 | |
| `MaxSpeedToReachDestinationMph` | 265 | |
| `SuperchargerSessionTripPlanner` | 57 | |

Tesla's billing docs push you here hard: Fleet Telemetry is ~$0.00667/hr/car for 1000 signals/hr vs $0.12/hr for equivalent `vehicle_data` polling — a documented 94% reduction ([Billing and Limits](https://developer.tesla.com/docs/fleet-api/billing-and-limits)).

### Fleet API — REST vs signed

Tesla states plainly: *"The Vehicle Command Proxy exposes endpoints identical to the ones described below. When it receives a request, it signs the command with a virtual key before passing the request to Fleet API. If a command is not signed, the vehicle will reject the request and perform no action."* ([Vehicle Commands](https://developer.tesla.com/docs/fleet-api/endpoints/vehicle-commands)).

**Where the cutoff is:**

- *"Note: The Vehicle Commands Proxy is not required for most business vehicles and Pre-2021 S and X vehicles."* (same page)
- vehicle-command README: *"Pre-2021 Model S and X vehicles do not support this new protocol. Fleet API will continue to work on these vehicles."*
- The authoritative per-vehicle answer is `POST /api/1/vehicles/fleet_status`, which returns `vehicle_command_protocol_required` ("If the vehicle requires the Vehicle Command Protocol"), plus `firmware_version`, `fleet_telemetry_version`, `total_number_of_keys` (max 20) ([Vehicle Endpoints](https://developer.tesla.com/docs/fleet-api/endpoints/vehicle-endpoints)). **Call this before every command path decision; don't infer from model/year.**
- The historical rollout ([Announcements, 2023-11-17](https://developer.tesla.com/docs/fleet-api/announcements)): Nov 2023 newly-delivered vehicles TVCP-only; Nov–Dec 2023 REST deprecated on vehicles not using it in the prior 30 days; Jan 2024 all vehicles require TVCP, REST fully deprecated. Fleet (business) accounts and pre-2021 S/X excluded.

There is also a generic `POST /api/1/vehicles/{vin}/signed_command` — *"a generic endpoint replacing legacy commands… It uses the Tesla Vehicle Command Protocol"* — which is what the SDK targets under the hood if you want to skip the proxy and sign in-process.

**Practical mapping for charge-line:**

| Vehicle | `navigation_request` | `navigation_gps/sc/waypoints_request` |
|---|---|---|
| Pre-2021 S/X, business fleet vehicles | plain REST | plain REST (should work; unverified by me) |
| Everything else (TVCP required) | plain REST via proxy fallback | **must be signed; requires your own patched SDK today** |

---

## 5. Cost and gates

**Registration chain** (all mandatory before a single command):

1. Create an application at developer.tesla.com; choose "Authorization Code and Machine-to-Machine" for a consumer app.
2. Generate an EC P-256 key: `openssl ecparam -name prime256v1 -genkey -noout -out private-key.pem`. *"the vehicle only supports prime256v1 keys."*
3. Host the public key at **`https://<your-domain>/.well-known/appspecific/com.tesla.3p.public-key.pem`** and keep it there — since Tesla mobile app 4.30.0 it must remain hosted for pairing continuity ([Announcements 2024-02-02](https://developer.tesla.com/docs/fleet-api/announcements)).
4. `POST /api/1/partner_accounts` with a partner token. The domain must match the root domain of your `allowed_origins`, and *"will be displayed to users as part of the mobile-app-based vehicle key-pairing process."* ([Partner Endpoints](https://developer.tesla.com/docs/fleet-api/endpoints/partner-endpoints))
5. **Per-user virtual key pairing.** The user must be sent to `https://tesla.com/_ak/<your-domain>` (optionally `?vin=...`) and approve in the Tesla app; removal is via the car's Locks screen ([Virtual Keys Developer Guide](https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide)). **This is a hard consumer-UX gate** — a second app, a deep link, and an in-car concept most drivers have never heard of. Automatic pairing exists only for B2B-program vehicles.

**Scopes** ([Authentication Overview](https://developer.tesla.com/docs/fleet-api/authentication/overview)): `openid`, `offline_access` (required for a refresh token), `vehicle_device_data`, **`vehicle_location`** (separate since Nov 2024; without it you lose location functionality), and `vehicle_cmds` for commands. *Inference:* navigation commands fall under `vehicle_cmds` — Tesla's vehicle-commands page lists **no** per-endpoint scopes, so this is not directly cited. `vehicle_charging_cmds` is charging-specific and probably not needed for nav. Tesla warns: *"it is only permissible to request authorization for scopes that are immediately necessary."*

**Pricing** ([developer.tesla.com](https://developer.tesla.com/) home + [Billing and Limits](https://developer.tesla.com/docs/fleet-api/billing-and-limits)):

| Category | Rate |
|---|---|
| Commands | 1,000 requests / $1 |
| Data (`vehicle_data`) | 500 requests / $1 |
| Wakes | 50 requests / $1 |
| Streaming signals | 150,000 signals / $1 |
| Monthly discount | $10 per account |

- All responses with status < 500 are billable; ≥ 500 are not.
- Default billing limit is **0** until a payment method is added; exceeding it suspends API usage **and removes Fleet Telemetry streaming configs — which are not restored**.
- Australia is in the supported-payment list (AP: JP, KR, **AU**, TW, NZ, HK, MO, MY, TH, PH). Base URL for AU is the NA region host: `https://fleet-api.prd.na.vn.cloud.tesla.com` ("North America, Asia-Pacific (excluding China)") ([Regions and Countries](https://developer.tesla.com/docs/fleet-api/getting-started/regions-countries)).

**Rate limits** (per device, per account; **shared across all apps touching the same vehicle**): Realtime Data 60/min, Wakes 3/min, **Device Commands 30/min**. A send-next-leg design that re-sends on progress must respect 30/min/car and, more importantly, must not wake the car unnecessarily (3/min, 50 wakes per $1).

**Other hard facts:** *"Is there a staging environment for Fleet API? No. There are no simulators or staging environments available."* ([FAQ](https://developer.tesla.com/docs/fleet-api/support/faq)). Refresh tokens last 3 months; acquiring a new refresh token invalidates the previous one and its access tokens. A user must have logged into the Tesla mobile app at least once before API calls on their behalf succeed.

**Cost sanity check for charge-line (inference):** a trip with 4 charging stops sent as a whole route = 1 command = $0.001. Sent leg-by-leg with a re-send on each progress update = 4-8 commands = still under a cent. Commands are not the cost driver; **wakes and data polling are**. Budget on the order of $0.02–$0.10 per active trip per car if you use Fleet Telemetry for state and avoid gratuitous wakes.

---

## 6. BLE as an alternative

Tesla publishes the complete BLE profile ([`pkg/protocol/protocol.md`](https://github.com/teslamotors/vehicle-command/blob/main/pkg/protocol/protocol.md)):

- Service UUID `00000211-b2d1-43f0-9b88-960cebf8b91e`
- Write characteristic `00000212-…` (write-with-response), read characteristic `00000213-…`
- Advertisement local name `S + <ID> + C`, where `<ID>` is lowercase hex of the first 8 bytes of `SHA1(VIN)` — e.g. VIN `5YJS0000000000000` → `S1a87a5a75f3df858C`
- Messages are length-prefixed with a 2-byte big-endian length
- *"Due to hardware constraints, VCSEC can only reliably maintain up to three simultaneous BLE connections. These are shared by keyfobs and phone keys."*

**Does BLE carry navigation?** Yes — navigation actions are ordinary `VehicleAction`s on the Infotainment domain, and the domain is transport-agnostic. Teslemetry's client exposes `navigation_request`, `navigation_gps_request`, `navigation_sc_request`, `navigation_waypoints_request` and `navigation_gps_destination_request` over BLE, noting *"These commands are ACK-only over BLE; the library returns the vehicle's command acknowledgement, but there is no separate BLE state prover for the navigation destination"* ([Teslemetry `docs/bluetooth_vehicles.md`](https://github.com/Teslemetry/python-tesla-fleet-api/blob/main/docs/bluetooth_vehicles.md), community). ElectricEel is a shipping BLE-only app doing exactly this.

**Constraints for a mobile app:**

- **No mobile SDK.** Tesla's is Go; `tesla-control` "does not run on Windows due to limitations in the available Golang BLE packages", and there is no iOS/Android binding. You reimplement the handshake (ECDH P-256 → SHA1 → 128-bit AES-GCM session key), metadata TLV serialization, and anti-replay counters yourself. On iOS that's CoreBluetooth + CryptoKit; on Android, `BluetoothGatt` + Conscrypt. *Inference: 2-4 weeks of specialist work, and it is security-critical code.*
- **Proximity only.** Useless for "plan on the couch, push to car." Fine for "you're standing at the car, send the route."
- **Pairing.** Over BLE you can enroll your own key with `tesla-control -ble add-key-request public_key.pem owner cloud_key` — *"The program should instruct you to confirm the new key by tapping your NFC card on the center console."* ([`cmd/tesla-control/README.md`](https://github.com/teslamotors/vehicle-command/blob/main/cmd/tesla-control/README.md)). That path needs **no Tesla partner account, no domain, no OAuth, no billing** — a genuinely interesting escape from §5's gates, at the cost of asking the user to find their key card. Alternatively use the `tesla.com/_ak/<domain>` deep link, which drags the partner registration back in.
- **Contention.** 3 concurrent connections shared with keyfobs/phone keys means a car with two phone keys nearby may refuse you.
- **Wake.** *"VCSEC can be reached over BLE even when infotainment is asleep"* — the corollary is that Infotainment (where nav lives) may need waking first, which BLE can do via VCSEC.

**Verdict:** worth building as a *secondary* path — "send route" works offline, costs nothing per command, and sidesteps Fleet API billing entirely. Not a substitute for the cloud path.

---

## 7. What the incumbents actually do

**ABRP (Iternio).** First-party release note, v4.6.0 (2023-09-08): *"The 'Send to Tesla' feature now supports the actual charger details being shared with the car, allowing the Tesla to precondition the battery for charging at the location."* ([abetterrouteplanner.com](https://abetterrouteplanner.com/resources/article/2023-09-08_abrp-4-6-0)). Note what is *not* claimed: the whole route. Sending "the actual charger details" such that the car preconditions is consistent with `navigation_sc_request` (Supercharger id) or `navigation_gps_request` to a single charger.

ABRP's own forum (forum.abetterrouteplanner.com) carries the explicit statement *"Since Tesla doesn't handle waypoints, the whole plan cannot be sent at once but you can send one leg at a time."* — **caveat: the ABRP forum was returning Cloudflare error 525 throughout this research and I could not load the thread to confirm authorship or date; this text came from a search-engine snippet. Treat as community-reported, not verified.** It is consistent with ABRP's release notes and with everything in §2. Community reports (Tesla Motors Club, unverified) also describe ABRP auto-sending the next waypoint as the previous one is reached, with the advice not to rely on it.

**PlugShare.** No Tesla send-to-car at all. Their own support article "PlugShare In Your Vehicle" lists exactly three options — Android Auto, CarPlay, and head-unit "Vehicle sign in" — and states you need a *"Vehicle with Android Auto or CarPlay compatible"* ([help.plugshare.com](https://help.plugshare.com/hc/en-us/articles/6111705869075-PlugShare-In-Your-Vehicle)). Teslas have none of those.

**Tesla's own app** is the existence proof for multi-stop remote send (§2(c)) — and it is the reference implementation the community reverse-engineers.

**Conclusion:** no incumbent has shipped whole-route-with-waypoints to a Tesla. If charge-line ships it, that is a genuine differentiator — and also a signal that it is harder than it looks.

---

## 8. Non-Tesla escape hatches

- **CarPlay / Android Auto — not available today.** Tesla has never supported either; PlugShare's requirement of a CarPlay/Android-Auto-capable vehicle is indirect first-party confirmation, and nothing in Tesla's owner's manuals or support site documents CarPlay. Trade press (autoevolution, The Apple Post, et al. — **not primary, and I found no Tesla first-party statement**) reports Tesla announced CarPlay support in 2026 but had not shipped it as of the 2026 Spring update. Treat "Teslas do not have CarPlay" as true today and as a watch item.
- **CarPlay route sharing (if/when Tesla ships CarPlay).** Apple added, in iOS 27, `CPNavigationSession.isRouteSharingSupported` — *"Whether the connected vehicle supports the route sharing feature"* — alongside `isRouteSharingEnabled` (*"Whether the vehicle is presently using route data for any features in its built-in navigation system"*), `routeSegments`, `addRouteSegments(_:)` (*"add CPRouteSegments in chronological order… as soon as they are available"*), and `resumeNavigation(updatedTrip:routeSegments:currentSegment:rerouteReason:)` ([Apple Developer: CPNavigationSession](https://developer.apple.com/documentation/carplay/cpnavigationsession)). This is a first-party API for handing a third-party nav app's **full route geometry** to the car — structurally a better fit for charge-line than Tesla's string-of-place-IDs endpoint. Gated on (a) Tesla shipping CarPlay and (b) Apple's CarPlay navigation entitlement, which is application-only.
- **Tesla's share sheet.** *"You can start navigation remotely from your iOS® or Android™ device using the 'share' functionality on your device after allowing access to the Tesla mobile app."* (Owner's Manual). Zero-integration, zero-cost, works for every Tesla: charge-line emits a standard share intent / `UIActivityViewController` payload, the user picks Tesla. **Single destination only**, and it depends on the user having the Tesla app installed. This is the free 80%-of-value fallback and should exist regardless of what else you build.
- **Deep links into the Tesla app.** `https://tesla.com/_ak/<domain>` is the documented key-pairing link. No documented deep link for "open Tesla app with this route pre-filled."
- **In-car browser.** Tesla ships a browser, but there is no documented mechanism for a web page to set the car's navigation destination. *Inference: not a viable path.*
- **Apple Maps / Google Maps handoff.** Both can share a destination to the Tesla app on the phone (which then does `navigation_request`). Still single-destination — it's the same share-sheet mechanism, just originating elsewhere.

---

## Decision / implications for charge-line

**What is actually buildable, in order of effort:**

| Tier | Mechanism | Multi-stop | Third-party chargers | Gates | Effort |
|---|---|---|---|---|---|
| 0 | OS share sheet → Tesla app | No | Yes (address) | none | hours |
| 1 | Fleet API `navigation_request` (unsigned REST) | No | Yes (address) | partner reg, OAuth, billing, (virtual key?) | days |
| 2 | Self-signed TVCP with vendored proto: `navigation_gps_request` + `order` | Yes, N calls | Yes (lat/lon) | tier 1 + virtual key + signing infra + unofficial proto | 1-2 weeks |
| 3 | Self-signed TVCP `navigation_waypoints_request` | **Yes, one call** | Yes (place IDs) | tier 2 + Google Place ID resolution for every stop | +days |
| 4 | BLE direct | Yes | Yes | NFC-card pairing, native BLE+crypto reimplementation, proximity | weeks |

> **Revised after field tests (2026-10-13):** tier 3 works on a real car. Tier 2 doesn't: the car showed only a pin at the last stop. Build tier 3 with a **tier-1 fallback**, and sign inside the app's own backend. A `tesla-http-proxy` fork isn't needed. See [Field results](#field-results-what-we-confirmed-on-a-real-car).

**Recommendation.** Ship **tier 0 immediately** (it costs nothing and covers the common "just get me to the next charger" case), then build **tier 3 with a tier-2 fallback** behind a feature flag. Run your own fork of `tesla-http-proxy` with PR #443 applied — do not wait for Tesla to merge it; #188 has been open since Feb 2024. Keep the fork narrow (one proto hunk, one Go file) so you can drop it the day upstream lands the change.

**What to promise the user.** Be specific and hedged:

- ✅ "Send your whole trip to your Tesla" — but gate it on `fleet_status.vehicle_command_protocol_required` + successful virtual-key check, and label it Beta.
- ✅ "Send the next charging stop to your Tesla" — always available, always works.
- ⚠️ **Do not promise that the car will keep your exact charging stops.** Tesla's Trip Planner may add its own Supercharger stops. Say so in the UI: *"Your Tesla may add its own Supercharger stops if it thinks you'll run low."* Consider surfacing the car's own `ExpectedEnergyPercentAtTripArrival` from Fleet Telemetry next to charge-line's estimate so the divergence is visible rather than surprising.
  **Field-tested 2026-10-13:** it *will* add them after every third-party stop, because the car plans no charging at those stops. One tap on "Remove all charging stops" removes them, and they don't come back, but the car then shows a "Charging needed to reach destination" warning. Tell the driver both things.
- ❌ Do not promise preconditioning at third-party chargers — it is region-gated and Tesla-controlled.

**Realistic UX.**

1. Plan trip in charge-line → "Send to car" button.
2. First use: Tesla account link (OAuth) → virtual-key pairing deep link → explain in one sentence why ("your car has to trust our key before it will accept a route").
3. On send: resolve each stop to a Google place ID; single `navigation_waypoints_request` with `trip_plan_options.destination_arrival_soe` set from charge-line's own arrival-SoC target.
4. On failure (no place ID, unsupported vehicle, unpaired key): silently degrade to `navigation_gps_request` REPLACE+APPEND chain, then to `navigation_request` with the final destination address, then to the OS share sheet. **Design the degradation ladder up front** — every rung has a different failure mode and you will hit all of them.
   **Revised 2026-10-09 after field tests:** drop the GPS chain from the default ladder. On a real car it left a pin at the final stop only, while `navigation_request` started navigation *and* had Trip Planner add charging stops. Go straight from waypoints to `navigation_request`. A command being acknowledged doesn't mean the route appeared.
5. Subscribe to Fleet Telemetry `DestinationName` / `MilesToArrival` / `RouteLine` to show "trip is loaded in your car" and to detect leg completion for the tier-2 path. Never poll `vehicle_data` for this.
6. Respect 30 commands/min/vehicle and treat wakes as expensive; check `fleet_status` before sending rather than firing and retrying.

**The honest risk.** Tier 3 depends on a proto tag Tesla has not published. It is corroborated by a Tesla employee's review comment and an end-to-end test on 2026.14.1, but it is not a contract. Instrument it: log every `navigation_waypoints_request` response, alarm on a rise in non-`result:true` responses, and keep the tier-2/tier-1 ladder hot so a firmware change degrades the feature instead of breaking the app.

---

## Open questions

1. **Does `navigation_request` really work unsigned on a TVCP-required vehicle?** Tesla's own proxy forwards it rather than signing it, with a comment explaining why — strong evidence, but I found no test report either way. **Resolves by:** one `curl` to `POST /api/1/vehicles/{vin}/command/navigation_request` on a post-2021 car, straight to Fleet API, bypassing the proxy.
   **Resolved 2026-10-09: yes.** The POC sent it straight to Fleet API (NA region, no proxy), with Teslemetry's body shape, to a car reporting "signed commands required" (firmware 2026.28.5). The car showed "Calculating… Bennelong Point" for about 15 s. Trip Planner then added Supercharger stops on its own, starting at Wangaratta.
2. **Is a virtual key required for unsigned commands at all,** or only for signed ones? Tesla's wording ("To accept commands, a vehicle must have an application's virtual key installed") is unqualified, which conflicts with the proxy forwarding `navigation_request`. **Resolves by:** the same test, run once before and once after pairing.
   **Half answered 2026-10-09:** it works *with* the key paired. Still untested without it.
3. **Exact `waypoints` string grammar.** PR #443 gives `refId:<placeId>` comma-separated. Unknown: whether raw `lat,lon` tokens, `refId:` mixed with coordinates, or a max count are accepted. **Resolves by:** trial against a real vehicle, or by capturing the Tesla Android app's own request.
4. **`TripPlanOptions` semantics.** Are `destination_start_soe` / `destination_arrival_soe` percentages or per-mille? Does the car honour them or treat them as hints? Both reconstructions declare them `int32` with no unit. **Resolves by:** empirical test comparing in-car charging plan with and without the field set.
   **Hint 2026-10-09:** after a navigation send, the car prompts "Set arrival energy at your destination in the turn list", a percentage setting. `destination_arrival_soe` probably sets this (unconfirmed).
   **Field test 2026-10-09 (strong evidence):** we sent `destination_arrival_soe=28`, and the car showed **28%** arrival at the destination. It planned a charge to hit it (Exeter, arriving at 10%). The same trip sent destination-only showed 12%. So it's a **percentage, and the car honours it**. We also sent `destination_start_soe=90`, with no visible effect: the first-leg arrival (30%) matched the destination-only run's (29%), which used the car's real charge. Its meaning is still unknown.
   **Caveat, 2026-10-13:** the arrival target only applies while Trip Planner is planning charging. After "Remove all charging stops", or with Trip Planner off, destination arrival showed 10%, not 28%.
5. **Whether PR #443 lands.** As of 2026-09-21 it is open, last updated 2026-04-23, with a Tesla maintainer saying *"I'll try to validate this week or next."* **Resolves by:** watching the PR and the repo tags.
6. **Whether `navigation_gps_request` / `navigation_sc_request` reach Fleet API unsigned on old vehicles.** Issue #334's title covers all three but its body only shows the waypoints response.
7. **Does Trip Planner respect an all-third-party route,** or does it always add Superchargers? PR #443 saw insertion only when range was insufficient. **Resolves by:** testing a route whose third-party stops already satisfy range.
   **Data point 2026-10-09:** with only a destination sent (Melbourne → Sydney, nothing in between), Trip Planner added Superchargers on its own. This is expected when the route can't be driven on one charge, so it doesn't answer the question.
   **Answered in part 2026-10-09:** no, at least by default. Trip Planner plans no charging at third-party waypoints, so it added Superchargers after Evie and after Chargefox. Still to test: the turn list's "Remove all charging stops" link, the car's Trip Planner setting turned off, and any way to mark a waypoint as a charging stop.
   **"Remove all charging stops" tested 2026-10-13:** one tap removed only the Superchargers Trip Planner had added. Every stop we sent stayed, including the Gundagai Supercharger, which stayed a charging stop. Trip Planner did **not** re-add anything; the link became "Add charging stops". The car still plans no charging at Evie, though. It showed a red "Charging needed to reach destination" banner and −24% arrival at Gundagai, and planned a 37-minute charge there to make up for it. Destination arrival dropped to 10%, not the 28% we sent. The driver gets the right route with one tap, but the car's energy numbers stay wrong until they actually charge at Evie (not yet observed).
   **Trip Planner setting off, tested 2026-10-13:** the result was identical to the tap. Only our 4 stops appeared, Gundagai stayed a charging stop (38 min), the same red warning showed (−24% at Gundagai), and destination arrival was 10%. It saves the tap, but it's a car-wide setting that also stops Supercharger planning on the driver's other trips. Tesla's command protocol has no command to change it: `vehicle.proto` only exposes `supercharger_session_trip_planner` as read-only status.
8. **Tesla + CarPlay timeline.** No first-party Tesla statement located. **Resolves by:** Tesla release notes / Tesla's own newsroom.
9. **ABRP's exact current implementation.** Their forum was down (HTTP 525) for the whole session. **Resolves by:** re-reading forum.abetterrouteplanner.com threads 4103 / 2804 / 3019, or by MITM-ing the ABRP app's Fleet API traffic.

---

## Sources

**Source code (cloned and read locally; commit `e35ef16`, 2026-08-30 for vehicle-command, `8fbaa10`, 2026-08-28 for fleet-telemetry)**

1. [`vehicle-command/pkg/proxy/command.go`](https://github.com/teslamotors/vehicle-command/blob/main/pkg/proxy/command.go) — lines 543-546: `navigation_request` → `ErrCommandUseRESTAPI` with Tesla's "sharing options… server-side processing" comment; line 562: `default:` → HTTP 400 `invalid_command`. Establishes that three of four navigation commands are unimplemented and one is deliberately unsigned.
2. [`vehicle-command/pkg/proxy/proxy.go`](https://github.com/teslamotors/vehicle-command/blob/main/pkg/proxy/proxy.go) — lines 356-382, 460-520: the command routing table and the `ErrCommandUseRESTAPI` → `forwardRequest` fallback.
3. [`vehicle-command/pkg/protocol/protobuf/car_server.proto`](https://github.com/teslamotors/vehicle-command/blob/main/pkg/protocol/protobuf/car_server.proto) — the full `VehicleAction` oneof: tag 89 → 97 with no tag 90; `Superchargers.id`/`LatLong location`; no navigation messages anywhere.
4. [`vehicle-command/pkg/vehicle/infotainment.go`](https://github.com/teslamotors/vehicle-command/blob/main/pkg/vehicle/infotainment.go) — `executeCarServerAction` / `getCarServerResponse` dispatch to `Domain_DOMAIN_INFOTAINMENT`; `GetNearbyCharging`; no navigation helper.
5. [`vehicle-command/pkg/protocol/protocol.md`](https://github.com/teslamotors/vehicle-command/blob/main/pkg/protocol/protocol.md) — lines 150-164: BLE service/characteristic UUIDs, advertisement name derivation, 2-byte length framing, 3-connection limit; §Domains, §Roles.
6. [`vehicle-command/README.md`](https://github.com/teslamotors/vehicle-command) — pre-2021 S/X exclusion; proxy overview; OAuth + private key model.
7. [`vehicle-command/cmd/tesla-control/README.md`](https://github.com/teslamotors/vehicle-command/blob/main/cmd/tesla-control/README.md) — BLE key enrollment via `add-key-request` + NFC card tap; no Windows support.
8. [`fleet-telemetry/README.md`](https://github.com/teslamotors/fleet-telemetry) — establishes fleet-telemetry is an inbound telemetry *server*, not a command path; 13-step setup incl. mTLS and vehicle-command proxy dependency.
9. [`fleet-telemetry/protos/vehicle_data.proto`](https://github.com/teslamotors/fleet-telemetry/blob/main/protos/vehicle_data.proto) — route/destination signal enum values (107-112, 163, 192, 215, 265, 57) and their firmware requirements.

**Tesla first-party documentation**

10. [Fleet API → Vehicle Commands](https://developer.tesla.com/docs/fleet-api/endpoints/vehicle-commands) — the four navigation endpoint paths + descriptions; the signed-command requirement; "not required for most business vehicles and Pre-2021 S and X". Confirmed by DOM inspection to contain **no** parameter tables or scope labels for these commands.
11. [Fleet API → Vehicle Endpoints](https://developer.tesla.com/docs/fleet-api/endpoints/vehicle-endpoints) — `fleet_status` fields incl. `vehicle_command_protocol_required`; `signed_command`; `nearby_charging_sites`; no `get_active_route`.
12. [Fleet API → Partner Endpoints](https://developer.tesla.com/docs/fleet-api/endpoints/partner-endpoints) — `POST /api/1/partner_accounts`, domain matching, `.well-known` public key hosting requirement.
13. [Fleet API → Virtual Keys Developer Guide](https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide) — prime256v1 only, `.well-known/appspecific/com.tesla.3p.public-key.pem`, `https://tesla.com/_ak/<domain>?vin=` pairing deep link, removal via Locks screen.
14. [Fleet API → Authentication Overview](https://developer.tesla.com/docs/fleet-api/authentication/overview) — token types and the full scope table (`vehicle_cmds`, `vehicle_location`, `offline_access`, …); link to Tesla's Postman collection.
15. [Fleet API → Billing and Limits](https://developer.tesla.com/docs/fleet-api/billing-and-limits) — billing mechanics, $10 monthly discount, billing-limit-exceeded behaviour (telemetry configs not restored), rate limits 60/3/30 per minute, cost-optimisation case studies.
16. [developer.tesla.com home](https://developer.tesla.com/) — the pricing table: Commands 1,000/$1, Data 500/$1, Wakes 50/$1, Streaming 150,000/$1.
17. [Fleet API → Announcements and Changelog](https://developer.tesla.com/docs/fleet-api/announcements) — 2023-11-17 TVCP rollout dates and exclusions; 2024-02-02 public-key hosting requirement; 2024-11-26 `vehicle_location` scope split; 2024-11-27 pay-per-use.
18. [Fleet API → Regions and Countries](https://developer.tesla.com/docs/fleet-api/getting-started/regions-countries) — AU is served by the NA base URL and is a payment-supported country.
19. [Fleet API → FAQ](https://developer.tesla.com/docs/fleet-api/support/faq) — no staging/simulator; 429/408 semantics; refresh-token lifetime; virtual-key-removal detection.
20. [Tesla Owner's Manual → Maps and Navigation (Model Y / Model X)](https://www.tesla.com/ownersmanual/modely/en_us/GUID-01F1A582-99D1-4933-B5FB-B2F0203FFE6F.html) — "share" from iOS/Android to start navigation; "Adding Stops to a Route" / "Edit Stop… complex trip"; Tesla app "Edit Trip > Add Stop… Send to Car" (app 4.27.5+); Trip Planner behaviour and "Remove all charging stops"; preconditioning at "a Supercharger or, in some regions, a third-party fast charger".
21. [Tesla Fleet API Postman collection](https://www.postman.com/crimson-space-512892/workspace/fleet-api/collection/33220881-5d29d2ee-0aad-494c-b469-c2d510125f5b) — linked from Tesla's auth docs; contains only 5 auth/registration requests, no navigation commands (fetched via Postman's public collection API).

**Tesla repo issues/PRs (first-party venue, third-party authors, with Tesla maintainer participation)**

22. [vehicle-command PR #443 — "Add support for navigation_waypoints_request command"](https://github.com/teslamotors/vehicle-command/pull/443) — the proto hunk at tag 90, `NavigateToWaypoints{,WithOptions}` signatures, the proxy case, the `refId:<placeId>` waypoints format, and the end-to-end test on a Model 3 (2026.14.1). Open, unmerged as of 2026-09-21.
23. [PR #443 review comments by `sethterashima` (Tesla maintainer)](https://github.com/teslamotors/vehicle-command/pull/443) — *"Rearrange to match internal order"* with the exact `NavigationWaypointsRequest` layout; *"I'll try to validate this week or next."* The strongest corroboration that the reconstructed schema matches Tesla's internal definition.
24. [vehicle-command issue #334](https://github.com/teslamotors/vehicle-command/issues/334) — verbatim Fleet API error `"Tesla Vehicle Command Protocol required"` for `navigation_waypoints_request`, and `invalid_command` from the proxy. Closed as dupe of #188.
25. [vehicle-command issue #188 — "Missing proxy commands"](https://github.com/teslamotors/vehicle-command/issues/188) — open since 2024-02-16; enumerates the missing navigation commands; last bump 2025-09-14 confirming they remain non-functional.

**Community implementations (labelled; used for schema corroboration and BLE feasibility only)**

26. [Teslemetry `tesla-protocol` → `proto/command/car_server.proto`](https://github.com/Teslemetry/tesla-protocol/blob/main/proto/command/car_server.proto) — `TESLEMETRY-EXT`-marked navigation messages at tags 21/22/53/69/90/106, the `RemoteNavTripOrder` enum, and `NavigationWaypointsRequest.TripPlanOptions`. Independent of PR #443 and in agreement with it.
27. [Teslemetry `tesla-protocol` AGENTS.md](https://github.com/Teslemetry/tesla-protocol/blob/main/AGENTS.md) — defines `TESLEMETRY-EXT` as local (non-upstream) additions; documents the `NavigationSuperchargerRequest` reserved-`order` situation.
28. [Teslemetry `python-tesla-fleet-api` `tesla/vehicle/fleet.py`](https://github.com/Teslemetry/python-tesla-fleet-api/blob/main/tesla_fleet_api/tesla/vehicle/fleet.py) — concrete REST bodies: `navigation_gps_request {lat,lon,order}`, `navigation_request {value:{"android.intent.extra.TEXT":…},type:"share_ext_content_raw",locale,timestamp_ms}`, `navigation_sc_request {id,order}`, `navigation_waypoints_request {waypoints}`.
29. [Teslemetry `docs/bluetooth_vehicles.md`](https://github.com/Teslemetry/python-tesla-fleet-api/blob/main/docs/bluetooth_vehicles.md) and [`docs/fleet_api_signed_commands.md`](https://github.com/Teslemetry/python-tesla-fleet-api/blob/main/docs/fleet_api_signed_commands.md) — navigation commands over BLE and over signed Fleet API; `order` semantics (1 replace / 2 prepend / 3 append); ACK-only over BLE.
30. [`nappa85/ElectricEel` `docs/vehicle-command-patch.md`](https://github.com/nappa85/ElectricEel/blob/master/docs/vehicle-command-patch.md) — a working precedent for vendoring PR #443 plus hand-encoded tag-21/tag-53 actions into a BLE-only app.
31. [`tdorssers/TeslaPy` `endpoints.json`](https://github.com/tdorssers/TeslaPy/blob/master/teslapy/endpoints.json) — legacy `get_active_route`; confirms route readback was Owner API, not Fleet API.

**Incumbent apps (first-party where available)**

32. [ABRP 4.6.0 release notes](https://abetterrouteplanner.com/resources/article/2023-09-08_abrp-4-6-0) — "Send to Tesla… supports the actual charger details being shared with the car, allowing the Tesla to precondition the battery."
33. forum.abetterrouteplanner.com (ABRP's own forum) — *"Since Tesla doesn't handle waypoints, the whole plan cannot be sent at once but you can send one leg at a time."* **Unverified: site returned Cloudflare 525 throughout; quote obtained from a search-engine snippet, authorship and date unconfirmed.**
34. [PlugShare Support: "PlugShare In Your Vehicle"](https://help.plugshare.com/hc/en-us/articles/6111705869075-PlugShare-In-Your-Vehicle) — in-vehicle access requires Android Auto, CarPlay, or a head-unit app platform; no Tesla send-to-car.

**Apple (for the CarPlay escape hatch)**

35. [Apple Developer: `CPNavigationSession`](https://developer.apple.com/documentation/carplay/cpnavigationsession) — `isRouteSharingSupported`, `isRouteSharingEnabled`, `routeSegments`, `addRouteSegments(_:)`, `resumeNavigation(updatedTrip:routeSegments:currentSegment:rerouteReason:)`.
36. [Apple Developer: `isRouteSharingSupported`](https://developer.apple.com/documentation/carplay/cpnavigationsession/isroutesharingsupported) — *"Whether the connected vehicle supports the route sharing feature"*; `var isRouteSharingSupported: Bool { get }`; introduced iOS/iPadOS/Mac Catalyst 27.0 (per Apple's documentation JSON).
