# Agent Platforms Compared: What Anthropic's Competitors Offer for the Three Maintenance Agents

**Date:** 2026-11-14
**For:** the owner, who asked what OpenAI and "others" offer for the job Claude Code's cloud scheduled tasks would do: an unattended agent that runs on a schedule, clones a private GitHub repo, reads the web, and opens a pull request for review. The three agents and what they need are in §1 of [the 12 November note](2026-11-12-maintenance-agents.md); the Claude options are covered there and not redone here.
**How to read it:** every fact is followed by the page that owns it, read on 14 November 2026. "Not verified" marks what I could not confirm from a primary source. Costs marked "estimate" are my arithmetic from published rates, not measurements. Prices are US dollars and, unless a page says otherwise, exclude Australian GST.

## Bottom line

- **No competitor beats Claude Code's cloud scheduled tasks on cost for these three agents.** Every option below is a second bill (about US$10–40 a month) or pay-per-token. The Claude plan you already pay for covers them at A$0 extra (earlier note, §6).
- **OpenAI has no cloud scheduler for repository work.**
  - Codex scheduled tasks that touch a repo run on your Mac, which must be on with the app open ([scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=app)).
  - Codex cloud runs repo tasks with the computer asleep, but nothing schedules them. OpenAI support, 5 November 2026: "Local schedules need the computer and app running", and cloud scheduling is feedback with no timeline ([forum](https://community.openai.com/t/codex-cloud-web-has-compounding-reliability-observability-and-workflow-problems-that-make-long-running-tasks-difficult-to-trust/1397259)).
  - **The route that works:** `openai/codex-action` or `codex exec` on a GitHub Actions cron, paid with an **API key** (about US$5–25 a month, estimate). OpenAI steers CI away from ChatGPT-plan sign-in ([non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)).
- **Google: not now.**
  - Jules, the closest match, "will wind down on December 31, 2026". It has been read-only since 11 November ([Jules changelog](https://jules.google/docs/changelog/)).
  - Gemini CLI stopped serving Google AI Pro and Ultra subscribers on 18 June 2026; only paid API keys still work ([Google Developers Blog](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)).
  - The replacement, Antigravity, has cron "automations" and cloud "remote agents", but remote agents only finished rolling out on 9 November 2026. I couldn't confirm that the two work together ([changelog](https://antigravity.google/docs/changelog/)).
- **GitHub Copilot automations are the strongest competitor**, and the only one with better guard rails than Claude:
  - pull requests attributed to Copilot (for shared automations);
  - workflows held until you approve;
  - one branch only;
  - a per-run credit cap.
  - **But:** private repos only ("public repositories coming soon"), so the public `charge-line-data` repo can't host the catalogue and price agents yet. Web search in the cloud agent is documented both ways. It costs US$10–39 a month ([automations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-automations), [changelog](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/)).
- **Cursor (US$30 Premium), Devin (US$20 Pro), Kiro (US$20 Pro) and Warp Oz (US$20 Build) all do the full job:** cron-scheduled cloud agents that clone a repo and open a pull request. None does something these three agents need that Claude doesn't. Kiro is the cheapest to try: the first month of Pro is free, plus 500 trial credits ([Kiro pricing](https://kiro.dev/pricing/)).
- **Where a competitor genuinely beats Claude's cloud tasks:**
  - Copilot's pull-request protections.
  - The GitHub Actions routes (Codex action, and equally the Claude action) can run on a **macOS runner**, so the catalogue agent's pull request could be checked by the Swift tests. Claude's cloud VM is Linux only.
  - Codex's two-job pattern keeps write access out of the agent's job.
- **Where none beats it:**
  - cost;
  - secrets kept out of the agent's reach. Only Codex cloud matches Claude's proxy-held network secrets; Copilot can confine a secret to an MCP server;
  - one plan covering all three agents.
- **If you want one proof of concept:** the price agent on one network, using `openai/codex-action` in a **public** throwaway repo. Actions minutes are free on public repos, so it costs well under US$1 of API usage (§9).

## 1. What changed since the 12 November note

- **The catalogue and the prices are moving to a public repo, `charge-line-data`.** Two consequences:
  - GitHub Actions is "free for public repositories" (earlier note, §3F; [Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)). Any GitHub Actions route (Claude action, Codex action, Gemini action, Agentic Workflows) costs only model usage there.
  - Copilot automations "are supported in private and internal repositories, with support for public repositories coming soon" ([changelog, 2 June 2026](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/)).
- **The server log agent stays on the private `charge-line-server`** and is the only one holding a secret (the read-only Fly token).

## 2. OpenAI

### What exists

| Product | Status | Fits the three agents? |
| --- | --- | --- |
| Codex cloud | No status label; in Plus and up | Runs repo tasks in the cloud and opens pull requests, but nothing schedules them |
| Codex scheduled tasks (desktop app) | No status label | Repo tasks run on your computer only |
| ChatGPT scheduled tasks and Team Tasks (ChatGPT Work) | No status label | Run in the cloud, but "can't work directly in a folder"; no repository documented |
| `codex cloud exec` (CLI) | "Experimental" | Starts a cloud task from any machine, so a cron elsewhere could fire it |
| `openai/codex-action` and `codex exec` in GitHub Actions | Released; permission profiles beta | **Yes**, on a GitHub Actions cron with an API key |
| GitHub Agentic Workflows, Codex engine | Preview (earlier note, §3F) | Yes, with an API key |

The Codex docs moved from developers.openai.com to learn.chatgpt.com; old links redirect.

### Codex cloud

- **What it is:** "Each task has its own workspace and can keep working while your computer is asleep." It checks out "any repository available to Codex through your connected GitHub or GitLab account", and you "commit or open a pull request when you're ready" ([Codex cloud](https://learn.chatgpt.com/docs/cloud)).
- **No schedule:**
  - The cloud page describes no scheduled runs.
  - An OpenAI support reply, 5 November 2026: scheduling exists "in supported desktop/local workflows, though web Cloud support differs"; "Local schedules need the computer and app running"; feedback on "Cloud scheduling" was passed on, but "I can't promise changes or a timeline" ([forum thread](https://community.openai.com/t/codex-cloud-web-has-compounding-reliability-observability-and-workflow-problems-that-make-long-running-tasks-difficult-to-trust/1397259)).
  - The same thread's author, a user rather than OpenAI, says "Codex Cloud cannot be relied on for long term execution".
- **Starting it from elsewhere:** `codex cloud` is "Experimental"; `codex cloud exec` "submits a task directly", `--env` is "required", and "Authentication follows the same credentials as the main CLI" ([CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli)).
  - A GitHub Actions cron could fire a cloud task this way, but it needs your ChatGPT sign-in on the runner (next section).
  - **Not verified:** whether a task started like this opens the pull request by itself.
- **Machine:** one VM per task. Plus gets "2 vCPUs, 8 GiB memory, 8 GiB disk"; Pro and above get 4 vCPUs, 16 GiB and 32 GiB ([cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)). **Not verified:** the operating system (Linux is assumed; no macOS is documented).
- **Internet:**
  - "By default, Codex blocks internet access during the agent phase. Setup scripts still run with internet access." ([agent internet access](https://learn.chatgpt.com/docs/cloud/internet-access))
  - Per environment, the choices are an empty allow-list, a "Common dependencies" preset, or "All". Methods can be limited to "`GET`, `HEAD`, and `OPTIONS`".
  - The page lists the risks: prompt injection from "untrusted web content", "Code or secret exfiltration", and a worked example where a GitHub issue makes the agent "leak the last commit message to an attacker-controlled server".
- **Web search:** in Codex it is "a hosted tool". It "doesn't use the permission profile's network proxy or domain allowlist, so it can stay available when command network access is disabled" ([web search](https://learn.chatgpt.com/docs/web-search)).
  - Modes are `disabled`, `cached` (the default for local chats; "an OpenAI-maintained index instead of fetching arbitrary pages live"), `indexed` and `live`.
  - "Treat all web results as untrusted input." Cached mode "lowers—but doesn't remove—prompt injection risk."
  - **Not verified:** whether the cloud agent has it. The page doesn't say.
  - For prices, `live` is the mode needed: a cached index may lag a network's price change.
- **Secrets** ([cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)):
  - An environment variable is "Passed directly to programs in the environment".
  - A network secret: "Programs receive a placeholder; the proxy substitutes the real value for allowed destinations." HTTPS on port 443 only.
  - This is the same design as Claude's network secrets, and the only competitor with it.
- **Pull requests:**
  - Code review runs under the "chatgpt-codex-connector" bot ([GitHub integration](https://learn.chatgpt.com/docs/third-party/github)).
  - **Not verified:** who is the author of a pull request Codex cloud opens, and whether it can request a reviewer.
  - Community threads report the Create PR step failing at times ([forum](https://community.openai.com/t/codex-cloud-fails-to-create-pr/1380347); not a primary source).

### Codex and ChatGPT scheduled tasks

- **Desktop app:**
  - "Schedule recurring tasks to run in the background." "Keep the computer on and the app running when a scheduled task needs local files." ([scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=app))
  - For a Git repository, a task runs "in your local project or on a new" worktree.
  - Schedules use RRULE (`RRULE:FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=9;BYMINUTE=0`), not cron.
  - This matches Claude's Desktop scheduled tasks: it could run the Xcode tests, but only while the Mac is on.
- **Web and mobile:**
  - Tasks "can use uploaded context and connected tools, but they can't work directly in a folder on your computer" ([scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=web)).
  - Event triggers (Gmail, Slack, GitHub pull request activity) are web and mobile only. "One task can use multiple event triggers, but it can't combine event triggers with a time-based schedule."
- **Team Tasks:** "Team Tasks run in the cloud through the team's service account and configured app connections" ([scheduled tasks](https://learn.chatgpt.com/docs/automations)). This is a workspace feature. **Not verified:** whether it can use a Codex cloud environment and open a pull request.
- **Unattended permissions:** "Scheduled tasks run unattended and use your default sandbox settings". With full access, "background scheduled tasks carry elevated risk" ([scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=app)).
- **Limits, Not verified:** OpenAI's help article reportedly caps active scheduled tasks at 3 (Free, Go), 5 (Plus), 10 (Business, Edu) and 15 (Pro, Enterprise), with hourly schedules on paid plans only ([help article](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt)). help.openai.com refused automated reading, so these figures come from search-result text.
- **ChatGPT agent** is reported as replaced by ChatGPT Work ([help article](https://help.openai.com/en/articles/11752874-chatgpt-agent); **Not verified**, same reason).

### Codex in GitHub Actions: the route that works today

- **`openai/codex-action`:**
  - It installs the Codex CLI and "configures a proxy to the Responses API", for running Codex "while keeping tight control over the privileges available to Codex" ([repository](https://github.com/openai/codex-action)).
  - "Users must provide an API key for their chosen provider." The docs describe API-key use only ([GitHub Action](https://learn.chatgpt.com/docs/github-action)).
  - **Safety:** `safety-strategy` defaults to `drop-sudo`, which "removes `sudo` before running Codex" and "protects secrets in memory"; `read-only` "should not be relied on alone to protect secrets" ([GitHub Action](https://learn.chatgpt.com/docs/github-action)).
  - **Network:** the recommended `:workspace` profile "does not grant network access" ([repository](https://github.com/openai/codex-action)). Live web search is a hosted tool outside that sandbox ([web search](https://learn.chatgpt.com/docs/web-search)), so the research agents may get search without opening the runner's network. **Not verified** inside the action.
  - **Runners:** Linux and macOS support every strategy; Windows needs `unsafe` ([repository](https://github.com/openai/codex-action)). A macOS runner could run the Swift tests, at US$0.062 a minute on a private repo (earlier note, §5). The Claude Code action is a Node program and should run there too; **Not verified**.
  - **Pull requests:** it doesn't open them itself. The README example posts a comment from a separate `github-script` step.
- **`codex exec`** ([non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)):
  - "By default, `codex exec` runs in a read-only sandbox"; `--sandbox workspace-write` allows edits.
  - The docs' GitHub Actions example splits the work in two. The Codex job has `contents: read`; an `open_pr` job "applies the patch, pushes a branch, and runs `gh pr create`".
  - **That split is a real guard rail:** the job that reads the web holds no write token. The earlier note's Claude option A can't do this; its option F (Agentic Workflows) can.
- **Sign-in in CI:**
  - "API keys are the right default for automation."
  - ChatGPT-plan sign-in is for "enterprise teams using ChatGPT-managed Codex access on trusted runners". "Treat `~/.codex/auth.json` like a password", and "Do not use this workflow for public or open-source repositories" ([non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)).
  - So there is no clean equivalent of Claude's `CLAUDE_CODE_OAUTH_TOKEN`. **Not verified** whether plan sign-in works at all on a personal Plus plan in CI.
- **API keys** are "Great for automation in shared environments like CI", charged at API rates, and "cloud features such as GitHub code review and Slack are not included" ([Codex pricing](https://learn.chatgpt.com/docs/pricing)).

### Plans and prices

- **Plans:** "ChatGPT Work and Codex are included in your ChatGPT Free, Go, Plus, Pro, Business, Edu, or Enterprise plan." ([Codex pricing](https://learn.chatgpt.com/docs/pricing))
  - Free US$0; Go US$8; Plus US$20; Pro from US$100 (US$100, US$200 or US$500); Business US$20–25 a user.
  - Codex on the web (cloud) starts at **Plus**. Free and Go are for "quick coding tasks" in the desktop app.
- **Plus limits:** per five hours, they vary by model, for example GPT-6.1 Sol "15-160" local messages. "Cloud tasks may use more of your allowance than local messages, and weekly limits may also apply." Pro "currently has no five-hour limit" ([Codex pricing](https://learn.chatgpt.com/docs/pricing)).
- **API rates per million tokens** ([API pricing](https://developers.openai.com/api/docs/pricing)):
  - `gpt-6.1-sol`: US$2 input, US$0.10 cached, US$10 output. These are Claude Sonnet 5.5's rates.
  - `gpt-6.1-terra`: US$1 and US$5. `gpt-6-luna`: US$0.10 and US$0.50.
  - `gpt-5.3-codex`: US$1.75 and US$14. It is the only Codex-named model listed.
  - Web search: US$10 per 1,000 calls.

### Fit

- **Catalogue and price agents** (public `charge-line-data`): good, through `codex-action` on an Actions cron. Free Actions minutes, API tokens only, and a read-only agent job with a separate PR job.
- **Server log agent** (private): workable. But the Fly token would sit in the runner (as with the Claude action), and the network has no allow-list beyond Codex's own sandbox.
- **Against:** a separate API bill, and a YAML workflow per agent. Pull requests come from `github-actions[bot]` or whatever token the PR job uses, which lets you request your own review. **Not verified** in this setup.

## 3. Google

### Jules is closing

- **Shutdown:** "Jules will wind down on December 31, 2026." Sessions could be finished until 11 November 2026; Jules is read-only until the end of the year. Google points to "Google Antigravity" ([Jules changelog, 29 October 2026](https://jules.google/docs/changelog/)).
- **What it had** ([Jules changelog](https://jules.google/docs/changelog/)), none of which can be started now:
  - scheduled tasks (10 December 2025: "Jules runs them on your schedule and opens a pull request");
  - web search (8 August 2025);
  - an API (3 October 2025);
  - repository environment variables (1 October 2025);
  - a "commit as you" setting (19 February 2026).
- **Limits while it ran:** 15 tasks a day free, 100 on Google AI Pro, 300 on Ultra ([usage limits](https://jules.google/docs/usage-limits/)).

### Gemini CLI and the Gemini CLI GitHub Action

- **Retired for consumer plans:** "On June 18, 2026, Gemini CLI and Gemini Code Assist IDE extensions will stop serving requests for Google AI Pro and Ultra." Free use through Gemini Code Assist for individuals ended too ([Google Developers Blog, 19 May 2026](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)).
  - "Gemini CLI will remain accessible via paid Gemini and Gemini Enterprise Agent Platform API keys."
  - Gemini Code Assist for GitHub took no new installations from that date, and its requests "in the following weeks will stop being served".
- **`google-github-actions/run-gemini-cli`:** "A GitHub Action invoking the Gemini CLI" ([repository](https://github.com/google-github-actions/run-gemini-cli)).
  - Its triage example runs "automatically or on a schedule". Gemini can "interact with other CLIs like the GitHub CLI (`gh`)".
  - Sign-in: Gemini API key, Vertex AI, Workload Identity Federation, or Gemini Code Assist.
  - The README still says AI Studio keys have "generous free-of-charge quotas". It has no prompt-injection guidance.
- **Gemini API prices** ([pricing](https://aistudio.google.com/docs/pricing)):
  - Gemini 3.8 Flash: free tier, or US$0.75 input and US$3.75 output per million until 31 December 2026, then US$1.50 and US$7.50.
  - Grounding with Google Search: "5,000 free search requests per month", then US$14 per 1,000.
  - **Free-tier data is "Used to improve our products"**: fine for the public data repo, not for the private server.
- **Not verified:** whether a free AI Studio key still runs Gemini CLI after 18 June 2026. The blog names only "paid" keys. If it does, this would be a US$0 option for the public data repo.

### Google Antigravity (the replacement)

- **Automations** ([/automation](https://antigravity.google/docs/commands/automation)):
  - "Set up a scheduled background automation by describing it to the agent in a conversation."
  - Cron with a time zone (`CRON_TZ=America/Los_Angeles 0 9 * * 1`), or Hourly, Daily or Weekly. Model: Flash Lite, Flash or Pro.
  - "Unattended runs automatically deny anything that would normally ask for your approval", so grants have to be recorded after a test run.
  - The only surface listed is the "Antigravity App"; the file lives under `~/.gemini/config/sidecars/`.
  - Scheduled Tasks were renamed Automations on 7 October 2026 ([changelog](https://antigravity.google/docs/changelog/)).
  - **Not verified:** whether automations run with your computer off.
- **Remote agents** ([remote agents](https://antigravity.google/docs/remote-agents/)):
  - They "run your agent sessions and tools in an isolated, Google-managed remote environment" and keep going "even when you close your browser, put your laptop to sleep".
  - GitHub by OAuth, private repos allowed.
  - For "Google AI Pro and Google AI Ultra subscribers who sign in with a personal Google Account". Not on Free, Google AI Plus or business accounts.
  - Rollout ([changelog](https://antigravity.google/docs/changelog/)):
    - 3 November 2026: "Conversations in a cloud project run in the cloud instead of on your computer".
    - 9 November: "finished rolling out to Google AI Ultra subscribers and to Google AI Pro subscribers on a paid plan".
    - 13 November: you can "sign in to pull request links directly from the app".
  - **Not verified:** that an automation can run as a remote agent; that a remote agent opens pull requests by itself; its network rules, secrets and web search.
- **Plans** ([changes to plans, 19 May 2026](https://antigravity.google/blog/changes-to-antigravity-plans/)):
  - Google AI Pro, US$20 a month, "provides an entry-level quota for experimentation".
  - Ultra costs US$100 (5× Pro's tokens) or US$200 (20×).
  - "AI credits are now used solely as an overage mechanism."
- **Fit:** watch, don't adopt. Every piece is weeks old, and Google just shut down the product (Jules) that did this job.

## 4. GitHub Copilot cloud agent and automations

- **What it is:** automations "run Copilot cloud agent automatically on a schedule, in response to events in a repository, or programmatically via the API", and can open a pull request ([automations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-automations)).
- **Scheduling:**
  - Hourly, daily or weekly ([changelog, 2 June 2026](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/)). No cron or time zone is documented.
  - Comment triggers were added on 3 August 2026 ([changelog](https://github.blog/changelog/2026-08-03-trigger-copilot-automations-with-comments/)).
  - Since 28 October 2026, "Cloud automations keep running when your computer is asleep or turned off" (created in VS Code 1.144) ([changelog](https://github.blog/changelog/2026-10-28-create-and-manage-copilot-automations-in-visual-studio-code/)).
- **Repos:** "The repository must be private or internal." Public support is "coming soon" ([automations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-automations), [changelog](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/)). "Each automation is scoped to a single repository."
- **Status:** none of the pages read gives automations a label.
  - The only "generally available" line found is for the cloud agent inside JetBrains IDEs: "Cloud agent is now generally available (no longer behind the Editor Preview feature flag)" ([changelog, 22 June 2026](https://github.blog/changelog/2026-06-22-new-features-and-claude-as-agent-provider-preview-in-jetbrains-ides/); search-result text).
  - **Not verified:** the release status of automations, and of the cloud agent on github.com.
- **Where it runs:**
  - "Cloud (a cloud sandbox), GitHub Actions-based, and Remote" ([about cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent)).
  - A session on Actions has "a maximum execution time of 59 minutes".
  - Compute "draw[s] on the same monthly GitHub account allowance, separate from AI credits", which is the US$12 of Actions compute on GitHub Free.
  - **Not verified:** whether a macOS runner is possible.
- **Pull requests and authorship:**
  - Shared automations act as Copilot. A personal automation's actions "are attributed to the creator, who can't approve their own pull requests" ([automations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-automations)).
  - "Workflows don't run on automation-created pull requests until a user with write access approves them."
  - Copilot "only has the ability to push to a single branch". Commits are authored by Copilot with the requester as co-author, and signed ([risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)).
  - **Not verified:** whether it requests your review automatically.
- **Network:**
  - "By default, Copilot's access to the internet is limited by a firewall", with a recommended allow-list (package registries and the like) plus your own entries ([firewall](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/customize-the-agent-firewall)).
  - It "should not be considered a comprehensive security solution". It doesn't cover other MCP servers or setup steps.
- **Web search: documented both ways.**
  - "Copilot coding agent can now search the web" ([changelog, 16 October 2025](https://github.blog/changelog/2025-10-16-copilot-coding-agent-can-now-search-the-web/)).
  - But the custom-agents reference lists the `web` tool alias as not applicable to Copilot in the cloud ([custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration)).
  - **Not verified.** The firewall allow-list plus the Playwright browser would cover named pricing pages either way.
- **Prompt injection:**
  - Events from users without write access are ignored by default.
  - GitHub "filters hidden characters before passing user input".
  - MCP tools "aren't limited to that repository" ([automations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-automations), [risks](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)).
- **Secrets:** "Agents" secrets are "exposed to the agent as environment variables in its development environment". Values are "masked in Copilot cloud agent session logs" ([secrets and variables](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables)).
  - The exception: "Secrets and variables prefixed with `COPILOT_MCP_` … are only available to MCP servers."
  - So a Fly token could be handed only to an MCP server that fetches logs, out of the agent's shell. Close to Claude's network secret, but you would need that MCP server.
- **Seeing a run:** sessions show "the prompt, session logs, and any pull requests or changes created" ([automations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-automations)).
- **Plans:**
  - Free has no cloud agent. Pro is US$10 with 1,500 AI credits, Pro+ US$39 with 7,000, Max US$100 with 20,000 ([plans](https://docs.github.com/en/copilot/get-started/plans)).
  - "1 AI credit = $0.01 USD", and use is token-based ([billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing)).
  - Credits pass model prices through, for example Claude Sonnet 5.5 and GPT-6.1 Sol at 200 credits per million input tokens and 1,000 per million output ([models and pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)). So Pro's 1,500 credits buy US$15 of model use.
  - Each run "uses GitHub AI Credits and GitHub Actions minutes". An optional per-run credit cap (minimum 30) "stops the run", and daily, weekly or monthly caps stop new runs ([automations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-automations)).
  - **Trial, Not verified:** a "Try free for 30 days" page exists ([Copilot Pro](https://github.com/github-copilot/pro)), but a community thread says new trials were paused in 2026.
- **Fit:**
  - **Server log agent:** good. It is private, and the strongest pull-request guard rails of any option.
  - **Catalogue and price agents:** not until public repos are supported, unless the data lives in a private repo.

## 5. Cursor

- **Automations:** "Cursor Automations run cloud agents in the background, either on a schedule or in response to events" ([automations](https://cursor.com/docs/cloud-agent/automations)).
  - "Choose from preset options or enter a cron expression." Runs "may run with a delay but will not start before the indicated time".
  - "Repo-backed automations can open pull requests after making code changes" (on by default). They can also request reviewers, use MCP servers, and use "computer use (browser, screenshots, recordings)".
  - Memory across runs is on by default. The docs warn that it persists, so untrusted input can leave harmful notes.
  - Status: no label read. The Cloud Agents API is "in public beta" ([API](https://cursor.com/docs/cloud-agent/api/endpoints)).
- **Authorship:** with "Run as: Me", pull requests open as your GitHub account; with a service account (team admins only), they open as `cursor` ([automations](https://cursor.com/docs/cloud-agent/automations)).
- **Where it runs:** "its own isolated VM with a full desktop environment" ([cloud agents](https://cursor.com/help/ai-features/cloud-agents)). The VMs run "in a separate AWS account from the rest of Cursor's production infrastructure", on Firecracker microVMs ([security](https://cursor.com/docs/cloud-agent/security)).
- **Network:**
  - "Internet access is on by default but can be restricted to allowlisted domains, down to allowlist-only" ([security](https://cursor.com/docs/cloud-agent/security)).
  - Modes are "Allow all network access", "Default + allowlist" and "Allowlist only". Git hosts and Cursor's services are always reachable ([secrets and network](https://cursor.com/docs/cloud-agent/security-network)).
- **Secrets:**
  - Secrets are encrypted and "injected as environment variables at runtime" ([security](https://cursor.com/docs/cloud-agent/security)).
  - Runtime Secrets are "redacted from the agent's tool call results, chat transcript, commits" but are "still loaded as environment variables" ([secrets and network](https://cursor.com/docs/cloud-agent/security-network)). Weaker than a proxy: a process in the VM can read them.
- **Prompt injection:** the security page names "an attacker who plants instructions in content the agent reads" and notes "Cloud Agents auto-run terminal commands" ([security](https://cursor.com/docs/cloud-agent/security)).
- **Web search:** **Not verified.** The docs mention the desktop browser, not a search tool.
- **Pricing** ([pricing](https://cursor.com/pricing), [help](https://cursor.com/help/account-and-billing/pricing)):
  - Free US$0; Plus US$8 (Grok models only, "without … Cloud Agents, Automations"); **Premium US$30** (needed for automations); Super US$100; Ultra US$200.
  - Usage is "a weekly pool of usage for Cursor models". "Third Party model usage … must be purchased separately" at API list price.
  - Prices exclude tax. No trial is mentioned.
- **Fit:** capable, and the desktop browser helps with JavaScript-heavy pricing pages. But US$30 a month, secrets readable in the VM, and it is the most expensive entry point here.

## 6. Devin (Cognition)

- **Automations:** "Automations let you wire external events" to Devin sessions; "Under the hood, schedules use the iCalendar RRULE format" ([automations](https://docs.devin.ai/product-guides/automations)).
  - An automation can carry "a network policy to restrict which external hosts the automation's sessions can access", "a maximum ACU (Agent Compute Unit) budget per session", and an invocation limit.
  - Each automation keeps "invocation history" with links to the sessions.
- **The older Schedules feature** (cron, stored as UTC) is "a legacy feature — new scheduled work is created as an automation" ([scheduled sessions](https://docs.devin.ai/product-guides/scheduled-sessions)).
- **Recent changes:** from 2 November 2026, network-policy edits apply to running sessions. From 6 November, automations can run as a service user ([release notes](https://docs.devin.ai/release-notes/2026)).
- **Pull requests:** a setting, "Open PRs as", chooses between Devin ("always opens pull requests as Devin"), User, or User only; "automations and service users still fall back to Devin" ([GitHub integration](https://docs.devin.ai/integrations/gh)). So an automation's pull request is authored by Devin, and you can be asked to review it.
  - "Devin uses the permissions granted at the organization level, not the permissions of the individual user running a session."
  - The app asks for read and write on contents, pull requests, issues, actions and workflows.
  - The docs recommend branch protection; they describe no built-in branch limits.
- **Plans** ([pricing](https://devin.ai/pricing), [self-serve plans](https://docs.devin.ai/admin/billing/self-serve)):
  - Free US$0 ("Light quota"); **Pro US$20**, which includes "Access to cloud agents (Devin Cloud)"; Max US$200; Teams US$80 plus US$40 a seat.
  - Pro's quota is daily and weekly, with no figure published. Extra use draws on on-demand credits "consumed at API pricing".
  - "Automations" are available on self-serve plans. On Teams, "If you run out of credits, Automations stop running."
  - ACUs are now an Enterprise unit.
- **Not verified:** web browsing and search in an automation's session (Devin has a browser, but I didn't read that page), and whether Free covers a scheduled run.
- **Fit:** good controls for US$20: a per-automation network policy, a compute cap, and pull requests authored by Devin so you can review them. Against it: a second subscription with an unpublished quota, and an app with broad write permissions.

## 7. Others

Only tools that really run scheduled or triggered pull-request work are kept.

| Tool | What it does here | Price for one person | Notes |
| --- | --- | --- | --- |
| **Kiro Web (AWS)** | Scheduled tasks: Hourly, Daily or CRON in UTC, "at most once per hour", "up to five schedules per task"; each run opens a pull request if it changed something ([schedule](https://kiro.dev/docs/web/automations/)). "Kiro never merges changes automatically" ([Kiro Web](https://kiro.dev/docs/autonomous-agent/)) | Pro US$20 with 1,000 credits; US$0.04 a credit after. **First upgrade: rest of the month free plus "500 trial credits"** ([pricing](https://kiro.dev/pricing/)) | Warns "The agent learns from and follows instructions in the repository code, even if those instructions are malicious." Network and secrets settings exist but weren't read in detail ([sandbox](https://kiro.dev/docs/web/sandbox/)). Credits per run: not verified |
| **Warp Oz** | `oz schedule create` with cron; runs "on Warp's infrastructure"; a CLI-created schedule opens pull requests under your GitHub account ([scheduled agents](https://docs.warp.dev/platform/triggers/scheduled-agents/)) | Build US$20 includes "$20 of agent usage … at API rates"; Free has "Limited cloud agents access" ([pricing](https://www.warp.dev/pricing)) | In effect pay-per-token with a US$20 floor. Network and secrets not read |
| **Factory (Droids)** | Automations on a cron schedule ("Cron expressions run in UTC"), Slack, GitHub or webhook. Managed "Droid Computers host up to 10 automations each"; automations open fix pull requests ([automations](https://docs.factory.com/software-factory/automations)) | Free (bring your own model sign-in or API key), Pro US$20, Plus US$100, Max US$200 ([pricing](https://factory.com/pricing)) | Which plan includes managed computers: not verified (earlier news said Max and above, [Droid Computers](https://factory.ai/news/droid-computers)). Runs on your own machine are free but need it awake |
| **OpenHands** | Open source (MIT) with a cloud. Automations take cron ("Defaults to UTC"), a 10-minute default timeout (up to 30), your Git token "automatically included", and secrets from Settings ([automations](https://docs.openhands.dev/openhands/usage/automations/creating-automations)) | Free cloud tier "within usage limits", plus your own model key (OpenHands blog; pricing page not read) | Pull-request opening by an automation is not documented on that page. The cheapest if self-hosted, but then you run the scheduler |
| **Augment (Cosmos)** | Cloud agents start "from webhooks, schedules, or events" and "open PRs", in "Fresh sandboxed VMs for every session" ([cloud agents](https://www.augmentcode.com/product/cloud-agents)) | Standard US$20 includes "$20/mo of usage"; extra at API list price "plus a 40% service fee" ([pricing](https://www.augmentcode.com/pricing)) | The 40% fee makes it dearer than paying a model provider directly |

**Dropped:**

- **Amazon Q Developer:** its GitHub app takes no new installations from 18 November 2026 and loses support on 30 January 2027, in favour of Kiro ([AWS docs](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/amazon-q-for-github.html), search-result text).
- **Sourcegraph Amp:** cloud sandboxes ("orbs") but no scheduler found ([pricing](https://ampcode.com/docs/pricing), search only).
- **Mistral Vibe:** remote agents open pull requests ([announcement](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/)), but no scheduled cloud coding sessions found.

## 8. Comparison

Monthly cost is for all three agents, as an estimate. The assumption is the earlier note's workload (§6 there): about 4 catalogue runs, 4 price runs and 30 log runs a month, about US$10–25 at US$2/US$10-per-million-token rates. US$1 ≈ A$1.5.

| Provider and route | Scheduling | Web research in a run | Private-repo pull requests | Secrets and network isolation | Cost a month, 3 agents (estimate) | Maturity |
| --- | --- | --- | --- | --- | --- | --- |
| **Claude Code cloud scheduled tasks** (earlier note, A) | Cron, hourly minimum | Hosted search; fetch through an allow-list | Yes; opened as you | Network secrets held by a proxy; per-environment allow-list | **A$0 extra** | Research preview |
| Claude Code GitHub Action (earlier note, B) | Actions cron | Yes; runner has open internet | Yes; Claude app | Secrets on the runner; no allow-list | A$0 extra (Actions free on the public repo) | v1 |
| **OpenAI: Codex action / `codex exec` on Actions** | Actions cron | Hosted search outside the sandbox (live mode) | Yes, via a separate PR job | API key behind a proxy, `drop-sudo`; sandbox has no network by default; Fly token would be on the runner | US$5–25 API (`gpt-6.1-terra` to `-sol`) | Released; profiles beta |
| OpenAI: Codex cloud | **None** (only `codex cloud exec` fired from elsewhere) | Allow-list per environment; search not documented | Yes; author not verified | Network secrets via proxy (as Claude) | Plus US$20 | No label; scheduling not offered |
| OpenAI: Codex desktop scheduled tasks | RRULE | Hosted search | Yes, from your Mac | Your Mac | Plus US$20; Mac must be on | No label |
| **Google: Antigravity** | Cron (app) | Not verified | Remote agents: GitHub OAuth; PRs not verified | Not verified | Google AI Pro US$20 | Remote agents rolled out 9 Nov 2026 |
| Google: Gemini CLI action | Actions cron | Search grounding, 5,000 free a month | Via `gh` in the run | Secrets on the runner | US$4–19 paid key (Gemini 3.8 Flash); maybe US$0 on a free key (not verified) | Gemini CLI retired for consumer plans |
| Google: Jules | Had it | Had it | Had it | Had it | n/a | **Closing 31 Dec 2026** |
| **GitHub Copilot automations** | Hourly, daily, weekly | Unclear; firewall allow-list plus Playwright | Yes; **private repos only**; Copilot or you as author | Firewall allow-list; secrets are env vars, except `COPILOT_MCP_` ones (MCP servers only) | Pro US$10 (1,500 credits ≈ US$15 of model use) to Pro+ US$39; plus Actions minutes | Launched 2 June 2026; no status label read |
| **Cursor** | Cron or presets | Desktop browser; search not verified | Yes; as you or `cursor` | Allow-list modes; secrets readable as env vars, redacted from logs | Premium US$30 (+ third-party models extra) | API public beta |
| **Devin** | RRULE (automations) | Browser; not verified | Yes; automations open them as Devin | Network policy per automation; compute cap per session | Pro US$20 + credits past quota | Released |
| Kiro Web | Hourly, daily, cron | Browser in sandbox; search not verified | Yes | Domain controls (not read in detail) | Pro US$20 (+US$0.04 a credit) | No label |
| Warp Oz | Cron | Not verified | Yes; as you | Not read | Build US$20 (includes US$20 at API rates) | Released (Oz launched 2026) |
| Factory | Cron (UTC) | Not verified | Yes | Not read | Pro US$20+; managed computers' plan not verified | Released |
| OpenHands | Cron | Not verified | Token included; PR not documented | Secrets in Settings | Free tier + model key | Released |

## 9. Proof-of-concept plan per provider

**The common POC:** the price agent for one network. Read Evie Networks' published price page, compare it with one number in a JSON file in a **throwaway** repo, and open one pull request with the source link and the quoted sentence. Run it once by hand, then once on its schedule. Success means the run read the live page, the PR is correct, and you can see what it did.

| Provider | Minimal POC | Account or plan | Free tier or trial covers it? | Setup effort | Blockers from Australia |
| --- | --- | --- | --- | --- | --- |
| **OpenAI (Codex action)** | Public throwaway repo; workflow on `schedule` + `workflow_dispatch`: job 1 runs `openai/codex-action` with `--search`/`web_search="live"`, `contents: read`, writes a patch; job 2 (`contents: write`, `pull-requests: write`) runs `gh pr create`. Model `gpt-6.1-terra` | OpenAI API account with prepaid credit and a project budget | No free tier read; a run costs cents (estimate). Actions free on a public repo | 1–2 hours | None known. **Not verified:** minimum prepaid amount |
| OpenAI (Codex cloud, for comparison) | Same prompt as a manual cloud task on a Plus plan, environment allow-listing the Evie page | ChatGPT Plus US$20 | No (Free and Go lack Codex on the web) | 30 minutes | None known |
| **GitHub Copilot** | **Private** throwaway repo; one automation, daily, with a per-run cap of 100 credits; firewall custom allow-list with the Evie domain | Copilot Pro US$10 | Trial not verified (may be paused) | 30–60 minutes | None known |
| **Google (Antigravity)** | Cloud project on the throwaway repo; `/automation` with a daily cron; check whether it runs with the laptop shut and opens a PR | Google AI Pro US$20, personal @gmail.com account | Remote agents not on Free | 1 hour, plus finding out what works | Remote agents' country list not stated. **Not verified** in Australia |
| Google (Gemini CLI action) | As the Codex action POC, with `run-gemini-cli` and an AI Studio key | Free key first; paid if refused | Maybe (not verified for Gemini CLI after 18 June) | 1–2 hours | None known |
| **Cursor** | Automation with a cron trigger on the throwaway repo; network "Allowlist only" plus the Evie domain | Premium US$30 | No (Free and Plus exclude automations) | 30–60 minutes | None known; prices exclude tax |
| **Devin** | Automation with a schedule trigger, network policy to the Evie domain, ACU or credit cap | Pro US$20 | Free's "light quota" may not include cloud runs (not verified) | 30–60 minutes | None known |
| Kiro | Kiro Web scheduled task (Daily) on the throwaway repo | Pro US$20 | **Yes, effectively:** first upgrade gives the rest of the month free + 500 trial credits | 30–60 minutes | Kiro Web for Identity Center orgs is us-east-1 only; individuals: not stated |
| Warp Oz | `oz schedule create` with a cron and an environment for the repo | Free ("Limited cloud agents access") or Build US$20 | Possibly on Free (not verified) | 1 hour | None known |

**What each POC must check**, beyond "did it open a PR":

- Did it read the **live** page, or a cached or search-snippet version?
- Did it quote the sentence it used?
- How much did the run cost, and where is that shown?
- Can you see every command and fetch it made?

## 10. Ranked recommendation for this project

1. **Claude Code cloud scheduled tasks, as planned** (earlier note). One plan, A$0 extra, network secrets held outside the VM, per-environment allow-lists. Its weak spots:
   - pull requests are opened as you, so nobody can be asked to review;
   - there is no hard write-split between reading the web and pushing;
   - it is a research preview.
2. **Claude Code GitHub Action on the public `charge-line-data` repo**, if option 1's guard rails feel too soft for agents that read the web. Actions minutes are free on a public repo, the subscription token still pays, and the pull request comes from an app, so you can be asked to review. Copy Codex's two-job pattern: the agent job read-only, a second job opening the PR.
3. **OpenAI Codex action on Actions** is the best non-Claude choice, and the right POC if you want a second opinion on quality.
   - It beats Claude cloud tasks on the read-only agent job, macOS runners for Swift tests, and pay-per-use with no subscription.
   - It loses on cost (US$5–25 a month versus A$0), on the Fly token sitting on the runner, and on no cloud scheduler of its own.
4. **GitHub Copilot automations**, for the **server log agent only**, if you ever want it off the Claude plan.
   - It beats Claude cloud tasks on pull-request protections, a per-run spend cap and GitHub-native triggers.
   - It loses on the extra US$10–39 a month, no public repos, and unclear web search.
5. **Kiro, Devin, Warp Oz, Cursor:** all do the job; none adds what the agents need. Try Kiro only if you want a no-cost look at another vendor (trial credits). Cursor is the dearest entry point.
6. **Google:** wait. Jules is closing, Gemini CLI is API-key-only, and Antigravity's cloud pieces are days old. Revisit in a few months.

## 11. Not verified

**OpenAI:**

- Codex cloud: the VM's operating system; who authors a pull request it opens; whether it can request a reviewer; whether a task started with `codex cloud exec` opens the PR by itself; whether web search is available in cloud tasks.
- Codex Team Tasks: whether they can use a Codex cloud environment and open a pull request.
- ChatGPT scheduled-task caps (3, 5, 10, 15 by plan, hourly on paid plans) and "ChatGPT agent replaced by ChatGPT Work": search-result text only; help.openai.com refused automated reading.
- Whether ChatGPT-plan sign-in works in CI on a personal Plus plan.
- Whether live web search works inside `openai/codex-action` with the `:workspace` profile.
- That the Claude Code action also runs on a macOS runner.
- The minimum prepaid amount for an OpenAI API account.
- Community reports of Create PR failures: forum posts, not a primary source.

**Google:**

- Whether a free AI Studio key still runs Gemini CLI after 18 June 2026.
- Whether Antigravity automations run with the computer off, or as remote agents.
- Whether remote agents open pull requests; their network rules, secrets and web search.
- Availability of remote agents in Australia.

**GitHub Copilot:**

- Release status of automations, and of the cloud agent on github.com.
- Web search in the cloud agent: the docs conflict.
- macOS runners; automatic review requests.
- Whether the 30-day Pro trial is still offered.
- Whether 1,500 credits cover these runs (estimate only).

**Cursor:** web search tool in cloud agents; release status of automations; no trial mentioned.

**Devin:** browsing and search in automations; Pro's quota size; whether Free covers scheduled cloud runs; whether the GitHub integration works on a personal account (the docs speak of organisations).

**Others:**

- Kiro: credits used per run; network and secret details; individual-account region.
- Warp: network, secrets, overage price; whether Free covers a POC.
- Factory: which plan includes managed Droid Computers.
- OpenHands: whether automations open pull requests; cloud pricing (blog only).
- Augment: which plan includes scheduled triggers.
- Amazon Q Developer dates: search-result text of AWS docs.
- Amp and Mistral: dropped on search results only.

**General:**

- Whether Australian GST is added by each vendor.
- Every cost marked "estimate", including the per-provider monthly figures in §8.

## Sources

- OpenAI Codex: [pricing](https://learn.chatgpt.com/docs/pricing), [cloud](https://learn.chatgpt.com/docs/cloud), [cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments), [agent internet access](https://learn.chatgpt.com/docs/cloud/internet-access), [web search](https://learn.chatgpt.com/docs/web-search), [scheduled tasks (app)](https://learn.chatgpt.com/docs/automations?surface=app), [scheduled tasks (web)](https://learn.chatgpt.com/docs/automations?surface=web), [scheduled tasks](https://learn.chatgpt.com/docs/automations), [GitHub integration](https://learn.chatgpt.com/docs/third-party/github), [GitHub Action](https://learn.chatgpt.com/docs/github-action), [non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode), [CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [`openai/codex-action`](https://github.com/openai/codex-action), [API pricing](https://developers.openai.com/api/docs/pricing), [forum thread with OpenAI reply](https://community.openai.com/t/codex-cloud-web-has-compounding-reliability-observability-and-workflow-problems-that-make-long-running-tasks-difficult-to-trust/1397259), [ChatGPT scheduled tasks help](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt)
- Google: [Jules changelog](https://jules.google/docs/changelog/), [Jules usage limits](https://jules.google/docs/usage-limits/), [Jules scheduled tasks](https://jules.google/docs/scheduled-tasks/), [Gemini CLI transition](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/), [`run-gemini-cli`](https://github.com/google-github-actions/run-gemini-cli), [Gemini API pricing](https://aistudio.google.com/docs/pricing), [Antigravity /automation](https://antigravity.google/docs/commands/automation), [remote agents](https://antigravity.google/docs/remote-agents/), [Antigravity changelog](https://antigravity.google/docs/changelog/), [Antigravity plans](https://antigravity.google/blog/changes-to-antigravity-plans/)
- GitHub Copilot: [automations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-automations), [about cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent), [risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations), [firewall](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/customize-the-agent-firewall), [plans](https://docs.github.com/en/copilot/get-started/plans), [individual billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing), [models and pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing), [custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration), changelogs: [2 June 2026](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/), [3 August 2026](https://github.blog/changelog/2026-08-03-trigger-copilot-automations-with-comments/), [28 October 2026](https://github.blog/changelog/2026-10-28-create-and-manage-copilot-automations-in-visual-studio-code/), [16 October 2025](https://github.blog/changelog/2025-10-16-copilot-coding-agent-can-now-search-the-web/)
- Cursor: [automations](https://cursor.com/docs/cloud-agent/automations), [cloud agents](https://cursor.com/help/ai-features/cloud-agents), [security](https://cursor.com/docs/cloud-agent/security), [secrets and network](https://cursor.com/docs/cloud-agent/security-network), [API](https://cursor.com/docs/cloud-agent/api/endpoints), [pricing](https://cursor.com/pricing), [pricing help](https://cursor.com/help/account-and-billing/pricing)
- Devin: [automations](https://docs.devin.ai/product-guides/automations), [scheduled sessions](https://docs.devin.ai/product-guides/scheduled-sessions), [release notes 2026](https://docs.devin.ai/release-notes/2026), [self-serve plans](https://docs.devin.ai/admin/billing/self-serve), [pricing](https://devin.ai/pricing), [GitHub integration](https://docs.devin.ai/integrations/gh)
- Others: [Kiro Web](https://kiro.dev/docs/autonomous-agent/), [Kiro schedule](https://kiro.dev/docs/web/automations/), [Kiro sandbox](https://kiro.dev/docs/web/sandbox/), [Kiro pricing](https://kiro.dev/pricing/), [Warp scheduled agents](https://docs.warp.dev/platform/triggers/scheduled-agents/), [Warp pricing](https://www.warp.dev/pricing), [Factory automations](https://docs.factory.com/software-factory/automations), [Factory pricing](https://factory.com/pricing), [OpenHands automations](https://docs.openhands.dev/openhands/usage/automations/creating-automations), [Augment cloud agents](https://www.augmentcode.com/product/cloud-agents), [Augment pricing](https://www.augmentcode.com/pricing), [Amazon Q Developer for GitHub](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/amazon-q-for-github.html), [Mistral Vibe remote agents](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/)
- Earlier note: [Maintenance agents, 12 November 2026](2026-11-12-maintenance-agents.md)
