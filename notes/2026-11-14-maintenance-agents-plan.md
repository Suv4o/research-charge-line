# Maintenance Agents: The Plan, the Data Repo and a POC for Every Option

**Date:** 2026-11-14
**For:** the owner, before building anything. It pulls together the decisions taken on 14 November, the design for
moving the vehicle catalogue and charging prices into a public repo, and how to try every agent platform on the same
small job. The platform facts are in [maintenance agents](2026-11-12-maintenance-agents.md) (Claude's options) and
[agent platforms compared](2026-11-14-agent-platforms-compared.md) (OpenAI, Google and the rest). The two data
questions are in [charging prices per network](2026-11-14-charging-prices-per-network.md) and
[finding new EVs](2026-11-14-new-ev-discovery.md).

> **Update, 15 November 2026:** the owner moved the agents to **GitHub Agentic Workflows with the Claude engine**,
> billed through the Anthropic API (about US$6 a month, estimate). The reasons are stronger guard rails, no sharing
> of the Pro plan's limits, and a worked example to show others. The cloud scheduled tasks below are no longer the
> plan. The data repo, server and app design (§2–§5) carry over. See
> [maintenance agents on GitHub Agentic Workflows](2026-11-15-github-agentic-workflows.md).

## Bottom line

- **Platform:** Claude Code's cloud scheduled tasks stay first. No competitor beats them on cost (A$0 on top of the
  Claude plan) or on keeping secrets out of the agent's reach. Every alternative is a second bill of about US$10–40 a
  month or pay-per-token ([agent platforms compared](2026-11-14-agent-platforms-compared.md)).
  - **OpenAI:** no cloud scheduler for repo work. Its working route is the Codex GitHub Action on an Actions schedule,
    paid through the API (about US$5–25 a month, estimate).
  - **Google:** Jules closes on 31 December 2026, and its replacement's cloud agents are days old.
  - **GitHub Copilot automations:** the best pull-request guard rails, but private repos only, so not for the public
    data repo.
- **Catalogue agent:** it can find cars new to Australia, from sources it may read. The catalogue is already behind
  ([finding new EVs](2026-11-14-new-ev-discovery.md)):
  - four of the cars listed as "not confirmed" on 22 October are on sale;
  - two new brands (Hongqi as "HQ", and Avatr) start deliveries in 2027;
  - Chery sold 279 EVs last month with no entry in the catalogue.
- **Prices:** a typical price per network stays the method. Per-site prices aren't possible from the networks
  themselves ([charging prices per network](2026-11-14-charging-prices-per-network.md)):
  - each network shows a site's price only in its app;
  - three networks' terms forbid robots (Chargefox, Jolt and Exploren), and two sites block automated readers;
  - NRMA's public table needs its permission.
  - Per-site prices come instead from drivers' reports (already in the app) and Open Charge Map.
- **Next:** build `charge-line-data`, then run the same small POC job on each platform, the free ones first (§7).

## Decisions after the research (14 November)

- **Platform: Claude Code cloud scheduled tasks only.** No proof of concept for each option: §7's table is kept as
  a record of what was considered.
- **Plan: Claude Pro.**
  - Scheduled runs share Pro's usage limits with everything else, so they run in Melbourne's small hours and stay
    small (the catalogue split into weekly batches).
  - The API-billed options (Managed Agents, GitHub Agentic Workflows, the Codex action) are out.
