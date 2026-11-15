# Maintenance Agents on GitHub Agentic Workflows, with Claude

**Date:** 2026-11-15
**For:** the owner, who moved the maintenance agents from Claude Code's cloud scheduled tasks to GitHub Agentic
Workflows on 15 November. They are also meant as a worked example for showing others how agentic workflows run.
This note covers what gh-aw is in November 2026, how Claude plugs into it, what it costs, and the plan rebuilt
around it. The data design (the public `charge-line-data` repo, the server, the app's built-in plus saved copy) is
unchanged from [the plan](2026-11-14-maintenance-agents-plan.md) §2–§5.

Read from gh-aw's own documentation (the `docs/` folder of [github/gh-aw](https://github.com/github/gh-aw) at
v1.2.x, 15 November), GitHub's changelog, GitHub's Copilot plans page and Anthropic's docs. Costs are estimates
until the first runs are measured.

## Bottom line

- **gh-aw is generally available since 28 October 2026**, on GitHub Free, Team and Enterprise. It was a technical
  preview in February, when the owner's
  [article](https://www.trpkovski.com/2026/02/22/agentic-workflows-write-github-actions-in-markdown) was written.
- **Claude is a full engine (`engine: claude`), no longer marked experimental.** It runs Claude Code inside the
  workflow's sandbox.
- **A Claude subscription can't pay for it.** gh-aw ignores `CLAUDE_CODE_OAUTH_TOKEN`; Pro and Max don't apply.
  Claude is billed one of three ways:
  - an Anthropic API key;
  - Anthropic **Workload Identity Federation** (no stored key at all; recommended here);
  - Claude models through a GitHub Copilot plan.
- **Cost: about US$6 a month (about A$9) with Claude Sonnet 5.5** for both agents (estimate), plus A$0 of Actions
  time because `charge-line-data` is public. Haiku 5.5 would be about US$1.50, Opus 5.5 about US$11. Hard caps per
  run and per day are built in.
- **Why it's worth the API bill over the cloud tasks:**
  - **The agent can't write.** It runs read-only. Its pull request is built by a separate job, only from files it is
    allowed to touch, after a second check for anything suspicious.
  - **The do-not-read list becomes a firewall rule.** Only listed sites are reachable, so the agent can't open
    CarExpert even if a page tells it to.
  - **Runs no longer share the owner's Pro usage limits.**
  - **Everything lives in the repo as Markdown,** which is what makes it a good showcase.
- **Next:** build `charge-line-data` with the two workflows, run them once in staged mode (nothing is written), then
  for real (§6).

## 1. What gh-aw is now, and what changed since February

**The model:**
- **A workflow is a Markdown file** in `.github/workflows/`: YAML frontmatter (triggers, permissions, engine, tools,
  network, safe outputs) and a body of plain instructions.
- **`gh aw compile` turns it into a `.lock.yml`** that Actions runs. Both files are committed. Edits to the body
  alone need no recompile.
- **The agent job is read-only.** Every write (a pull request, an issue, a comment) is a "safe output": the agent
  asks, and a separate job with write permission does it, after checks.
- **gh-aw is complementary to ordinary Actions.** Its own docs put it this way: keep builds, tests and deterministic
  scripts as normal workflows, and use an agentic workflow where a task needs reasoning or judgement.

**What's new since the article (February):**

| Then (technical preview) | Now (GA, v1.2.x) |
| --- | --- |
| Claude and Codex "experimental", Copilot the stable one | Claude Code, Codex, Pi and Copilot listed as engines. Agy is experimental; Gemini is deprecated. |
| Claude needs `ANTHROPIC_API_KEY` | Also keyless: Anthropic WIF (since 11 June). Also Claude models billed through Copilot. |
| Copilot needs a personal access token | In an organisation: `permissions: copilot-requests: write`, no token. A personal repo still needs the token. |
| No spending controls | `max-ai-credits` per run (default 1,000 = US$10) and `max-daily-ai-credits` (default 5,000), on every engine. Also `max-turns`, timeouts, `gh aw forecast`, `gh aw audit`. |
| `network: defaults` plus domains | Same firewall, plus a separate `hosted-web` list for Claude's and Codex's provider-hosted search and fetch. |
| Schedules as cron or `daily` | Fuzzy schedules (`weekly on monday around 09:00`), `utc+N` offsets, and a `timezone` field on cron lines. |

**Releases and upkeep:**
- **gh-aw releases weekly or fortnightly.** Lock files embed the compiler version, and the project can revoke a
  version (`blockedVersions`) or set a minimum. An old lock file can start failing until it's recompiled.
- **So `gh aw upgrade` plus `gh aw compile` becomes a regular chore.** `gh aw compile --dependabot` can let
  Dependabot watch the pinned tools.

## 2. How Claude plugs in

| Route | Set up | Billed | Web search and fetch | Fit |
| --- | --- | --- | --- | --- |
| **Anthropic WIF** (keyless) | A federation rule in the Claude Console that trusts only this repo's `main` branch; the IDs go in `engine.auth`; `id-token: write` | Anthropic API, pay as you go | Anthropic-hosted, limited by `network.hosted-web` | **Recommended.** No secret to leak or rotate, and a good thing to show. |
| **`ANTHROPIC_API_KEY`** | A key from the Console, saved as an Actions secret (`gh aw secrets set`) | Anthropic API | Same | The fallback if WIF gives trouble. |
| **Claude via Copilot** | `model: copilot/claude-sonnet-5.5`; a `COPILOT_GITHUB_TOKEN` personal token (personal repo) | Copilot AI credits | **None built in:** the compiler rejects them on this route, so an MCP fetch server and a search service (for example Tavily) are needed | Not for us: Copilot Pro is a flat US$10, more than the API at our volume, and more parts. Worth knowing for teams on Copilot Business: the same workflow switches by changing two lines. |
| Claude Pro/Max subscription | n/a | n/a | n/a | **Not supported:** "Subscription OAuth tokens are unsupported." |

**Notes on the routes:**
- **WIF works for an ordinary Console organisation.** It needs permission to create service accounts, issuers and
  rules, which an organisation's owner has.
  - **Scope the rule tightly:** `subject_prefix` `repo:Suv4o/charge-line-data:ref:refs/heads/main`, plus
    `repository_owner` and `ref` claims. Scheduled and manual runs on `main` match; pull-request runs and forks
    can't.
  - **Tokens are short-lived:** the Anthropic token is minted per run (lifetime set on the rule, for example 10
    minutes).
- **Copilot Free can't run Claude.** It has auto model selection only. Copilot Pro (US$10) includes Haiku 5.5 and
  Sonnet 5.5; Opus 5.5 needs Pro+ (US$39).
- **Model choice:**
  - Anthropic ids on the API route (`claude-sonnet-5-5`); dotted ids on Copilot (`claude-sonnet-5.5`). gh-aw maps
    between them.
  - Bare `auto` on the Anthropic route means Claude Code's `sonnet` alias.
  - The threat-detection pass uses the workflow's engine unless configured otherwise.

## 3. The guard rails, applied to Charge Line

| Risk | What gh-aw does | Our setting |
| --- | --- | --- |
| A web page tells the agent to do something else (prompt injection) | The agent job has no write permission. Threat detection reads the proposed output and patch before anything is written. | Defaults on. Human review before merge. |
| The agent edits files it shouldn't | `create-pull-request.allowed-files` is an exclusive list: any other file in the patch is refused. Protected by default: everything under `.github/` (the workflows included), package manifests, `README.md` and agent instruction files. | Catalogue: `vehicles.json` only. Prices: `networks.json` / `prices.json` only. |
| The agent reads sites whose terms forbid it | The firewall (AWF) allows only listed domains for anything the agent fetches itself. Claude's hosted search and fetch obey `network.hosted-web` (an `allowed` or a `blocked` list, plus `max-uses`). | Allow-lists built from the sources each agent may read. The do-not-read list is enforced, not just asked for. |
| A runaway run | `max-turns`, `timeout-minutes` (20 by default), `max-ai-credits` per run, `max-daily-ai-credits` per workflow. | For example 60 turns, 300 credits (US$3) per run, 600 a day. Plus a spend limit on the Anthropic workspace. |
| Pull requests merged without checks | Branch protection on `main` (free on a public repo): pull request required, validator required. | Required check `validate`. |
| The agent's pull request doesn't start the checks | Pull requests made with the default `GITHUB_TOKEN` don't trigger other workflows (a GitHub rule). gh-aw pushes an empty commit with a token you provide (`GH_AW_CI_TRIGGER_TOKEN`) to start them. | A fine-grained token: Contents read/write on `charge-line-data` only. |
| Review requests | The pull request comes from `github-actions[bot]`, so the owner can be a real requested reviewer (the cloud tasks opened pull requests as the owner). | `reviewers: [Suv4o]`, `labels: [agent]`. |

**Gotcha:** GitHub turns off scheduled workflows in a public repo after 60 days with no repository activity. It
emails first. Merged agent pull requests count as activity. If the data goes quiet for two months, a run may need
re-enabling.

## 4. What it costs

**GitHub Actions:**
- Free on a public repo.
- Each run is a short pre-activation job, the agent job (1–15 minutes) and the detection job, each with about 1.5
  minutes of runner setup.
- The future log agent, in the private server repo, comes out of GitHub Free's 2,000 minutes a month: about 5
  minutes a run, so even daily runs (about 150 minutes) fit.

**Claude inference.** Rough figures per run, not yet measured:
- **Assumed run:** about 40 turns, context growing from about 30,000 to about 120,000 tokens, mostly cache reads,
  about 30,000 output tokens, about 20 hosted web searches.
- **Prices:** web search is US$10 per 1,000 searches; web fetch is billed as tokens only.
- **Detection:** the threat-detection pass is small, about US$0.05 on Sonnet.
- **Runs per month:** about 4.3 catalogue runs plus 1 price run.

| Model (input/output per million tokens) | Per run | Per month |
| --- | ---: | ---: |
| Haiku 5.5 (US$0.10/US$0.50) | ~US$0.25 (mostly web searches) | **~US$1.50** |
| **Sonnet 5.5 (US$2/US$10)** | ~US$1 | **~US$6 (~A$9)** |
| Opus 5.5 (US$4/US$20) | ~US$2 | **~US$11** |

- **Users don't change it.** The agents' cost is the same at 2,000, 10,000 or 50,000 users. Serving the two small
  data files stays negligible (the plan §2).
- **First runs set the real number.** `gh aw audit <run>` gives tokens and AI credits for a run; `gh aw logs` and
  `gh aw forecast` give monthly ranges. The per-run cap is then set just above the measured cost.
- **Against the cloud tasks:**
  - **The cloud tasks cost A$0 extra,** but share the owner's Pro limits and have softer guard rails.
  - **A Copilot plan is a flat US$10–39** and lacks Claude's hosted web tools.

## 5. The plan, rebuilt on gh-aw

### `charge-line-data` (public)

```
vehicles.json                    the catalogue (from the app's Vehicles.json, plus sources, checked dates)
networks.json                    networks: id, name, OSM/OCM operator aliases, typical A$/kWh, source, checked
schema/                          JSON Schema for both
scripts/validate.mjs             shape, ranges, unique and kept IDs, sources present (also checks IDs against main)
.github/workflows/
  validate.yml                   ordinary Actions: runs the validator on every pull request (required check)
  catalogue.md + .lock.yml       agentic: weekly, a quarter of the brands plus the new-EV sweep
  prices.md + .lock.yml          agentic: monthly, typical prices plus new networks
  shared/sources.md              imported by both: allowed sources, the do-not-read list, the rules
.gitattributes                   lock files marked generated (gh-aw writes it)
LICENSE                          ODbL 1.0
```

**Changes from the 14 November design:**
- **`agents/*.md` goes away:** the workflow bodies are the agents' instructions, and changes still go through review.
- **`seen.json` becomes repo-memory.** Candidates the agent has seen but not added (with link, date and quote) live
  on a `memory/catalogue` branch that gh-aw commits after each run. Only real catalogue changes reach `main` by pull
  request. If the owner prefers the candidates visible in review, `seen.json` can stay in `main` and in
  `allowed-files`.

### The catalogue workflow (sketch, to be checked against the compiler)

```aw
---
on:
  schedule: weekly on monday around 03:00 utc+11
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
  id-token: write                       # for Anthropic WIF
engine:
  id: claude
  model: claude-sonnet-5-5
  auth:
    type: github-oidc
    provider: anthropic
    federation-rule-id: fdrl_…          # identifiers, not secrets; the rule trusts only this repo's main
    organization-id: org_…
    service-account-id: svac_…
    workspace-id: ws_…
max-turns: 60
max-ai-credits: 300
max-daily-ai-credits: 600
imports:
  - shared/sources.md
tools:
  web-search:
  web-fetch:
  playwright:                           # ROVER's approvals list needs a browser
  repo-memory: true
network:
  allowed: [defaults, bitre.gov.au, infrastructure.gov.au, greenvehicleguide.gov.au, thedriven.io]
  hosted-web:
    allowed: [thedriven.io, greenvehicleguide.gov.au, bitre.gov.au, infrastructure.gov.au]   # plus makers' AU sites
    max-uses: 30
safe-outputs:
  create-pull-request:
    title-prefix: "[catalogue] "
    labels: [agent, catalogue]
    reviewers: [Suv4o]
    allowed-files: [vehicles.json]
    if-no-changes: ignore
  create-issue:
    title-prefix: "[catalogue] "
    labels: [agent]
    max: 2
---

# Keep the EV catalogue current
(the rules from the plan §3: this week's quarter of the brands, then the new-EV sweep in source order;
a car joins only with an Australian price or "available now" from the maker; never rename or delete an id;
run `node scripts/validate.mjs` before proposing the change; nothing new means no pull request)
```

**The prices workflow:**
- **Same shape:** a monthly cron with `timezone: Australia/Melbourne`; `allowed-files` for the network file only;
  hosted web limited to the allowed price sources.
- **New networks:** a step before the agent downloads the public charger file (`/v1/chargers/au`). The agent
  counts fast sites by operator and proposes any operator with three or more that isn't in the list (the plan §4).
- **Deterministic first, agent second:** downloads and counting run as ordinary steps (gh-aw's `steps:`), so the
  agent spends tokens only on judgement.

### The order of work

1. **Build `charge-line-data` locally:**
   - data, schema, validator, `validate.yml`;
   - the two workflows, compiled with `gh aw compile`.

   Scan for sensitive data. Create the public repo after the owner's OK.
2. **The owner's setup** (about 20 minutes):
   - **Install gh-aw:** `gh extension install github/gh-aw`.
   - **Anthropic Console:**
     - a workspace for the agents, with a monthly spend limit (for example US$15);
     - prepaid credit (for example US$10);
     - a WIF rule from the GitHub Actions wizard, or an API key as the fallback.
   - **GitHub:** a fine-grained token for `GH_AW_CI_TRIGGER_TOKEN` (Contents read/write, this repo only).
   - **Branch protection on `main`,** with `validate` required.
3. **First runs, safely:**
   - **Staged:** run each workflow once (Actions tab or `gh aw run`) with `staged: true` under `safe-outputs`. Safe
     outputs are previewed in the run summary and nothing is written.
   - **Live:** if the previews are good, switch staged off and run again. The first live catalogue run should
     propose the four missing cars and Chery, and record HQ and Avatr as candidates.
   - **Measure:** read `gh aw audit` and set the per-run caps from the measured cost.
4. **Server:** serve `/v1/vehicles/au` and `/v1/prices/au` from `main` with an `ETag` (the plan §2). The owner
   deploys.
5. **App:** built-in plus saved copy, networks from the data. TestFlight first.
6. **Later, the log agent in the private `charge-line-server` repo:**
   - first the logging task (the plan §5);
   - then a daily or weekly workflow. A custom job, outside the agent's sandbox, fetches the logs with a read-only
     Fly token and hands them over as an artifact, so the agent never holds the token;
   - its outputs: an issue per new error, or a draft pull request limited by `allowed-files` to source and tests.
7. **The article:** how Charge Line keeps its own data current with GitHub Agentic Workflows and Claude.

### What carries over unchanged

- **The public data repo** and the server/app design (the plan §2).
- **The catalogue's sources and do-not-read list** (§3 and [finding new EVs](2026-11-14-new-ev-discovery.md)).
- **The price rule, drivers' report medians and new-network detection** (§4).
- **The logging-first order for the log agent** (§5).

Dropped: the Claude GitHub App on the data repo, the cloud environment, and the `/schedule` tasks. None had been
created.

## 6. Open points

- **The workflow sketch is unverified.** It follows the docs but hasn't been compiled. `gh aw compile` will say what
  it rejects. Points to check:
  - whether `engine.auth` accepts repository variables (`${{ vars.… }}`) instead of literal IDs;
  - Playwright's domain rules;
  - the exact `utc+11` wording, given Melbourne's daylight saving.
- **WIF identifiers in a public repo.** They aren't credentials: a token is issued only to runs GitHub signs for this
  repo's `main`. Keeping them in variables is tidier if the compiler allows it.
- **Costs are estimates** until the first audited runs.
- **gh-aw moves fast:** weekly releases, occasional breaking changes (v1.2.0 had two). Budget a monthly
  `gh aw upgrade`.
- **The owner's article is now out of date in places:**
  - Claude is no longer experimental;
  - organisations need no Copilot token;
  - WIF, `hosted-web`, budgets and fuzzy schedules are new.

  The new article can point to the old one and say what changed.

## Sources

- gh-aw docs, read from [github/gh-aw](https://github.com/github/gh-aw) (`docs/src/content/docs/`, 15 November 2026):
  - engine and auth:
    [Claude setup](https://github.github.com/gh-aw/engines/claude/),
    [Claude reference](https://github.github.com/gh-aw/reference/engines/claude/),
    [AI engines](https://github.github.com/gh-aw/reference/engines/),
    [authentication](https://github.github.com/gh-aw/reference/auth/);
  - cost:
    [billing](https://github.github.com/gh-aw/reference/billing/),
    [cost management](https://github.github.com/gh-aw/reference/cost-management/);
  - network and tools:
    [network](https://github.github.com/gh-aw/reference/network/),
    [tools](https://github.github.com/gh-aw/reference/tools/),
    [web search](https://github.github.com/gh-aw/reference/web-search/);
  - pull requests and safety:
    [pull requests](https://github.github.com/gh-aw/reference/safe-outputs-pull-requests/),
    [triggering CI](https://github.github.com/gh-aw/reference/triggering-ci/),
    [threat detection](https://github.github.com/gh-aw/reference/threat-detection/);
  - running:
    [schedule syntax](https://github.github.com/gh-aw/reference/schedule-syntax/),
    [repo memory](https://github.github.com/gh-aw/reference/repo-memory/),
    [custom steps and jobs](https://github.github.com/gh-aw/reference/steps-jobs/),
    [releases](https://github.github.com/gh-aw/reference/releases/),
    [weekly update, 9 November](https://github.github.com/gh-aw/blog/2026-11-09-weekly-update/).
- GitHub changelog:
  - [GitHub Agentic Workflows generally available](https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available) (28 October 2026);
  - [public preview](https://github.blog/changelog/2026-06-11-github-agentic-workflows-is-now-in-public-preview) (11 June 2026);
  - [technical preview](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/) (13 February 2026).
- GitHub Copilot:
  - [individual plans](https://docs.github.com/en/copilot/concepts/billing/individual-plans) (models per plan, AI credits);
  - [usage-based billing](https://github.blog/changelog/2026/04/27/github-copilot-is-moving-to-usage-based-billing/).
- Anthropic:
  - [WIF with GitHub Actions](https://platform.claude.com/docs/en/manage-claude/wif-providers/github-actions);
  - [pricing](https://platform.claude.com/docs/en/about-claude/pricing) (model prices; web search US$10 per 1,000 searches).
- The owner's article: [Agentic Workflows: write GitHub Actions in Markdown](https://www.trpkovski.com/2026/02/22/agentic-workflows-write-github-actions-in-markdown) (22 February 2026).
