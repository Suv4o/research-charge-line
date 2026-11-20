# Research

Investigation notes for [Charge Line](https://chargeline.au), an iPhone app that plans EV road trips across
Australia. Each note answers one question against
primary sources (official docs, source code, specs, first-party APIs) and cites
every claim.

## Convention

- One question per file, in `notes/`.
- Filename: `YYYY-MM-DD-short-kebab-slug.md` — the date is when the research was
  done, not when it was last touched. Vendor APIs move; the date is how you know
  whether to re-check.
- Every note opens with a **Bottom line up front** section and closes with
  **Open questions** and a numbered **Sources** list.
- Claims that rest on community reports rather than primary sources are labelled
  as such inline.
- When a note's claims are later tested for real (a POC on a real device, say),
  put a **Field results** section above the Bottom line and add a dated note
  wherever a section is affected. Keep the original text: it records what we
  believed before testing.
- Add a row to the index below when you add a note.

## Index

| Date | Note | Question |
| --- | --- | --- |
| 2026-09-21 | [Tesla: sending a planned route to the vehicle](notes/2026-09-21-tesla-send-route-to-vehicle.md) | Can we push a planned multi-stop trip, including third-party chargers, into a Tesla's own navigation? |
| 2026-10-13 | [Trip planner data: chargers, routing, vehicles, energy and planning](notes/2026-10-13-trip-planner-data.md) | Where should the planner get Australian chargers, routes, vehicles and energy figures? |
| 2026-10-22 | [Australian EV catalogue: cars, figures and estimates](notes/2026-10-22-australian-ev-catalog.md) | Which EVs are on sale in Australia, and how are their figures sourced? |
| 2026-10-23 | [A cheaper charger search: Open Charge Map first](notes/2026-10-23-cheaper-charger-search.md) | Can Open Charge Map replace most paid charger searches? |
| 2026-10-27 | [Charging prices: where they can come from](notes/2026-10-27-charging-prices.md) | Where can a trip's charging cost come from? |
| 2026-10-29 | [Cutting Google costs: how ABRP does it, and a plan](notes/2026-10-29-cutting-google-costs.md) | How do we keep Google's bill small as users grow? |
| 2026-10-29 | [Free charger data: gaps, Google for the gaps, live availability](notes/2026-10-29-free-data-gaps-and-live-availability.md) | How much do free sources miss, and where does live availability come from? |
| 2026-10-30 | [Our own routing and address search](notes/2026-10-30-own-routing-and-search.md) | Can self-hosted routing and search replace Google's, and when does it pay? |
| 2026-11-01 | [TomTom live availability](notes/2026-11-01-tomtom-live-availability.md) | Does TomTom fill the Tesla and NRMA gap in live status? |
| 2026-11-02 | [Charger details like ABRP's, cheaply](notes/2026-11-02-charger-details-like-abrp.md) | Photos, payment, prices and "last successful charge" at low cost? |
| 2026-11-03 | [Can Charge Line use PlugShare's chargers?](notes/2026-11-03-plugshare-api.md) | Is PlugShare's data available to us? |
| 2026-11-03 | [Weather for Premium](notes/2026-11-03-weather.md) | Which weather source, at what cost, and where does it go? |
| 2026-11-12 | [Maintenance agents: what should run them](notes/2026-11-12-maintenance-agents.md) | Which tooling runs the catalogue, price and server-log agents? |
| 2026-11-14 | [Agent platforms compared](notes/2026-11-14-agent-platforms-compared.md) | What do OpenAI, Google, GitHub and others offer for the same three agents? |
| 2026-11-14 | [Charging prices per network and per site](notes/2026-11-14-charging-prices-per-network.md) | Can prices be kept current per network, or per site? |
| 2026-11-14 | [New EV discovery](notes/2026-11-14-new-ev-discovery.md) | How does the catalogue agent find cars and brands new to Australia? |
| 2026-11-14 | [Maintenance agents: the plan](notes/2026-11-14-maintenance-agents-plan.md) | The data repo, how data reaches the app, and a POC for every option |
| 2026-11-15 | [Maintenance agents on GitHub Agentic Workflows](notes/2026-11-15-github-agentic-workflows.md) | How do the agents run as gh-aw workflows with Claude, and what does it cost? Built and live 20 November: results, measured costs, lessons (§7) |

## Related

- Proofs of concept that test these notes: [charge-line-pocs](https://github.com/Suv4o/charge-line-pocs).