- **POCs repo:** [charge-line-pocs](https://github.com/Suv4o/charge-line-pocs) (public).
- **The price agent also finds new charging networks** and adds them to the list with their prices (§4, "New
  networks").

## 0. The three research notes in one table

| Question | Answer | Note |
| --- | --- | --- |
| Which platform runs the agents? | Claude Code cloud scheduled tasks; the Claude GitHub Action on the public data repo as runner-up; the Codex action as the best non-Claude POC | [agent platforms compared](2026-11-14-agent-platforms-compared.md), [maintenance agents](2026-11-12-maintenance-agents.md) |
| Can the catalogue agent find new EVs and brands? | Yes: ROVER approvals, BITRE's monthly RAV entries, the Green Vehicle Guide's "newly added" list, The Driven, and makers' sites | [finding new EVs](2026-11-14-new-ev-discovery.md) |
| Can prices be kept per network or per site? | Per network: yes, from fewer sources than planned. Per site: only from drivers' reports, Open Charge Map and (with permission) NRMA | [charging prices per network](2026-11-14-charging-prices-per-network.md) |

## 1. What's decided (14 November)

- **A public `charge-line-data` repo** holds the vehicle catalogue and the charging prices. No code that matters and
  no secrets. The two agents that read the web (catalogue, prices) work only there.
- **The server serves that data to the app**, so a merged change reaches drivers without an App Store release.
- **The app keeps its own copy**, built in and then saved from the server, so it never waits on the network: it uses
  what it has at once and swaps in a newer copy when the server sends one (§2).
- **The catalogue agent also finds EVs new to Australia**, including brands that have just arrived, not only changes
  to brands already listed.
- **Prices:** the typical-price rule stays unless the research shows per-network or per-site prices can be kept
  current reliably and within each network's terms.
- **Server logs:** better logging first, as its own task. The log agent comes after, once there's something to read.
- **Every option gets a proof of concept**, kept in the public POCs repo.
- **Research and POCs are public**, with nothing sensitive in them (§6).

## 2. The data repo, and how the data reaches the app

### The repo: `charge-line-data` (public)

```
vehicles.json        the catalogue: the same fields as today's Vehicles.json, plus per-field sources
prices.json          typical A$/kWh per network (and per site where allowed), each with its source and date
schema/              JSON Schema for both files
scripts/validate.mjs checks both files: shape, sane ranges, unique and kept IDs, sources present
.github/workflows/   runs the validator on every pull request (free: the repo is public)
agents/              each agent's instructions, changed only by pull request
LICENSE              ODbL, like the charger file (to be confirmed by the discovery note's licensing section)
```

- **Branch protection on `main`** (free on a public repo): pull request required, the validator must pass, and no
  bypass. No agent can change `main` without the owner merging.
- Every entry keeps its `source`. A `checked` date per entry lets the agent visit the stalest first.
- A `schemaVersion` at the top. The app ignores a file with a schema newer than it understands, so a change to the
  shape can never break an older app.

### The server

- Every few hours (or on a GitHub webhook) it fetches `vehicles.json` and `prices.json` from the repo's `main`
  branch, validates them with the same rules, and keeps the last good copy. A bad file is refused and the last good
  one stays.
- It serves them as `GET /v1/vehicles/au` and `GET /v1/prices/au`, public like `/v1/chargers/au`, with an `ETag`, so
  an unchanged file costs a `304`. This is the pattern the charger file already uses (`server/src/app.ts`).
- Cost: two small files, a few kilobytes each, fetched by each phone at most once a day. Negligible at 2,000, 10,000
  and 50,000 users.

### The app

- **The built-in copy stays.** Each App Store build includes the files as they were at build time, so a new install
  plans at once, offline too.
- **A saved copy.** At launch, the app uses the newer of the built-in and the saved copy, by the file's
  `builtAt`. In the background (at most once a day) it asks the server with its `ETag`; on a new file it checks it,
  saves it in Application Support and uses it from then on. If the server is slow or down, nothing waits and nothing
  changes. This is how `ChargerDatabase` already handles the charger file.
- **IDs never change.** A driver's saved car is found by its `id`, so the agent may add cars and mark old ones with
  `untilYear`, but never rename or delete an `id` (the validator enforces it against `main`).

## 3. Catalogue agent: finding new EVs as well

Details and sources in [finding new EVs](2026-11-14-new-ev-discovery.md).

- **Monthly, after BITRE's monthly release.** It reads, in order:
  1. ROVER's published list of vehicle type approvals: the earliest signal, often weeks before orders open. It loads
     by JavaScript, so the agent needs the browser.
  2. BITRE's monthly spreadsheet of vehicles entered on the Register of Approved Vehicles, by make and model and by
     motive power per make: the best machine-readable government source.
  3. The Green Vehicle Guide's "newly added" page: the official WLTP range and Wh/km, but makers upload voluntarily,
     so some makes are missing.
  4. The Driven's RSS feed and its monthly EV sales by brand: the one news site whose terms allow automated reading.
     robots.txt asks for 10 seconds between requests.
  5. The makers' Australian sites, for specs.
- **It may not read:** CarExpert (news included), CarsGuide, Chasing Cars, WhichCar, Drive, ANCAP, EV Central, EVDB
  Australia. Their terms or robots.txt forbid automated reading. This list goes in `agents/catalogue.md`.
- **New brands and models** go first to a `seen.json` list of candidates, with where and when each was seen. A car
  joins the catalogue only with an Australian price or "available now" from the maker, so announcements don't become
  cars. Non-EVs (for example Forthing's hybrids) and overseas specs are filtered out.
- **Data shape:** today's fields, plus `sources` per field, the Green Vehicle Guide's figures where listed,
  `firstSeen`, `onSaleFrom` and `checked`.
- **Licence:** ODbL 1.0, as for the charger file. Bare facts aren't protected by Australian copyright and there is no
  database right; the real risk is a site's terms, which the do-not-read list handles (the note's reading, not legal
  advice).
- **The first run has work waiting:** the Deepal E07, Xpeng X9, Leapmotor B05 and MG U9 EV (on sale), Chery's EV,
  and HQ (Hongqi) and Avatr as candidates for 2027.

## 4. Price agent: per network or per site

Details and sources in [charging prices per network](2026-11-14-charging-prices-per-network.md).

- **Per-site prices from the networks: not possible.**
  - Every network shows a site's price only in its app, and none publishes a feed.
  - Chargefox's terms forbid robots, and that covers every site it runs (RAC, Tasmania's Electric Highway,
    Queensland's Super Highway, 7-Eleven). So do Jolt's and Exploren's.
  - tesla.com and bp pulse's site blocked the automated reader.
  - Evie and Ampol publish no prices on their websites.
  - Google Places has no price field. The state charger datasets have none. Roaming tariffs (OCPI) are for partners
    only.
- **NRMA is the exception:** a public table of 85 site prices, but its terms forbid reproducing it. Email NRMA for
  permission (the outreach drafts already ask NRMA about data).
- **Per-site prices that are possible:**
  - **drivers' reports:** already in the app since build 10 ("Drivers paid 69c/kWh");
  - **Open Charge Map listings:** CC BY, used already;
  - **NRMA's table,** with permission.
  - Together, about 15% of fast sites today (the note's estimate), growing with users.
- **The typical price per network stays**, kept current more narrowly than planned:
  - **No LLM agent needed for the drivers' share.** A weekly job on the server computes each network's median from
    the last 90 days of drivers' reports and opens a pull request when it moves past the rule's threshold.
  - **The LLM agent handles the rest each month:** allowed published sources (NRMA with permission, network
    announcements on allowed sites, Open Charge Map). It opens a pull request when an allowed source supports a
    change. Otherwise it opens an issue for the owner to check in the network's app.
### New chargers and new networks (added after the owner's decision)

- **New charger sites need no agent.** The server rebuilds the charger file every day from OpenStreetMap and Open
  Charge Map, so a new site appears in the app within a day of being mapped.
- **New networks do need one.** Today the app knows seven networks by name (a Swift `enum`). Any other operator is
  "Other network", at a typical A$0.65.
  - The price data becomes a list of networks, each with an id, a display name, the operator names it appears under
    in OpenStreetMap and Open Charge Map, a typical price (or none yet), the source and the date checked.
  - The app reads that list. A new network then shows its own name and price without an App Store release. The seven
    built-in networks keep their special handling (Tesla's prices and stalls, live status).
- **How the price agent finds them** each month:
  1. It reads the public charger file (`/v1/chargers/au`, ODbL, no key needed) and counts fast sites by operator.
  2. Any operator with three or more fast sites that matches no network in the list is a candidate.
  3. It looks the network up from allowed sources only: the network's own site if its terms allow it, Open Charge
     Map, and The Driven. It records the name, what it charges if that's published, and whether its terms forbid
     automated reading.
  4. It opens a pull request adding the network: with a price when an allowed source gives one, otherwise with no
     price and an issue for the owner to check the network's app.
- **Cost:** one download of a public file plus a few page reads a month. A$0 extra.

- **Worth checking by hand now:** a CarsGuide survey of Sydney at peak time (15 July 2026) found Evie at $0.70–0.75
  (we use 0.69), bp pulse at $0.66–0.79 (0.65) and Tesla at $0.79 at 300 kW+ (0.55 and 0.65). Sydney at peak is the
  dear end, but it's worth a look in the apps.

## 5. Server logs: first the logging, then the agent

A separate task, done before any log agent:

- One structured line per event (JSON): time, level, route pattern, status, duration, an error ID, and for every 5xx
  the error's class, message and stack trace.
- Upstream failures (Tesla, Open Charge Map, Overpass, MET Norway) logged with the upstream's name and status, so the
  agent can tell our bugs from their outages.
- No personal data in logs: no coordinates, VINs, tokens or full URLs with query strings.
- A daily summary line (requests, 4xx, 5xx, upstream failures) so a quiet day reads as one line.
- Then the log agent (design in the [maintenance agents](2026-11-12-maintenance-agents.md) note §4.3): a read-only Fly
  token, and a pull request or an issue for each new error.

## 6. Publishing: what's public and what stays private

| Folder | Public repo | What stays out |
| --- | --- | --- |
| `POCs/` | yes (name to be chosen) | `.env`, `.tesla/`, `node_modules`; the old `poc/` history (kept privately in `.archive/`) |
| `research/` | `research-charge-line` | two private files (deployment notes, unsent email drafts); the earlier history (kept privately) |
| `charge-line-data` | yes (new) | nothing secret to begin with |
| `app/`, `server/` | stay private | — |

Checked on 14 November before publishing: no keys or tokens in any file or commit; the only VINs are Tesla's
documented placeholders (`5YJ3E1EA0PF000001`, `5YJS0000000000000`); the only private keys are Tesla's published
protocol test keys (their public halves don't match the real key); the only email in the content is the public
support address. The owner's name and personal email appear as commit author, as they already do in the public
website repo.

Test data in the private app and server repos now uses made-up values only (Tesla's example VIN, another town).

## 7. A proof of concept for every option

### The same small job for every platform

To compare them fairly, every POC does one job: the catalogue agent's discovery step, cut down to size. Its source
allows automated reading, and today it should find something.

> In a sandbox repo (`charge-line-agents-sandbox`, a copy of `charge-line-data` with a small `vehicles.json` and an
> empty `seen.json`), read The Driven's RSS feed and its latest monthly EV sales by brand article, waiting 10 seconds
> between requests as its robots.txt asks. List the EV makes and models sold or launched in Australia that aren't in
> `vehicles.json` or `seen.json`. Add them to `seen.json` with the link and the sentence quoted, run
> `scripts/validate.mjs`, and open one pull request assigned to the owner. If there is nothing new, open nothing.

- **Why this job:** the price job planned first would have read Evie's and Jolt's sites. Jolt's terms forbid that,
  and Evie has no prices online. The Driven allows it, and Chery, the Deepal E07 and others should show up on the
  first run, so every platform has a real pull request to make.
- **Runs:** once by hand, then on its schedule daily for a week. After the first pull request is merged, a quiet run
  should open nothing. That checks the "no change, no PR" rule.
- **Recorded for each:**
  - setup time;
  - runs that worked;
  - pull request quality (right cars, links and quotes, nothing outside `seen.json`);
  - whether it read the live page (not a search snippet);
  - cost per run, and where that's shown;
  - how secrets were held (none are needed, except where a platform needs an API key);
  - how easy the transcript is to read.
- Each POC is a folder in the public POCs repo with its setup files (task prompt, workflow or agent config) and a
  `RESULTS.md`.

### The options, cheapest first

| # | Option | POC? | Needs | Cost of the POC | Setup |
| --- | --- | --- | --- | --- | --- |
| 1 | **Claude Code cloud scheduled tasks** | Yes | Claude GitHub App on the sandbox; a cloud environment allow-listing thedriven.io | A$0 (plan usage) | 30–60 min |
| 2 | **Claude Code GitHub Action** on a schedule | Yes | `claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN` secret; a workflow, with the two-job pattern (read-only agent job, separate PR job) | A$0 (plan; Actions free on a public repo) | 1 hour |
| 3 | **Claude Cowork** | Partly | A Cowork scheduled task that reads the same sources and sends a monthly briefing | A$0 (plan) | 15 min |
| 4 | **OpenAI Codex action** on a schedule | Yes | OpenAI API key with prepaid credit; `openai/codex-action` with web search; two jobs | Cents per run (estimate) + OpenAI's minimum top-up (not verified) | 1–2 hours |
| 5 | **GitHub Agentic Workflows** (Claude engine) | Yes | `gh aw`; an Anthropic API key with credit; safe outputs for the PR | Cents per run (estimate) | 1–2 hours |
| 6 | **Claude Managed Agents** | Yes | API key with credit; a scheduled deployment with a dollar budget; a fine-grained token for the sandbox | Cents per run; covered by a Max plan's monthly API credit, not by Pro | 1–2 hours |
| 7 | **Kiro** (Amazon) | Yes | Kiro Pro; the first month is free plus 500 trial credits | A$0 in the trial | 30–60 min |
| 8 | **Warp Oz** | Yes | Warp; the free plan may cover it (not verified) | A$0–US$20 | 1 hour |
| 9 | **Google Gemini CLI action** | Maybe | AI Studio key; Gemini CLI is now API-key only | A$0 if a free key still works (not verified) | 1–2 hours |
| 10 | **GitHub Copilot automations** | Yes, private sandbox | Copilot Pro US$10 a month (trial not verified); a **private** sandbox | US$10 | 30–60 min |
| 11 | **Devin** | Yes | Devin Pro | US$20 | 30–60 min |
| 12 | **Cursor** | Yes | Cursor Premium (Free and Plus exclude automations) | US$30 | 30–60 min |
| 13 | **Google Antigravity** | Later | Google AI Pro US$20; cloud agents launched 9 Nov 2026; Australian availability not verified | US$20 | — |
| 14 | **Sentry Seer** | Later, with the log agent | Sentry Team US$29 + Seer; only once the server logs errors properly (§5) | US$29+ | — |
| — | **Claude Duet** | No | US-only waitlist, no GitHub; re-check when it reaches Australia | — | — |

Running 1–9 costs a few dollars at most. Adding 10–12 for one month costs about US$60.

## 8. Decisions for the owner

1. **Go ahead with `charge-line-data`?** Two files, a schema, a validator, a workflow on pull requests and branch
   protection, ODbL licence; then the server endpoints and the app's built-in plus saved copy (§2).
2. **The sandbox and the POCs:** start with options 1–3 (free on your plan), then 4–9 (cents each)? Options 10–12
   cost US$10–30 each for a month; worth it, or skip?
3. **API credit for options 4–6:** are you on Claude Pro or Max? Max includes US$100 a month of API credit, which
   covers Managed Agents and Agentic Workflows. Pro doesn't, and options 4–6 would need a few dollars of credit.
4. **NRMA:** email asking permission to use its published price table (the outreach drafts already ask NRMA about
   data).
5. **Prices to check now in the apps:** Evie, bp pulse and Tesla in Sydney at peak (§4).
6. **The catalogue's first update:** the Deepal E07, Xpeng X9, Leapmotor B05, MG U9 EV and Chery's EV could go in
   now by hand, or wait for the agent's first run as its test.
7. **The POCs repo's name:** `charge-line-pocs` suggested.
