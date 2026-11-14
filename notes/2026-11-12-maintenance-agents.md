# Maintenance Agents: What Should Run the Catalogue, Price and Server-Log Agents

**Date:** 2026-11-12
**For:** the user, choosing the tooling for three unattended agents that keep Charge Line maintained through pull requests he reviews: a vehicle catalogue agent, a charging price agent and a server log agent. He named GitHub Agentic Workflows, "Claude Cowork", Claude in the cloud, "Claude Duet" and third-party tools.
**How to read it:** every fact is followed by the page that owns it, read on 12 November 2026. "Not verified" marks what I could not confirm from a primary source. Costs marked "estimate" are my arithmetic from published rates, not measurements.

> **Update, 14 November 2026:** the price agent's sources in §4.2 are narrower than this note assumed: most networks' terms forbid automated reading, or they publish no prices. The catalogue agent also has to find cars new to Australia. See [the plan](2026-11-14-maintenance-agents-plan.md), [charging prices per network](2026-11-14-charging-prices-per-network.md) and [finding new EVs](2026-11-14-new-ev-discovery.md). The text below is kept as it was.

## Bottom line

- **Use Claude Code's cloud scheduled tasks (called "routines" until recently, at claude.ai/code/routines) for all three agents.**
  - **No new bill.** Runs "draw down subscription usage the same way interactive sessions do", and there is "no separate charge for the cloud VM" ([scheduled tasks](https://code.claude.com/docs/en/routines), [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web)).
  - **It has every part the three agents need:** a cron schedule, web search, a fresh clone of a private repo, a pushed branch and pull request, and a full transcript of each run.
  - **Its secrets handling is the best of the cheap options.** GitHub credentials and "network secrets" (the Fly token) stay outside the machine the agent runs in ([cloud environments](https://code.claude.com/docs/en/cloud-environments)).
  - **What to accept:** it is a research preview; pull requests are opened as you, so you are assigned rather than asked to review; and nothing on a free GitHub plan stops the agent's access from pushing to `develop` or `main` (§5).
- **Runner-up: the Claude Code GitHub Action on a `schedule:` cron**, signed in with your subscription (`CLAUDE_CODE_OAUTH_TOKEN`). Same subscription limits, plus Actions time that fits inside GitHub Free's US$12 a month. The pull request comes from the Claude GitHub App, so GitHub can request your review. But the secrets sit in the runner, there is no network allow-list, and each agent is a YAML file to maintain.
- **If you want harder guard rails later:** GitHub Agentic Workflows (the agent is read-only and writes go through checked "safe outputs") or Claude Managed Agents (a dollar cap on every run). Both bill the Claude API and cannot use the subscription. A Max plan's US$100 monthly API credit would cover them; a Pro plan has no such credit.
- **Not a fit:**
  - **Claude Cowork** is for documents and connectors, not repositories. Its scheduler is the same one, and adding a repository makes it a Claude Code task, which is the recommendation.
  - **Claude Duet** is real (announced 21 October 2026), but it is a personal assistant app on a US-only waitlist. It has no repository or pull request features.
  - **Claude Tag** is Claude in Slack for Team and Enterprise plans only.
  - **Copilot automations, Devin, Cursor and Sentry's Seer** each mean a second subscription for work the Claude plan already covers.
- **Do first:** add a small Linux validator for the catalogue and the prices, write the price rule down in the repo, and log stack traces for 5xx on the server. Without those the agents have nothing to check themselves against.
- **Cost:** A$0 on top of the Claude plan. The same three agents on the API would be about US$10–25 a month (estimate, §6).

## 1. What the three agents need

| | Catalogue | Prices | Server logs |
| --- | --- | --- | --- |
| Repo | `charge-line-app` (private), branch `develop` | `charge-line-app`, `develop` | `charge-line-server` (private), `main` |
| Reads | About 50 makers' Australian pages and news coverage | About 10 networks' pricing pages | Fly logs for the last day |
| Changes | `ChargeLine/Resources/Vehicles.json` | Seven numbers in `ChargeLine/Model/ChargingCost.swift` | Server source and tests, or nothing |
| Checks itself with | A validator script (to be written); Swift tests need a Mac | A validator script (to be written) | `npm test`, `npm run typecheck` (run on Linux) |
| Output | Pull request with sources | Pull request with sources | Pull request with a fix, or an issue |
| Secrets | None | None | A read-only Fly token |
| Reaches drivers | Next App Store release | Next App Store release | Next `fly deploy` |

Nothing an agent merges reaches a driver without a step only the owner can take: an App Store release, or a `fly deploy`. The website repo deploys from `main` by itself, so no agent gets it.

## 2. The options compared

| | Fit for the 3 agents | Scheduling | Web research | Private-repo pull requests | Secrets | Billing | Setup | Maturity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **A. Claude Code cloud scheduled tasks** | Good for all three | Presets or cron; 1 hour minimum | Web search built in; other sites need the environment's allow-list or Full access | Claude GitHub App or your `gh` token, through a proxy; opened as you | Network secrets kept outside the VM | Claude subscription | Low: a web form or `/schedule` | Research preview |
| **B. Claude Code GitHub Action** | Good for all three | Actions cron | Web tools once allowed; the runner has open internet | Claude GitHub App; opened by the app | Actions secrets, readable inside the run | Subscription token or API key, plus Actions time | Medium: a workflow per agent | v1 |
| **C1. Agent SDK, self-hosted** | Possible; most work | Your own cron | Yes | A token you manage | Yours to build | Subscription limits or API | High | Released SDK |
| **C2. Claude Managed Agents** | Good for all three | Cron to the minute, with time zone | Search and fetch on Anthropic's servers, with a host allow-list | A fine-grained token you supply, plus GitHub's MCP server | Vaults; swapped in as requests leave | API tokens + US$0.08 per session-hour | Medium to high: API calls | Beta |
| **D. Claude Cowork** | Poor | Yes, runs remotely | Yes | None documented | Connectors | Claude subscription | Low | Released; web and mobile newer |
| **E. Claude Duet** | None | Checks "every few hours" | n/a | None | n/a | Claude subscription; US waitlist | n/a | Research preview |
| **F. GitHub Agentic Workflows** | Good; strongest guard rails | Actions cron or "weekly on monday" | Hosted search and fetch for the Claude engine; firewall allow-list | "Safe outputs" create the pull request, with reviewers and assignees | Actions secrets; the agent job is read-only | Actions time + Anthropic API key or a Copilot plan. No Claude subscription | Medium to high: compile step | Preview (status not verified) |
| **G. Copilot cloud agent + automations** | Good | Automations on a schedule | Behind a firewall allow-list | Native | GitHub's own | Copilot Pro US$10/month: AI credits + Actions time | Low | Released June 2026 |
| **H. Third-party (Devin, Cursor, Codex, Seer)** | Works, at a price | Varies | Varies | Varies | Varies | A second subscription | Low to medium | Varies |

## 3. Each option

### A. Claude Code cloud scheduled tasks (formerly routines): recommended

- **What it is:** "a saved Claude Code configuration: a prompt, one or more repositories, and a set of connectors, packaged once and run automatically" on "Anthropic-managed cloud infrastructure". Status: "Scheduled tasks are in research preview. Behavior, limits, and the API surface may change." ([scheduled tasks](https://code.claude.com/docs/en/routines))
- **Plans:** "available on Pro, Max, Ultra, Team, and Enterprise plans". Created at claude.ai/code/routines, in the Desktop app, or with `/schedule` in the CLI ([scheduled tasks](https://code.claude.com/docs/en/routines)).
- **Triggers:** a schedule, an API call (`POST …/fire` with a per-task token), or a GitHub event (pull request, release, issue). One task can have several ([scheduled tasks](https://code.claude.com/docs/en/routines)).
  - Schedule: presets, or a cron expression. "Expressions that run more often than once per hour are rejected." Five-field cron is read as UTC.
  - A run set exactly on the hour "can start several minutes late"; the docs suggest a time like 9:07.
- **Where it runs:** "a fresh virtual machine (VM) running Ubuntu 24.04 on x86_64" with about 4 vCPUs, 16 GB of memory and 30 GB of disk. Node 20–22, Python, Docker, `gh`, `jq` and Chrome are already installed. No macOS, so no Xcode ([cloud environments](https://code.claude.com/docs/en/cloud-environments)).
- **Web research:**
  - Web search "runs a query against Anthropic's web search backend", so it doesn't depend on the VM's network ([tools reference](https://code.claude.com/docs/en/tools-reference)).
  - Everything else leaving the VM is filtered. The Default environment is "Limited": package registries, GitHub and cloud SDKs only. Other sites return `403` with `x-deny-reason: host_not_allowed` until you list them under Allowed domains, or choose Full ([cloud environments](https://code.claude.com/docs/en/cloud-environments), [errors](https://code.claude.com/docs/en/errors)).
  - **Not verified:** whether the WebFetch tool is held to that allow-list in the same way as `curl`. Assume it is, and list the domains.
- **Private repos:** two ways to connect GitHub ([cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web)):
  - the Claude GitHub App: "private repositories that the Claude GitHub App is installed on";
  - `/web-setup`, which sends your local `gh` token: "any repository your `gh` token can access".
  - Either way, "your GitHub credentials stay encrypted on Anthropic's servers and never enter a session's VM". The proxy "serves GitHub API requests for the repositories attached to the session" and answers 403 for any other.
- **Pull requests:**
  - "Each repository is cloned at the start of a run. Claude creates `claude/`-prefixed branches", starting "from the repository's default branch unless your prompt specifies otherwise" ([scheduled tasks](https://code.claude.com/docs/en/routines)). The app's work is on `develop`, so the prompt must say so.
  - The docs' own examples open pull requests unattended ("opens update PRs against the docs repository for an editor to review").
  - "Commits and pull requests carry your GitHub user." So the author is you. Code owners and review requests are for other people; assign yourself instead (§5).
  - Inside the VM, `gh pr` and `gh issue` fail because the proxy rejects GitHub's GraphQL API. `gh api repos/{owner}/{repo}/...` (REST) works ([cloud environments](https://code.claude.com/docs/en/cloud-environments)). **Not verified:** that an unattended run creates and assigns the pull request this way without a prompt; test with Run now.
  - The proxy "rejects branch deletions and pushes of anything other than a branch", but "doesn't limit which branches a push can update. To do that, use branch protection rules or rulesets on GitHub."
- **Secrets:**
  - Environment variables are plain: "Anyone who uses the environment can read the values", and so can the agent.
  - A **network secret** is "an API key or token you store on a cloud environment so Claude can call that API from any session in the environment without seeing the key". The proxy adds it "after each request leaves the session's VM". Available on Pro and above ([cloud environments](https://code.claude.com/docs/en/cloud-environments)).
- **Approvals when nobody is there:** a run "begins in auto mode", where "a classifier model allows or blocks actions that would otherwise wait for your approval". After repeated blocks "a permission prompt appears in the run's session and waits until someone answers it" ([scheduled tasks](https://code.claude.com/docs/en/routines)). The classifier blocks "anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content Claude read" ([permission modes](https://code.claude.com/docs/en/permission-modes)).
- **Billing and limits:**
  - Subscription usage, shared with everything else you do in Claude: "cloud sessions share rate limits with all other Claude and Claude Code usage within your account" ([cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web)).
  - Past the plan's limit, runs are "rejected until your usage window resets" unless usage credits (paid overage) are turned on ([scheduled tasks](https://code.claude.com/docs/en/routines)). Leave them off to keep the bill fixed.
  - 100 scheduled runs an hour per account: far above three agents.
  - If the GitHub connection expires, the task "skips runs until you reconnect, for up to 72 hours", then turns itself off.
- **Seeing what a run did:** each run "opens as a full session" with the transcript and the diff. A run marked Succeeded only "ended without Claude Code reporting a failure": "open the run and read its transcript". Commits carry a `Claude-Session:` link, and so does the pull request body ([scheduled tasks](https://code.claude.com/docs/en/routines), [cloud environments](https://code.claude.com/docs/en/cloud-environments)).
- **Two neighbours that are not this:** Desktop scheduled tasks and `/loop` run on your Mac and need it on ([comparison](https://code.claude.com/docs/en/scheduled-tasks)). A Desktop task could run the Xcode tests, which the cloud can't.

### B. Claude Code GitHub Action (`anthropics/claude-code-action@v1`): runner-up

- **What it is:** "a GitHub Action that runs Claude Code inside your repository's workflows". With a `prompt` input it "runs in automation mode on any GitHub event, including a cron schedule" ([GitHub Actions](https://code.claude.com/docs/en/github-actions)).
- **Scheduling:** `on: schedule:` cron. "GitHub runs scheduled workflows only from the default branch."
- **Sign-in:** an API key, or `CLAUDE_CODE_OAUTH_TOKEN`, "an OAuth token that authenticates with your Claude subscription, available on Pro, Max, Ultra, Team, and Enterprise plans", made with `claude setup-token` and valid for one year ([authentication](https://code.claude.com/docs/en/authentication)).
- **Billing:** "If you authenticate with an OAuth token, runs use your Claude subscription instead of API billing." Anthropic's help page, updated 7 October 2026: "when you're signed in with your Claude plan, the Claude Agent SDK and `claude -p` still draw from your subscription limits" ([help article](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)). A plan to move this use to a separate credit was "paused" on 15 June 2026; it could return.
- **Plus Actions time:** GitHub Free includes US$12 of compute a month; a Linux minute is US$0.006 and a macOS minute US$0.062 ([Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)). That is 2,000 Linux minutes or about 190 macOS minutes.
- **Tools:** "Claude has no shell or GitHub API access until you grant the tools the prompt needs, with `--allowedTools`". Web search and fetch are ordinary Claude Code tools that can be listed there. `--max-turns` caps a run.
- **Pull requests:** the action "authenticates as the Claude GitHub App" unless you pass a token. Workflow `permissions:` limit what the job can touch. The app-authored pull request can request you as reviewer.
- **Secrets:** GitHub Actions secrets. The subscription token and any Fly token are present on the runner, where a misled agent with a shell could read them. GitHub-hosted runners have no outbound allow-list.
- **Seeing what a run did:** "By default, results appear in the workflow run log."
- **Why second:** same cost, but weaker isolation of secrets and network, a long-lived subscription token stored in GitHub, and three workflows to maintain.

### C1. Claude Agent SDK, self-hosted

- **What it is:** "the same tools, agent loop, and context management that power Claude Code", as `claude -p` or Python and TypeScript packages ([headless](https://code.claude.com/docs/en/headless)).
- **Billing:** subscription limits when signed in with the plan; API rates with a key (same help article as above).
- **Unattended runs:** "Pass `--permission-prompts none` when nobody is available to answer permission prompts, for example in a scheduled job."
- **Fit:** you would build the schedule, sandbox, secrets and GitHub token handling yourself. Options A and B already are this, packaged. Not worth it here.

### C2. Claude Managed Agents

- **What it is:** a "pre-built, configurable agent harness that runs in managed infrastructure". "Claude Managed Agents is in beta." It needs a Claude API key ([overview](https://platform.claude.com/docs/en/managed-agents/overview)).
- **Scheduling:** a scheduled deployment takes "standard POSIX cron" with an IANA time zone, to the minute. Runs start with "jitter of up to 15 percent of the interval between runs, with a minimum of 5 seconds and a maximum of 9 minutes" ([scheduled deployments](https://platform.claude.com/docs/en/managed-agents/scheduled-deployments)).
- **Cost cap:** a budget on the deployment "bounds every run separately"; a session at its cap "pauses" with `budget_reached` ([budgets](https://platform.claude.com/docs/en/managed-agents/budgets)). No other option has a hard dollar cap per run.
- **Web:** search and fetch "run on Anthropic's servers"; with `limited` networking the `allowed_hosts` list applies to them too ([environments](https://platform.claude.com/docs/en/managed-agents/environments)).
- **GitHub:** you mount the repository with a token you supply and declare GitHub's MCP server for pull requests. "Use fine-grained personal access tokens with minimum required permissions." ([GitHub access](https://platform.claude.com/docs/en/managed-agents/github))
- **Secrets:** vault credentials are "stored in the sandbox as an opaque placeholder… substituted with the real secret at egress. The agent never sees the secret value." ([vaults](https://platform.claude.com/docs/en/managed-agents/vaults))
- **Approvals:** per-tool policies `always_allow`, `always_ask` or `auto` ([permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies)).
- **Billing:** model tokens at API rates, web search at US$10 per 1,000, and "US$0.08 per session-hour" while running ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)). No subscription draw.
  - Max and Ultra plans include a monthly API credit (US$100 and US$200) that covers "Claude Managed Agents" and the Agent SDK with an API key. "Free, Pro, and Enterprise plans aren't eligible." ([help article](https://support.claude.com/en/articles/17154008))
- **Fit:** technically the tidiest (budget, vault, host list), but set up through API calls, and paid separately unless you are on Max.

### D. Claude Cowork

- **What it is:** "built for non-coding knowledge work — research, analysis, document creation, and other multi-step tasks", while "Claude Code is… built for software engineering" ([Cowork](https://claude.com/product/cowork)).
- **Scheduling:** it has scheduled tasks on all paid plans, and they "run remotely, so they run on their cadence even when your computer is asleep". They "work with your connectors and the files saved to your Claude account" ([help article](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)). Nothing there mentions a repository, a branch or a pull request.
- **How it relates to option A:** the same New scheduled task dialog serves both. "To make yours what the dialog calls a Claude Code task, select a repository or add a GitHub event or API trigger… That kind of task runs Claude Code in a cloud session." ([scheduled tasks](https://code.claude.com/docs/en/routines))
- **Fit:** wrong tool for pull requests. A Cowork task could email you a monthly "what changed in Australian EVs" briefing, but it can't edit `Vehicles.json`.

### E. "Claude Duet"

- **It exists.** "Introducing Claude Duet", 21 October 2026: "a new app where Claude works as a proactive agent". It "checks your connected accounts every few hours", sends a morning brief and works on tasks in the background ([announcement](https://claude.com/blog/claude-duet)).
- **Availability:** "A research preview is available by waitlist today, starting with US Pro, Max, and Ultra subscribers." A standalone app for iOS and Android, and on claude.ai. Team and Enterprise are "not included yet" ([product page](https://claude.com/product/claude-duet)).
- **Price:** none of its own. It "shares your plan's usage limits with the rest of Claude".
- **What it works with:** connectors such as Gmail, Slack, Stripe and QuickBooks. Neither page mentions GitHub, repositories or pull requests.
- **Fit:** none for now. It is not offered in Australia, and it is a personal assistant, not a repository agent.
- **The closest thing with the "teammate" shape is Claude Tag:** "@Claude" in Slack, which can "turn a bug report into a draft PR" and follow standing instructions. "Available for Claude Enterprise and Team customers in Slack." ([Claude Tag](https://claude.com/product/tag)) "Claude Tag isn't available on individual plans." ([Claude Code in Slack](https://code.claude.com/docs/en/slack))

### F. GitHub Agentic Workflows (`gh aw`)

- **What it is:** "define AI-powered repository automation in Markdown with YAML frontmatter"; `gh aw compile` "generates the `.lock.yml` workflow that GitHub Actions executes". Made by GitHub Next and Microsoft Research ([repository](https://github.com/github/gh-aw)).
- **Status:** the README carries the warning "Use it with caution, and at your own risk", and its docs call their slide deck "the technical preview deck". **Not verified:** a plain statement of the product's release status.
- **Engines:** "GitHub Copilot, Claude Code, OpenAI Codex, Google Gemini, and Pi".
- **Claude engine sign-in:** an Anthropic API key only. "Provider-based OAuth authentication (such as billing through a Claude Teams or Claude Max subscription) is not supported", and `CLAUDE_CODE_OAUTH_TOKEN` is ignored ([authentication](https://github.github.com/gh-aw/reference/auth/)).
- **Copilot engine sign-in on a personal repo:** a fine-grained token with the Copilot Requests permission, from an account with a Copilot licence ([authentication](https://github.github.com/gh-aw/reference/auth/)).
- **Safe outputs:** the workflow can create issues and pull requests "without giving the agentic portion of the workflow any write permissions" ([safe outputs](https://github.github.com/gh-aw/reference/safe-outputs/)).
  - `create-pull-request` takes `reviewers`, `assignees`, `labels` and `title-prefix`; `draft` defaults to true and is "a policy, not a default"; `allowed-files` is "an exclusive allowlist" ([pull requests](https://github.github.com/gh-aw/reference/safe-outputs-pull-requests/)).
  - "PRs do not trigger CI by default."
  - A `merge-pull-request` output exists, marked experimental. Don't configure it.
- **Network:** a firewall on by default; `network.allowed` lists domains. For the Claude engine, hosted search and fetch "run on provider infrastructure, so `network.allowed` does not constrain their destination domains"; a separate `hosted-web` list does ([network](https://github.github.com/gh-aw/reference/network/)).
- **Cost:** "gh-aw itself is free and open source." You pay Actions time, "free for public repositories, metered for private", and the engine: for Claude, "inference is billed directly to your Anthropic account" ([FAQ](https://github.github.com/gh-aw/reference/faq/), [billing](https://github.github.com/gh-aw/reference/billing/)).
- **Private repos on a free plan:** private repositories are supported, and Actions on GitHub Free includes US$12 a month. **Not verified:** a sentence saying gh-aw works on GitHub Free specifically.
- **Fit:** the best-documented defence against a misled agent. But it can't use the Claude subscription, it adds a compile step, and it retired a range of releases this year after a security advisory ([repository](https://github.com/github/gh-aw)). A good second step if option A's guard rails prove too soft.

### G. GitHub Copilot cloud agent and automations

- **What it is:** "Automations let you run Copilot cloud agent automatically on a schedule, in response to events in a repository, or programmatically via the API", and can open a pull request ([automations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-automations)).
- **Where:** "The repository must be private or internal."
- **Plans:** "available with the GitHub Copilot Pro, GitHub Copilot Pro+, GitHub Copilot Max, GitHub Copilot Business, and GitHub Copilot Enterprise plans." Copilot Pro is US$10 a month with 1,500 AI credits ([plans](https://docs.github.com/en/copilot/get-started/plans)).
- **Billing:** each run uses Actions time and AI credits ([changelog, 2 June 2026](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/)). An automation can carry an "AI credits limit".
- **Fit:** capable and well integrated, but US$10 a month for what the Claude plan already does.

### H. Third-party tools

| Tool | Relevant to | Price | Fit |
| --- | --- | --- | --- |
| Sentry (errors) | Agent 3's input | Developer plan free: 1 user, 5,000 errors, 30 days ([pricing](https://sentry.io/pricing/)) | Useful later as a better source than raw logs (§4.3) |
| Sentry Seer (error to fix) | Agent 3 | Add-on to Team (US$29/month) and above; not on the free plan; "new credit-based Seer pricing is coming December 8" ([pricing](https://sentry.io/pricing/)) | Too dear for one small server |
| Dependabot | Dependency pull requests only | Free on GitHub | Worth adding to the server and website; it complements the agents |
| Devin, Cursor background agents, OpenAI Codex cloud | All three | **Not verified** (prices not read for this note) | Each is a second subscription; none adds something the three agents need |
| Fly.io | Agent 3 | n/a | No agent of its own for this; it supplies the logs and the token (§4.3) |

## 4. The three agents, on Claude Code cloud scheduled tasks

### 4.0 Shared setup, once

1. **Connect GitHub with the Claude GitHub App, installed on `charge-line-app` and `charge-line-server` only.** The other route, `/web-setup`, hands over a token for "any repository your `gh` token can access" ([cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web)). The website repo stays out: a push to its `main` deploys.
2. **Two cloud environments**, so the agent that reads the web holds no secret and the agent that holds a secret can't reach the web:
   - `charge-line-research` (catalogue and prices): Limited network, with the makers', networks' and news sites listed under Allowed domains. No secrets.
   - `charge-line-logs` (server): Limited network with package managers only (for `npm ci`). One network secret, for `api.fly.io`.
3. **Keep each agent's instructions in its repo**, for example `agents/catalogue.md`, and make the task's saved prompt one line: "Follow `agents/catalogue.md`." Changes to an agent's rules then go through pull requests like everything else.
4. **Add the validators** (§4.1, §4.2) and a small GitHub Actions workflow that runs them on every pull request. It runs on Linux in under a minute, and it is a check the agent can't skip. A pull request pushed by a cloud session is pushed as you, so it triggers workflows normally.
5. **Remove every connector from each task.** "All of your connected MCP connectors are included by default… Claude can use an included connector during a run, including writes." ([scheduled tasks](https://code.claude.com/docs/en/routines)) An agent reading web pages must not also hold Gmail or Calendar.
6. **Leave usage credits off**, so a runaway run stops at the plan's limit instead of billing.
7. **Test each task with Run now** before trusting its schedule, and read the transcript.

### 4.1 Vehicle catalogue agent

- **Trigger and cadence:** weekly, one quarter of the 47 makes per run, so every model is checked monthly. The group comes from the week number and a list in `agents/catalogue.md`.
  - Why not one monthly run: about 150 page reads in one session is long, uses a large share of a usage window at once, and produces a pull request too big to review well.
  - Time: a custom cron such as `7 16 * * 6` (UTC), which is 03:07 on Sunday in Melbourne during daylight saving. Runs share your limits, so the small hours are best.
- **What it reads:**
  - `agents/catalogue.md`: the rules from the 22 October note. Maker's Australian pages first, then launch coverage; the Australian WLTP claim; usable kWh as the maker's net figure, else quoted × 0.95 marked "est."; and the two sites whose terms forbid automated collection (EVDB Australia, CarExpert's spec pages) on a do-not-use list.
  - `ChargeLine/Resources/Vehicles.json`.
  - The makers' sites and news search for new, changed and discontinued models.
- **What it may change:** `Vehicles.json` only.
  - Never change or remove an `id`: drivers' saved cars depend on them. A discontinued model gets `untilYear`.
  - Every changed entry updates its `source` with the page and the date.
  - More than about 25 changed models in one run: stop and open an issue instead. Something is wrong.
- **How it validates:** `node scripts/validate-catalogue.mjs` (to be written; Node 22 is in the VM):
  - the file parses, and every model has the fields the planner needs, with the right types;
  - sane ranges (for example usable kWh ÷ WLTP km between 100 and 300 Wh/km);
  - plugs from the known list;
  - unique IDs, and no ID on `develop` missing;
  - nothing outside `Vehicles.json` changed.
  - The Swift tests still need a Mac. Run them when you review, or add a macOS job: a 10-minute run is about US$0.62 of the US$12 ([Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)).
- **How the pull request is opened:** branch `claude/catalogue-<year>-W<week>` from `origin/develop`, base `develop`. The body lists each change as model, field, old → new, source link and the sentence quoted; then the makes checked with no change; then anything it couldn't read. Assigned to you. No change means no pull request.
- **Secrets:** none.
- **What could go wrong:**
  - A UK or European page's figures taken as Australian (WLTP and trims differ).
  - Gross battery size taken as usable.
  - A maker's site that needs JavaScript or blocks automated readers. The VM has Chrome; even so, some pages will go unread and must be listed as such, not guessed.
  - A plausible but invented number. The quoted sentence in the pull request is the defence: spot-check a few.
  - A page with text written to steer the agent. It can only reach the allow-listed sites and this one repo, and its output is a pull request.

### 4.2 Charging price agent

- **Trigger and cadence:** weekly (for example `37 16 * * 0` UTC, Monday 03:37 in Melbourne). It reads about ten pages and opens a pull request only when a typical price should move, so most weeks it does nothing.
- **First, write the rule down** in `agents/prices.md`. Networks publish ranges, and the agent needs one way to turn a range into a number. A rule consistent with the 27 October note ("the highest is used, so a plan never promises less than the driver pays"):
  - the price a non-member pays at a fast charger in the daytime;
  - for a published range, the upper end of the usual range, not the dearest single site;
  - whole cents; change the app only when the figure moves by 3c or more;
  - no published figure (Tesla and others show prices only in their apps): leave the number alone and say so.
  - This rule is the owner's to set. The above is a starting point.
- **What it reads:** the pages cited in the 27 October note for Tesla, Evie, Chargefox, Ampol AmpCharge, BP Pulse, NRMA and Jolt, plus Exploren and any other network it finds has become common. A new network is an issue for you, not a code change.
- **What it may change:** the seven numbers and the date comment in `ChargeLine/Model/ChargingCost.swift`.
  - **Better:** move the numbers into a small JSON resource first. The agent then edits data, not Swift it can't compile, and the validator can check it properly.
- **How it validates:** `node scripts/validate-prices.mjs` (to be written): every price between A$0.20 and A$1.50 per kWh, no move above 25% in one run, nothing else changed.
- **How the pull request is opened:** branch `claude/prices-<date>` from `origin/develop`, base `develop`. A table of network, old, new, the published sentence, link and date. Assigned to you.
- **Secrets:** none.
- **What could go wrong:**
  - A promotional or member price taken as the standard one.
  - A third-party "price guide" used as the source. The note used those only as a cross-check; the rule should say the same.
  - Churn: a number flapping by a cent or two. The 3c threshold is there for that.

### 4.3 Server log agent

- **Do first, in the server:**
  - **Log the stack trace for every 5xx.** Today the line is `error <route pattern>: <message>`. A message alone rarely identifies the line of code, so the agent could only guess.
  - **Keep personal data out of the logs** (coordinates, VINs, tokens). Whatever is logged gets copied into a session transcript.
  - Logging the route pattern, not the raw URL, is already right: it gives a caller little room to plant text in the log.
- **Trigger and cadence:** daily, for example `7 18 * * *` UTC (05:07 in Melbourne). Fly keeps about 7 days, so a missed day can be recovered. A weekly run would sit on the edge of that window.
- **What it reads:** Fly's logs through the HTTP API "`fly logs` uses under the hood": `GET /api/v1/apps/charge-line-server/logs`, paged with `next_token`. "By default, the most recent 100 logs from the last 24 hours are returned", and it is "the only option that gives you access to historical logs going back to the current retention window (about 7 days)". Fly notes it "isn't officially supported for external use, but it's mostly stable: `flyctl` depends on it" ([logs API options](https://docs.fly.io/monitoring/logs-api-options)).
  - A committed script, `scripts/fetch-logs.mjs`, pages through the last 26 hours and prints a short summary: each distinct error with its route, count, first and last time and one sample (cut to a fixed length), plus any failed `chargers:` or `weather:` build.
  - The machine stopping when idle doesn't matter: the logs are kept in Fly's own store, not on the machine.
  - **Not verified:** the host name (`api.fly.io` is what flyctl uses; the docs page gives only the path).
- **What it does:**
  - No errors: stop. No issue, no pull request.
  - An error already tracked in an open issue or pull request: add the new count as a comment, nothing more.
  - A new error with a clear cause: write a failing test, fix it, run `npm test` and `npm run typecheck`, and open a pull request against `main`, assigned to you.
  - Anything else: open an issue with the evidence.
- **What it may change:** the server's source and tests. Not `fly.toml`, the Dockerfile, dependencies, `agents/` or `.github/`; those become issues.
- **Secrets:** one read-only Fly token, stored as a network secret for `api.fly.io`, so the agent can use it but never see it.
  - `fly tokens create readonly --name "log agent" --expiry 2160h`: "limited to reading a single org and its resources" ([access tokens](https://docs.fly.io/security/tokens), [command](https://docs.fly.io/flyctl/tokens-create-readonly)). Tokens last "20 years… by default", so set an expiry.
  - It is org-wide. Fly documents app-scoped deploy, SSH and exec tokens, but no app-scoped read-only one. `--from-existing` can "create a read-only token based on an existing token", which may give an app-only read token from a deploy token. **Not verified.**
  - **Not verified:** exactly what a read-only token can read besides logs, and the header form the network secret needs (Fly tokens "look like `FlyV1 fm2_...`. The `FlyV1` prefix and the space after it are part of the token").
  - No deploy token, ever. `fly deploy` stays on your Mac.
- **What could go wrong:**
  - **Text in a log line written to steer the agent.** Error messages can echo what an upstream service or a caller sent. The script cuts samples short, the agent can reach only Fly and this repo, and its output is an issue or a pull request.
  - **Noise.** Upstream timeouts (weather, Overpass) aren't bugs. The rules should name them and set a count below which nothing is opened.
  - **A wrong fix that passes the tests.** Review it as you would any pull request; the transcript shows the reasoning.
- **Fly's own search** (Grafana at fly-metrics.net, 7 days, "beta… free during the beta") is for a person, not an agent ([search logs](https://docs.fly.io/monitoring/search-logs)). The Fly Log Shipper needs its own always-on app and an outside store; too much for this ([logs API options](https://docs.fly.io/monitoring/logs-api-options)).
- **Would Sentry be a simpler, safer source?** Simpler to read, not safer.
  - For: errors arrive grouped and counted, with stack traces and the release. The free Developer plan allows one user and 5,000 errors with a 30-day lookback ([pricing](https://sentry.io/pricing/)).
  - Against: a new SDK on the server; a new company receiving error data, which the privacy policy would have to name; and the pricing page lists third-party integrations as not included in the Developer plan, so no GitHub link on the free tier.
  - The text in a Sentry event is as untrusted as a log line.
  - Fly no longer sets Sentry up for you: "Provisioning new Sentry projects through Fly.io… is no longer available." ([Fly docs](https://docs.fly.io/monitoring/sentry))
  - **Verdict:** start with Fly's logs plus stack traces. Look at Sentry only if errors become frequent enough to need grouping.

### 4.4 Later: serve the catalogue and prices from the server

Both files ship inside the app, so a merged pull request reaches drivers only with the next App Store release. The server already serves a daily charger file (`/v1/chargers/au`). Serving `Vehicles.json` and the prices the same way would let a merged change reach drivers at the next `fly deploy`, which is still a step only you take. It also makes a bad merge reach everyone faster, so the validators matter more.

## 5. GitHub facts and the security checklist

### GitHub

- **Actions on a private repo, GitHub Free:** US$12 of compute a month is included. Linux is US$0.006 a minute and macOS US$0.062. With no payment method, "usage is blocked once you consume the included compute usage" ([Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)). The validators on Linux cost almost nothing; Xcode tests on every agent pull request would not fit.
- **Protected branches and code owners in private repos need GitHub Pro.** GitHub's plans page lists "Protected branches", "Code owners" and "Required pull request reviewers" under "Advanced tools and insights in private repositories" for Pro ([GitHub's plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)). **Not verified:** Pro's current price (US$4 a month when last seen).
- **Code owners:** "automatically requested for review when someone opens a pull request that modifies code that they own", but not for drafts, and "the CODEOWNERS file must be on the base branch" ([code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)).
- **Under option A the pull request's author is you**, so there is nobody to request a review from. Assign yourself: `gh api -X POST repos/<owner>/<repo>/issues/<number>/assignees -f "assignees[]=<you>"`. **Not verified:** that GitHub refuses a review request for the author (its API has long done so), and whether assigning yourself sends any notification. A bookmark on github.com/pulls/assigned may be the simplest inbox.
- **Under options B and F the author is an app**, so `reviewers:` or CODEOWNERS (with Pro) can request you.
- **Tokens, where one is needed (options C2 and F):** a fine-grained personal access token "can be further limited to only access specific repositories" with "specific, fine-grained permissions" ([personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)): one repo, Contents and Pull requests read and write, plus Issues for the log agent. Option A needs none. For option B, Anthropic's guidance is "Do not use a personal access token — a static token does not rotate between runs and could be partially or fully recovered over time via prompt injection" ([action security](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)).
- **Dependabot** covers npm, GitHub Actions and Swift packages, including private repositories ([supported ecosystems](https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories)). It is the right tool for dependency pull requests; none of the three agents should do that job.

### The risk

All three agents read text other people wrote (web pages, log lines) and can write to a repo. Anthropic's own wording: an agent's "behavior can be influenced by the content they process: files, webpages, or user input. This is sometimes called prompt injection." ([secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment))

What each platform documents against it:

| | Cloud scheduled tasks (A) | GitHub Action (B) | Agentic Workflows (F) | Managed Agents (C2) |
| --- | --- | --- | --- | --- |
| Writes limited to a pull request | No: the agent pushes with your access; the proxy blocks only branch deletion and tags | By workflow `permissions:` | Yes: agent job read-only, "safe outputs" write | By the token you supply |
| Network allow-list | Yes, per environment | No | Yes, firewall on by default | Yes, `allowed_hosts` |
| Secrets hidden from the agent | Yes: GitHub proxy and network secrets | No: "best-effort scrub… reduces but does not eliminate prompt injection risk" | Agent job has no write token | Yes: vault placeholders |
| A second model checks actions | Yes: auto mode's classifier | Only if you choose auto mode | Threat detection on outputs (not read in detail) | `auto` policy, optional |
| Hard spend cap | Plan limit (usage credits off) | `--max-turns`, job timeout | `max-turns`, AI-credit cap | Dollar budget per run |

Sources: [cloud environments](https://code.claude.com/docs/en/cloud-environments), [scheduled tasks](https://code.claude.com/docs/en/routines), [action security](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md), [gh-aw safe outputs](https://github.github.com/gh-aw/reference/safe-outputs/), [gh-aw network](https://github.github.com/gh-aw/reference/network/), [Managed Agents environments](https://platform.claude.com/docs/en/managed-agents/environments), [vaults](https://platform.claude.com/docs/en/managed-agents/vaults), [budgets](https://platform.claude.com/docs/en/managed-agents/budgets).

### Checklist

1. **Pull requests only.** No agent gets a way to merge, release or deploy: no App Store Connect key, no Fly deploy token, no website repo.
2. **Decide about branch protection.** Under option A the agent pushes as you, and the proxy "doesn't limit which branches a push can update". The only hard stop is a branch protection rule on `develop` and `main` ("Require a pull request before merging", with "Do not allow bypassing the above settings", because rules don't bind admins by default) ([protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)). On private repos that needs GitHub Pro. Without it, the stops are the instructions and auto mode's classifier, and a bad push is undone from your local clone.
3. **No connectors on the tasks** (§4.0).
4. **Separate reading the web from holding a secret.** The catalogue and price agents have the web and no secret. The log agent has a secret and no web.
5. **Narrow network.** Limited with a domain list for the research environment; never Full on the logs environment.
6. **Check the repos hold no secrets.** Each run clones the whole repo into a machine that reads web pages. `Secrets.xcconfig`, `.env` and `.tesla/` must be ignored by git and absent from history.
   - Checked 13 November 2026: `Config/Secrets.xcconfig` (app) and `.env` (server) were never committed and are ignored; `.tesla/` is in no repo. The only key-like files ever added are `Secrets.example.xcconfig` (a template) and the Tesla public key on the website, which is public by design. Re-check whenever a new secret file appears.
7. **Read-only, expiring Fly token**, stored as a network secret and named so it can be revoked (`fly tokens list`, `fly tokens revoke`).
8. **Validators run twice:** by the agent, and by a workflow on the pull request that fails if anything outside the allowed files changed.
9. **Agents can't loosen their own rules.** A change to `agents/`, `scripts/validate-*`, `.github/` or `.claude/` fails the validator and is yours to make.
10. **Every claim in a pull request carries its link and the sentence quoted.** Spot-check a few each time.
11. **Read the transcript** when a run surprises you. "Succeeded" means the session ended, not that the work is right.
12. **Usage credits off**; (option B only) the one-year subscription token in GitHub secrets is rotated yearly.

## 6. Cost

**Under the recommendation: A$0 extra.** The runs use the plan's limits. Anthropic publishes no figure for how much of a plan's limit a run uses, so measure it: do one Run now of each agent and look at claude.ai/settings/usage. The catalogue run is the one to watch; the weekly split (§4.1) is there to keep it small.

For comparison, the same work at API rates, which is what options C2 and F would bill. **Estimates**, from the published prices for Claude Sonnet 5.5 (US$2 per million input tokens, US$10 output, US$0.10 for cached input) and web search at US$10 per 1,000 ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)). Claude Opus 5.5 is twice these rates.

| Agent | Assumed work per run | Per run | Runs a month | Per month |
| --- | --- | --- | --- | --- |
| Catalogue, one quarter of the makes | About 40 page reads, 15 searches, 70 steps, a 30,000-token file | US$1–3 | 4.3 | US$5–13 |
| Prices | About 15 page reads, 10 searches, 25 steps | US$0.50–1 | 4.3 | US$2–4 |
| Logs, quiet day | Fetch, summarise, stop | US$0.05–0.10 | About 28 | US$1.50–3 |
| Logs, a day with a fix | 60 steps, tests run | US$1–3 | About 2 | US$2–6 |
| **Total** | | | | **About US$10–25 (A$15–38)** |

| Setup | Claude | GitHub Actions | Other | Total a month |
| --- | --- | --- | --- | --- |
| **A. Cloud scheduled tasks** | In the plan | None (validator workflow: a few minutes) | None | **A$0 extra** |
| **B. GitHub Action, subscription token** | In the plan | About 200 Linux minutes ≈ US$1.20 of the included US$12 | None | **A$0 extra** |
| **F. Agentic Workflows, Claude engine** | US$10–25 on an API key | Same, plus about 1.5 minutes of overhead per job | None | **US$10–25**, or US$0 inside a Max plan's US$100 API credit |
| **C2. Managed Agents** | US$10–25 on an API key | None | US$0.08 per session-hour: under US$1 | **US$11–26**, or US$0 inside a Max plan's credit |
| **G. Copilot automations** | n/a | Some | Copilot Pro US$10, 1,500 AI credits (whether that covers these runs: not verified) | **US$10 or more** |

Plan prices: Pro US$20 a month, Max US$100, Ultra US$200 ([pricing](https://claude.com/pricing)).

## 7. Open questions and what is not verified

- **Which Claude plan the owner is on.** It decides whether options C2 and F are free (Max and Ultra carry an API credit) or cost US$10–25 a month (Pro).
- **How much of the plan's limit each run uses.** Not published. Measure with Run now.
- **Whether an unattended cloud run opens and assigns the pull request by itself**, through `gh api`, with no prompt left waiting. The docs' examples say it opens pull requests; the exact mechanism isn't documented. Test first.
- **Whether WebFetch in a cloud session follows the environment's allow-list.** Assumed yes.
- **Whether makers' and networks' sites serve their pages to a cloud machine** (JavaScript, bot blocking). Only a trial run will show which sites fail.
- **Fly:** the API's host name; what a read-only token can read besides logs; whether `--from-existing` gives an app-only read token; the header form for the network secret.
- **GitHub:** Pro's price today: third-party sites list US$4 a month or US$48 a year ([creditforstartups](https://creditforstartups.com/resources/github-pro-pricing), [Capital & Compute](https://capitalandcompute.net/blog/github-pricing-plans-cost/); secondary sources, checked 13 November), but GitHub's own pricing page needs JavaScript, so not confirmed from GitHub. Also: that the author of a pull request can't be asked to review it; whether assigning yourself notifies you.
- **Checked 13 November against our own notes:** the catalogue rules (makers' figures first, usable kWh × 0.95 marked "est.", EVDB Australia and CarExpert's spec pages not used because their terms forbid automated collection) are in `2026-10-22-australian-ev-catalog.md`; "the highest is used, so a plan never promises less" is in `2026-10-27-charging-prices.md`.
- **GitHub Agentic Workflows' release status**, and whether it is confirmed on GitHub Free for private repos. Its threat-detection step was not read in detail.
- **Copilot:** whether 1,500 AI credits cover these runs, and the release status of automations.
- **Sentry:** whether the free plan's API can be polled by an agent, and Seer's price after 8 December 2026.
- **Devin, Cursor, Codex:** only their pricing pages were read; none was tested.
- **Everything in §6 marked as an estimate.**
- **Could not read:** GitHub's pricing page (it needs JavaScript). GitHub's REST page on review requests doesn't mention authors either way.

## Sources

- Claude Code: [scheduled tasks](https://code.claude.com/docs/en/routines), [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web), [cloud environments](https://code.claude.com/docs/en/cloud-environments), [scheduling compared](https://code.claude.com/docs/en/scheduled-tasks), [GitHub Actions](https://code.claude.com/docs/en/github-actions), [authentication](https://code.claude.com/docs/en/authentication), [headless](https://code.claude.com/docs/en/headless), [tools reference](https://code.claude.com/docs/en/tools-reference), [permission modes](https://code.claude.com/docs/en/permission-modes), [secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment), [Claude Code in Slack](https://code.claude.com/docs/en/slack), [action security](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)
- Claude plans and help: [pricing](https://claude.com/pricing), [Agent SDK with your plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan), [monthly API credits](https://support.claude.com/en/articles/17154008), [Cowork scheduled tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)
- Claude products: [Cowork](https://claude.com/product/cowork), [Introducing Claude Duet](https://claude.com/blog/claude-duet), [Claude Duet](https://claude.com/product/claude-duet), [Claude Tag](https://claude.com/product/tag)
- Claude Platform: [Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview), [scheduled deployments](https://platform.claude.com/docs/en/managed-agents/scheduled-deployments), [vaults](https://platform.claude.com/docs/en/managed-agents/vaults), [GitHub access](https://platform.claude.com/docs/en/managed-agents/github), [budgets](https://platform.claude.com/docs/en/managed-agents/budgets), [environments](https://platform.claude.com/docs/en/managed-agents/environments), [permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies), [pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- GitHub Agentic Workflows: [repository](https://github.com/github/gh-aw), [authentication](https://github.github.com/gh-aw/reference/auth/), [billing](https://github.github.com/gh-aw/reference/billing/), [network](https://github.github.com/gh-aw/reference/network/), [safe outputs](https://github.github.com/gh-aw/reference/safe-outputs/), [pull requests](https://github.github.com/gh-aw/reference/safe-outputs-pull-requests/), [FAQ](https://github.github.com/gh-aw/reference/faq/)
- GitHub: [Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans), [code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens), [Copilot automations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-automations), [Copilot plans](https://docs.github.com/en/copilot/get-started/plans), [Dependabot ecosystems](https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories)
- Fly.io: [logs API options](https://docs.fly.io/monitoring/logs-api-options), [logging overview](https://docs.fly.io/monitoring/logging-overview), [search logs](https://docs.fly.io/monitoring/search-logs), [`fly logs`](https://docs.fly.io/flyctl/logs), [access tokens](https://docs.fly.io/security/tokens), [`fly tokens create readonly`](https://docs.fly.io/flyctl/tokens-create-readonly), [Sentry](https://docs.fly.io/monitoring/sentry)
- Others: [Sentry pricing](https://sentry.io/pricing/), [Cursor pricing](https://cursor.com/pricing), [Devin pricing](https://devin.ai/pricing), [Codex pricing](https://learn.chatgpt.com/docs/pricing)
