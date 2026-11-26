# Agentic OSS Engineering Playbook

*Synthesized from primary-source GitHub API audits of **35 public agentic coding, orchestration, and skill-stack repositories** (**3,040,947 / ~3.04M combined GitHub stars**, snapshot date: **2026-11-25**). Independently audited and red-teamed by Codex (`gpt-6.2-astra`), Claude (`claude-opus-5-5`), and Grok (`grok-4.7`) — see [`MULTI_MODEL_REVIEW.md`](MULTI_MODEL_REVIEW.md).*

Every recommendation below is backed by real configuration files, YAML CI workflows, lint plugins, and commit histories captured under [`data/`](../data/).

---

## Executive Summary: 6 Observed Patterns (With Counter-Examples & Caveats)

1. **Mechanical invariants outperform prose instructions — though large instruction files still ship.**
   - Most high-velocity TypeScript codebases in the cohort (`t3code`, `orca`, `Paradev`, `emdash`, `opencode`, `openclaw`, `paseo`, `sandcastle`) encode recurring failure modes directly into **`oxlint` / Biome custom plugins, `ast-grep` rules, or static ratchets** rather than relying solely on `AGENTS.md`.
   - *Counter-examples & caveats:* Large instruction files do not automatically stall a repo — `oh-my-openagent` carries a 70.8 KB `AGENTS.md` (with a 3-month-stale header) and still landed 50 commits in 19.2 hrs at 71.1k★, and `gstack` splits 54 KB across `AGENTS.md`/`CLAUDE.md` at 142.6k★. Rust-first `codex` has no root `AGENTS.md` and ships every 14.7 hrs. Mechanical rules prevent silent regressions; prose still helps as a lean router.

2. **Contributor gating controls open backlog size, at a discoverability trade-off.**
   - GitHub's `open_issues_count` combines **open issues and open pull requests**. In an era of 90-second AI PRs, open trackers accumulate massive queues, while default-closed gates stay small by construction:
     - `openai/codex` (136.4k★, open tracker + paid user base): **28,619** open issues + PRs
     - `manaflow-ai/cmux` (29.0k★, autonomous agent factory): **11,218**
     - `stablyai/orca` (137.8k★, 50 commits / 3.2 hrs, `Fixes #` gate for outsiders): **9,918**
     - `openclaw/openclaw` (395.2k★, 20-PR cap + bot sweepers): **9,182**
     - `pingdotgg/t3code` (78.8k★, `VOUCHED.td` + PR limits): **3,681**
     - `aaif-goose/goose` (57.0k★, `Ready`-board gate): **512**
     - `obra/superpowers` (326.5k★, maintainer-reported 94% PR rejection rate): **372**
     - `earendil-works/pi` (123.8k★, default-closed `lgtmi`/`lgtm` auto-close): **307** (Codex has 93.2× as many open items, though this reflects closing policy and product/user-base differences as much as review load)
   - *Counter-examples & caveats:* `pi`'s 307 is partly true by construction because unapproved items are auto-closed on arrival (which reduces public bug discoverability). `bolt.diy` (`2`) uses `stale.yml`, and `symphony` (`0`) is a reference spec with no community intake. Normalized by stars, `paseo` (`25.3k★`, `2,203` open = `11` stars/item) has a heavier open queue than open-tracker `opencode` (`55` stars/item) despite its *"PRs closed by default"* policy.
   - `getpaseo/paseo` still captures the real bottleneck cleanly in `CONTRIBUTING.md`: *"I can prompt an agent to write code just as you can. The bottlenecks are choosing what to build, shaping it, verifying its behavior, and taking responsibility for its maintenance."*

3. **Match CI workflow count to team size — avoid both zero PR CI and unstaffed CI factories.**
   - Across our 35 repos, most lean high-signal codebases run **~8–30 YAML workflows** (`sandcastle`: 8, `paseo`: 12, `pi`: 16, `spec-kit`: 19, `opencode`: 21, `Paradev`: 22, `OpenHands`: 25, `t3code`: 29; `emdash` runs 6).
   - **Under-gated (`0–1` workflows):** `1code` (0 public workflows; one-way mirror) stopped receiving pushes after 7 weeks. `slopus/happy` (1 workflow) explicitly bans adding Actions for cost reasons and works because a tight 2-person core pushes directly to `main`. `superpowers` (0 workflows) relies on an external CLI eval repo.
   - **Heavy CI stacks (`38–231` workflows):** Large multi-engineer or company-backed teams sustain heavier CI (`gstack`: 38, `gemini-cli`: 47, `orca`: 67 with 6 cache-warmup/runner workflows, `openclaw`: 133). At the extreme (`cmux`: **231** YAML workflows), **17 of 20 stored Nov 25 commit subjects** (~85%, authored by `teamleaderleo` on a single day) touched CI, runner pools, or release automation — a vivid warning of how automation overhead can dominate a small team's day.

4. **Commit tests only for costly invariants, verify them independently, and disclose honestly.**
   - Agents game soft checks in two opposite ways: flooding PRs with brittle mock/UI unit tests, or weakening tests and treating skipped CI jobs as coverage.
   - Combining the cohort's strongest defenses resolves both failure modes:
     1. **Test selectively (`orca`):** `"Tests are the exception"` — commit automated tests only where a silent regression is costly (parsers/codecs, security boundaries, persistence/migrations, concurrency/state machines, cross-platform paths), delete brittle UI/mock tests you touch, and track test-vs-prod LoC on PRs (`pr-test-loc.yml`).
     2. **Keep grading independent (`OpenHands`):** `verify-skill-isolation.yml` blocks PRs from editing both production code and `.agents/skills/verify-*/` in the same PR; `stryker-diff.mjs` runs diff-scoped mutation testing on critical paths.
     3. **Treat self-run QA as disclosure, not independent proof (`cmux`, `oh-my-openagent`, `beads`):** Require `### Observed / Not run`, keep local QA captures gitignored (`.omo/evidence/` + `sha256sum` + CI audit if tracked), verify filtered tests executed >0 subtests, and answer `NOT_ENOUGH_INFO` when evidence runs out.

5. **Four repos archived or sunset — from distinct failure modes (scope, lock-in, mirror decay, and security).**
   - With `n = 4` (3 `archived=true`, 1 README sunset notice), this is a postmortem catalog rather than a statistical law — especially since heavily multi-language repos backed by large teams (`openclaw`, `cmux`, `oh-my-openagent`) continue shipping:
     - `21st-dev/1code` (5.6k★, Archived; 7 weeks creation-to-last-push): One-way public mirror (`sync-to-public.sh`) with zero public CI/tests, dual lockfiles, and stale WIP docs (exact business reason for archival not stated in repo).
     - `BloopAI/vibe-kanban` (28.8k★, Sunsetting per README): Strong Rust craft (`ts-rs`, `sqlx`), carrying 30 Rust crates + ElectricSQL + WebRTC relay + Tauri + Rust nightly on a small core team.
     - `RooCodeInc/Roo-Code` (24.2k★, Archived May 2026): Remained coupled to a VS Code extension while surviving peers (`Cline`, `OpenHands`, `Goose`) decoupled into standalone SDKs + ACP.
     - `gsd-build/get-shit-done` (64.1k★, Archived May 2026): **Security/governance event** — commit `126b6b9e` warned the repo *"appears compromised"* and README migrated users to `open-gsd/gsd-core`.

6. **Skill stacks organize workflow and safety, not raw bug-fix rate (one self-reported benchmark).**
   - `garrytan/gstack` published a rare self-reported head-to-head benchmark in its `README.md`: on 100 real GitHub bugs/features using Opus 5.5, the model solved **58% (58/100) with `gstack`** vs. **61.6% (61/99, one unscored) without it** (and 29/60 in each arm on security fixes). That is one model and one vendor's task set — it does not generalize to every skill stack, nor prove a numeric multiplier for mechanical gates — but it is a healthy reminder not to treat prompt stacks as a substitute for deterministic repo checks.
   - The durable mechanical ideas in Chunk 6 are deterministic: `mattpocock/sandcastle`'s 5-category type-aware `oxlint` + automated `lint-shrink.yml` PR bot, `mattpocock/skills`'s YAML frontmatter validation + Claude/Codex invocation parity, `gstack`'s token-budget & egress-receipt tests, `OpenSpec`'s CLI startup-module budget, and `pstack-claude`'s `tools/forks.json` fork tracker.

---

## Methodology, Confounders & Not Covered

- **Snapshot & selection:** All 35 JSON snapshots were collected on **2026-11-25** via `scripts/collect_chunk.py` (top high-star public repos across worktree GUIs, harnesses, orchestrators, specialists, and skill stacks). `pingdotgg/t3code` serves as the study's reference baseline (`RUBRIC.md`) and should be read with that baseline framing in mind.
- **Key confounders to keep in mind when comparing rows:**
  - **Backing & team size:** OpenAI (`codex`, `symphony`), Google (`gemini-cli`), GitHub (`spec-kit`), YC/VC teams (`orca`, `Paradev`, `cmux`, `OpenHands`), foundations (`goose`), and solo/2-person maintainers (`pi`, `happy`, `mattpocock`, `obra`) operate under totally different review budgets.
  - **Metrics caveats:** `Open Issues` = GitHub `open_issues_count` (issues + PRs combined). `Workflows` = exact `.yml`/`.yaml` files in `.github/workflows/` (one file can contain many jobs). `Last-50 Velocity` = exact author-timestamp span of the latest 50 commits (47 for `symphony`) — a point-in-time snapshot, not a yearly average. `ai_coauthor_pct` is omitted from the main quality matrix because commit-trailer regexes read `0%` on teams that strip trailers (`orca`, `codex`, `Paradev`).
- **Notable repos outside this 35-repo wave (worth auditing in a future Chunk 7):** **Aider** (publishes self-authored release share), **Zed** (originator of ACP), **Kilo Code** (thriving Cline/Roo fork countering the "trapped fork" narrative), **Continue** (IDE-extension-to-agent pivot), **SWE-agent / SWE-bench**, and non-agent OSS AI-governance pioneers (**Ghostty**, **curl**, **Gentoo/NetBSD**).

---

## Master 35-Repository Matrix

*Workflow counts reflect exact `.yml`/`.yaml` files in `.github/workflows/`. `Open` reflects GitHub `open_issues_count` (open issues + open PRs).*

| Chunk | Repository | Stars | Open | Status | Primary Stack | YAML CI | Last-50 Span | Signature Practice to Know |
| --- | --- | ---: | ---: | --- | --- | ---: | --- | --- |
| Base | [`pingdotgg/t3code`](../RUBRIC.md) | 78.8k | 3,681 | Active | TS (226.7 MB, Effect, Vite+, Electron, RN) | 29 | 50 / **7.0 hrs** | `oxlint-plugin-t3code`, `VOUCHED.td`, `evals/`, `agent-context-budget` |
| C1 | [`stablyai/orca`](../chunks/chunk-01-direct-rivals/orca.md) | **137.8k** | 9,918 | Active | TS (143.7 MB, Electron, Web, Mobile, `orcad`, Ghostty) | 67 | 50 / **3.2 hrs** | `"Tests are the exception"`, `pr-test-loc`, `## Performance` CI gate, `quadratic-buffer-concat` oxlint |
| C1 | [`ParadevAI/Paradev`](../chunks/chunk-01-direct-rivals/paradev.md) | 16.6k | 1,263 | Active | TS (35.2 MB, Bun, Turbo, Electron/Next/Expo, Drizzle) + TLA+ | 22 | 50 / **3.2 days** | Domain `noRestrictedImports` in Biome, `paradev schema`, 2-min test budget |
| C1 | [`BloopAI/vibe-kanban`](../chunks/chunk-01-direct-rivals/vibe-kanban.md) | 28.8k | 537 | **Sunsetting** | 30-crate Rust (`axum`/`sqlx`/`ts-rs`/`tauri`) + React | 9 | 50 / **7.5 mos** | `ts-rs` codegen check, `sqlx` offline check (warning: scope sprawl) |
| C1 | [`generalaction/emdash`](../chunks/chunk-01-direct-rivals/emdash.md) | 6.3k | 92 | Active | TS (21.2 MB, pnpm, Nx, Electron, Drizzle, MobX) | 6 | 50 / **22 days** | `respectEslintDisableDirectives: false`, self-pruning allowlists, sole-writer DB lint |
| C1 | [`21st-dev/1code`](../chunks/chunk-01-direct-rivals/1code.md) | 5.6k | 45 | **Archived** | TS (5.1 MB, Electron, Bun, tRPC, Drizzle) | **0** | Archived Mar '26 | Ephemeral NDJSON log server (`localhost:7799/log`); 0 public CI / one-way mirror |
| C2 | [`anomalyco/opencode`](../chunks/chunk-02-agent-harnesses/opencode.md) | 229.1k | 4,172 | Active | TS (Effect v4, Bun, Solid/OpenTUI) + Rust daemon | 21 | 50 / **12.3 hrs** | `anti-slop` oxlint plugins, unit-tested `ast-grep`, Miri, 7 triage workflows |
| C2 | [`earendil-works/pi`](../chunks/chunk-02-agent-harnesses/pi.md) | 123.8k | **307** | Active | TS (npm workspaces, erasable TS, Biome) | 16 | 50 / **1.7 days** | Default-closed `lgtmi`/`lgtm` auto-close gate, multi-agent Git safety, GritQL Biome |
| C2 | [`openai/codex`](../chunks/chunk-02-agent-harnesses/codex.md) | 136.4k | 28,619 | Active | Rust (90.7 MB, Bazel/Cargo) + pnpm SDKs | 28 | 50 / **14.7 hrs** | 7-day npm cooldown (`minimumReleaseAge: 10080`), `CI required` aggregator |
| C2 | [`google-gemini/gemini-cli`](../chunks/chunk-02-agent-harnesses/gemini-cli.md) | 109.1k | 751 | Active | TS (npm workspaces, Ink, esbuild/SEA) | 47 | 50 / **18.1 days** | 38 `*.eval.ts` files + `eval-gate` environment approval, zero-checkout drift check |
| C3 | [`cline/cline`](../chunks/chunk-03-autonomous-and-ide/cline.md) | 71.9k | 1,833 | Active | TS (Bun, SDK + CLI + VS Code gRPC + Tauri) | 17 | 50 / **19.5 days** | 34-line trap-only `AGENTS.md`, strip agent promo footers, fixture installer tests |
| C3 | [`RooCodeInc/Roo-Code`](../chunks/chunk-03-autonomous-and-ide/roo-code.md) | 24.2k | 1,025 | **Archived** | TS (pnpm, Turbo, VS Code ext + webview) | 7 | Archived May '26 | 5-line single-invariant `AGENTS.md`, `.roomodes`, clean pre-archive strip |
| C3 | [`OpenHands/OpenHands`](../chunks/chunk-03-autonomous-and-ide/openhands.md) | 94.3k | 1,252 | Active | TS (React 19, Vite 8, Electron Agent Canvas) | 25 | 50 / **2.0 days** | **`verify-skill-isolation.yml`** (`.agents/skills/verify-*/`), Stryker diff mutation, `HUMAN:` PR check |
| C3 | [`aaif-goose/goose`](../chunks/chunk-03-autonomous-and-ide/goose.md) | 57.0k | 512 | Active | Rust (`oi-kit` + ACP + `rmcp`) + Electron | 39 | 50 / **4.8 days** | `Ready`-board gate, `check-lean-size`, `wasm32`, `git cherry` release check |
| C4 | [`openclaw/openclaw`](../chunks/chunk-04-agent-native-orchestration/openclaw.md) | 395.2k | 9,182 | Active | TS (**474.7 MB**) + Swift/Kotlin/Rust, Kysely | 133 | 50 / **2.3 hrs** | <20 KB `AGENTS.md` ("cite an incident"), all-error `oxlint`, `prefix-stability` test |
| C4 | [`paperclipai/paperclip`](../chunks/chunk-04-agent-native-orchestration/paperclip.md) | 116.9k | 6,812 | Active | TS (157.8 MB, Express/React/Drizzle/PG) + Rust | 41 | 50 / **14.5 hrs** | `grep`-indexed `rules/*.mdc`, `pnpm verify` (exit 2), real PG `pg_dump`/restore CI |
| C4 | [`openai/symphony`](../chunks/chunk-04-agent-native-orchestration/symphony.md) | 28.2k | **0** | Reference | `SPEC.md` + 914 KB Elixir/OTP + Burrito | 4 | 47 / **195 days** | Spec-as-product ("implement `SPEC.md` in your language"), `mix pr_body.check` |
| C4 | [`gastownhall/beads`](../chunks/chunk-04-agent-native-orchestration/beads.md) | 29.0k | 1,828 | Active | Go (51.4 MB) + Bazel + Dolt | 23 | 50 / **8.0 days** | `gascity-eddie[bot]` (41/50 commits), `NOT_ENOUGH_INFO`, "verify test ran" |
| C5 | [`getpaseo/paseo`](../chunks/chunk-05-specialists/paseo.md) | 25.3k | 2,203 | Active | TS (51.2 MB, Expo/Electron, Noise NK relay) | 12 | 50 / **2.4 days** | Anti-slop `Doc voice`, per-file/API `no-sync-io` allowlist, "PRs closed by default" |
| C5 | [`slopus/happy`](../chunks/chunk-05-specialists/happy.md) | 24.8k | 1,154 | Active | **Native Swift (22.3 MB) + Kotlin (14.6 MB)** + TS | **1** | 50 / **8.4 days** | Incident-cited `main == origin/main` release rule, CI-cost ban, `env:up/seed` CLI |
| C5 | [`manaflow-ai/cmux`](../chunks/chunk-05-specialists/cmux.md) | 29.0k | 11,218 | Active | **Swift (115.2 MB)** + Py/Rust/TS + Ghostty (BSL server dirs) | **231** | 50 / **9.7 hrs** | `REVIEW.md`, `verify-local.py --receipt -`, compiled-app reuse (warning: CI bloat) |
| C5 | [`smtg-ai/claude-squad`](../chunks/chunk-05-specialists/claude-squad.md) | 8.9k | 54 | Quiet | **263 KB Go** (Bubble Tea) + `tmux` + worktrees | 5 | 50 / **17 mos** | Unix composition over reinvention, `golangci-lint --only-new-issues` |
| C5 | [`stackblitz-labs/bolt.diy`](../chunks/chunk-05-specialists/bolt-diy.md) | 20.1k | 2 | Active | TS (3.4 MB, React Router, WebContainers, AI SDK) | 13 | 50 / **5.3 days** | Prod Docker `curl` smoke test in CI, `.performance-budgets.json` (`stale.yml` trims issues) |
| C5 | [`code-yeongyu/oh-my-openagent`](../chunks/chunk-05-specialists/oh-my-openagent.md) | 71.1k | 2,823 | Active | TS (58.0 MB) + Rust (5.3 MB), 45 pkgs, Bun (SUL-1.0) | 43 | 50 / **19.2 hrs** | Local `.omo/evidence/` + `sha256sum` proof + anti-commit test, hermetic `$HOME` tests |
| C5 | [`zgsm-ai/costrict`](../chunks/chunk-05-specialists/costrict.md) | 4.5k | 14 | Slowing | TS (15.1 MB, Roo Code enterprise fork, pnpm) | 9 | 50 / **3.6 mos** | 1-line English commit rule (92% conv), 40+ CVE overrides, workspace-trust MCP gate |
| C6 | [`mattpocock/skills`](../chunks/chunk-06-skill-stacks/mattpocock-skills.md) | 332.8k | 251 | Active | Markdown skills + 20 KB Shell/JS, Changesets | 4 | 50 / **7.1 wks** | 5-bucket lifecycle, fresh-context subagents, Claude+Codex invocation parity, YAML check |
| C6 | [`mattpocock/sandcastle`](../chunks/chunk-06-skill-stacks/mattpocock-sandcastle.md) | 9.3k | 137 | Active | TS (2.6 MB, TS 7, Effect, `oxlint-tsgolint`) | 8 | 50 / **5.9 days** | **5-cat `oxlint` straitjacket + `lint-shrink.yml` bot**, real `bwrap` CI, `docs-guide.test.ts` |
| C6 | [`obra/superpowers`](../chunks/chunk-06-skill-stacks/superpowers.md) | 326.5k | 372 | Active | Markdown skills + 520 KB Shell/JS, 15+ harnesses | **0** | 50 / **4.0 mos** | **94% PR rejection rate**, external Quorum eval lab, `"react todo list"` bootstrap test |
| C6 | [`github/spec-kit`](../chunks/chunk-06-skill-stacks/spec-kit.md) | 151.4k | 230 | Active | Python (11.9 MB, `uv`, Typer, MCP SDK) | 19 | 50 / **7.0 days** | **Firewall-sandboxed `gh-aw` agentic workflows**, Evidence Gate, Ruff `S602`–`S605` |
| C6 | [`garrytan/gstack`](../chunks/chunk-06-skill-stacks/gstack.md) | 142.6k | **45** | Active | TS (**45.1 MB**), Bun, Playwright/Aside CLIs | 38 | 50 / **1.8 days** | Self-reported **58% vs 61.6%** eval, `egress-receipt-wiring`, token-budget ratchets, `$150/wk` cap |
| C6 | [`Fission-AI/OpenSpec`](../chunks/chunk-06-skill-stacks/openspec.md) | 75.7k | 214 | Active | TS (5.8 MB, Node 22+, pnpm 10, Vitest 5) | 4 | 50 / **25 days** | **`startup-modules.test.ts`** CLI cold-start guard, GHSA-annotated overrides, 2-PR features |
| C6 | [`gsd-build/get-shit-done`](../chunks/chunk-06-skill-stacks/get-shit-done.md) | 64.1k | 0 | **Archived** | 7.3 MB CJS + 2.6 MB TS SDK, `node:test` | 20 | Archived May '26 | `prompt-injection-scan.sh`, ADRs (archived after *"appears compromised"* warning → `open-gsd`) |
| C6 | [`bmad-code-org/BMAD-METHOD`](../chunks/chunk-06-skill-stacks/bmad-method.md) | 55.7k | 116 | Active | Python (1.8 MB, `uv`, Jinja2, Ruff) + Astro | 5 | 50 / **27 days** | *"Length and ambiguity are paid on every run... Prefer deleting an instruction to hedging it"*, PEP 723 |
| C6 | [`backnotprop/pstack`](../chunks/chunk-06-skill-stacks/pstack.md) | 5.2k | 2 | Active | Agent Skills + TLA+ (48.8 KB) + Lean (52 KB) | 0 | 7 / **27.9 days** | Port of Lauren Tan's (`poteto`) Cursor `pstack`: `/create-formal-verification-skill` (TLA+/Lean) |
| C6 | [`michael-denyer/pstack-claude`](../chunks/chunk-06-skill-stacks/pstack.md) | 4.9k | 16 | Active | 1.8 MB TS/JS multi-harness `pstack` port + TLA+/Lean | 6 | 50 / **6.5 days** | `tools/forks.json` CI check, `--check-rules`, `watch-pr` prompt-injection hardening |

---

## Tier 1 — Steal Immediately (High ROI, < 1 Day Each)

1. **Trap-Only, Incident-Cited `AGENTS.md` + Safe `@AGENTS.md` Include:**
   - **Sources:** `openclaw` (*"A new rule cites an incident"*, <20 KB cap), `cline` (34 lines), `happy` (40 lines), `BMAD` (*"Prefer deleting an instruction to hedging it"*), `t3code` / `Paradev` / `emdash` (`CLAUDE.md` = 1-line `@AGENTS.md` include, which also works cleanly on Windows where symlinks can break).
   - Add `paseo`'s `Doc voice` cliché ban and `openclaw`'s *"Choose good compromises"* (idempotency key + check + retry over speculative machinery).
2. **Progressive Rule & Skill Indexing + Living `REVIEW.md`:**
   - **Sources:** `paperclip` (`rules/*.mdc` headers scanned via `grep`), `cmux` (`REVIEW.md` seeded from real PR review catches), `orca` (`docs/agents-md-refs/`).
3. **Custom Lint Rules With Baselines & Shrink-Only Ratchets:**
   - **Sources:** `opencode` (`anti-slop` + `ast-grep`), `orca` (`quadratic-buffer-concat`, `ime-enter-guard`, `no-restricted-imports` guarding lazy SDK loads, `main-blocking-work.yml`), `Paradev` (domain `noRestrictedImports`), `emdash` (`respectEslintDisableDirectives: false`), `paseo` (per-file, per-API allowlists + unit-tested rules), `sandcastle` (5-category type-aware `oxlint` + `lint-shrink.yml` bot on lint/typecheck baselines).
4. **Multi-Agent Git & Local Isolation Safety:**
   - **Sources:** `pi` (ban `git add -A`, `git stash`, `git reset --hard`; review PRs without switching branches), `paseo` (checkout-local `.dev/<app>-home`), `t3code` / `cmux` (never kill processes by pattern or touch live user installs), `oh-my-openagent` (hermetic `$HOME` tests), `orca` (`ORCA_BACKGROUND_LAUNCH=1` hidden-window CDP).
5. **Anti-Test-Slop + Honest Disclosure + Cached Diff-Scoped Checks:**
   - **Sources:** `orca` (`"Tests are the exception"` for costly silent regressions + zero-checkout `pr-test-loc.yml` + mandatory `## Performance` PR section with `"None, because ..."` + cached `pnpm check:changed` with *"do not also run full suite"*), `cmux` (`### Observed / Not run`), `beads` (*"Check That the Test Actually Ran"* + `NOT_ENOUGH_INFO`), `oh-my-openagent` (gitignored `.omo/evidence/` + anti-commit audit).
6. **Single `if: always()` CI Required Aggregator:**
   - **Sources:** `codex`, `t3code`. Explicitly fail on `failure` or `cancelled`, treat `skipped` as success **only** when caused by path filtering, and make this aggregator the sole required branch-protection check.

---

## Tier 2 — Trigger-Gated Upgrades (Adopt Only When the Trigger Applies)

1. **Supply-Chain Cooldown + Sweeper (`codex`, `openclaw`, `orca`, `OpenHands`, `paseo`, `OpenSpec`):** Once you manage a shared lockfile with frequent dependency bumps, enable `minimumReleaseAge` (3 days `4320` on fast teams like `orca`; 7 days `10080` on `codex`/`openclaw`), explicit commented `allowBuilds`, dated expiry comments + a sweeper workflow (`dated-todo-sweep.yml`), and `lockfile-lint`. Put GHSA overrides in `pnpm-workspace.yaml` (not `package.json`).
2. **Verification Skill Independence & Diff Mutation Testing (`OpenHands`):** Once agents edit critical billing/auth/state-machine logic or maintain eval harnesses, add `verify-skill-isolation.yml` (blocking PRs that edit both app code and `.agents/skills/verify-*/`) and targeted `stryker-diff.mjs` on those critical paths only.
3. **Real DB Backup/Restore & Lock-Safe Migrations (`paperclip`, `Paradev`):** If you maintain self-hosted SQL migrations, prefix with `lock_timeout = '5s'` + `pipefail` and run a CI `pg_dump` → restore smoke check.
4. **Production Container / Installer / OS-Sandbox Smoke Tests (`bolt.diy`, `oh-my-openagent`, `sandcastle`):** If you ship Docker images, shell installers, or OS sandboxes, test the real artifact in CI (`curl` health check, double-run installer in isolated `$HOME`, real `bwrap`).
5. **Prompt-Prefix KV-Cache Stability & Behavioral Evals (`openclaw`, `gemini-cli`, `t3code`, `gstack`):** If you operate a cached LLM system prompt or agent tools, add `prefix-stability.test.ts` and gate live evals behind a GitHub **`eval-gate` environment** approval (`gemini-cli`) with a hard weekly spend cap (`gstack`: `$150/wk`).
6. **Skill-Repo Hygiene (`mattpocock/skills`, `gstack`, `pstack-claude`):** If your repo ships `SKILL.md` files, validate frontmatter with the installer's exact YAML parser, cap catalog tokens (`catalog-budget.test.ts`), set **both** `disable-model-invocation: true` (Claude) and `agents/openai.yaml` `allow_implicit_invocation: false` (Codex) on manual skills, and enforce fresh subagent context inside skills that dispatch subagents.
7. **Public OSS Contributor Gating (`pi`, `t3code`, `goose`, `OpenHands`, `cline`, `superpowers`):** Before opening a popular repo to external AI PRs, pick a clear gate (`VOUCHED.td` + PR limits, `Ready`-board gate, or upfront rejection expectations), require a `HUMAN:` summary section, and strip agent promo footers.

---

## Tier 3 — Anti-Patterns & Postmortems to Avoid

| Anti-Pattern | Real-World Evidence | Why It Hurts |
| --- | --- | --- |
| **Zero public CI + one-way mirror** | `21st-dev/1code` (archived; 7 weeks to last push) | Dual lockfiles, stale WIP docs, zero external trust, impossible to accept PRs safely. |
| **Scope & language sprawl ahead of team size** | `BloopAI/vibe-kanban` (30 Rust crates + ElectricSQL + WebRTC + Tauri → sunsetting); `cmux` (231 workflows; 17/20 Nov 25 commits by one dev on CI/release automation) | Maintenance and build friction dominate engineering bandwidth. |
| **Unchecked supply-chain / maintainer security** | `gsd-build/get-shit-done` (64.1k★, archived after *"appears compromised"* warning in `126b6b9e`) | Prompt and skill packages carry the same supply-chain blast radius as code packages. |
| **Duplicated `CLAUDE.md` / ALL-CAPS mega-docs** | `oh-my-openagent` (70.8 KB, 3-month-stale header); `vibe-kanban` / `paseo` / `cmux` (copy-pasted duplicates) | Burns tokens on every turn and drifts out of sync across harnesses. |
| **Warning-only lint / non-blocking PR gates** | `cline` (`apps/vscode` Biome rules `"info"`/`"off"`), `cmux` (`biome.json` formatter off), `bolt.diy` (`continue-on-error: true` on PR gate) | Silent quality decay — agents ignore non-blocking warnings. |
| **Committing generated bundles & scratch files** | `oh-my-openagent` (constant bundle-regen commits), `costrict` (`localhost`, `progress.txt`), `cmux` (`PR-10599-AUDIT.md`) | Merge conflicts across parallel worktrees and noisy diffs. |
| **Storing user API keys in JS-accessible cookies** | `bolt.diy` (`README.md` warning) | Any XSS turns into immediate credential exfiltration. |

---

## Practical Adoption Blueprint (Harmonized for a 1–5 Person TypeScript Monorepo)

Designed so Week 1, Week 2, and Week 3 gates reinforce rather than fight each other:

### Week 1 — Foundation (Zero Extra CI Maintenance)
1. **Lean `AGENTS.md` + 1-line `@AGENTS.md` in `CLAUDE.md`:** Open with your check command; include incident-cited traps, `paseo`'s `Doc voice`, `openclaw`'s *"Choose good compromises"*, `pi`'s multi-agent Git safety rules, and `orca`'s **`"Tests are the exception"`** policy (commit tests only for costly silent regressions; delete brittle mock/UI tests).
2. **One cached diff-scoped local command (`check:changed` / `verify`):** Instruct agents to run it once when done and **not** also re-run the full typecheck/lint/test suite (`orca`).
3. **PR template upgrades:** Add `### Observed / Not run` (`cmux`), `## Performance` with `"None, because ..."` allowed (`orca`), and fail CI if gitignored QA captures get committed.
4. **Seed `REVIEW.md` from real PR history** (only if you have actual PR review catches — never invent synthetic rules).

### Week 2 — Mechanical Ratchets (Baseline First, Never Red `main`)
5. **Commit baseline counts first, then turn on 3–5 lint rules taken directly from your repo's real review catches** (`oxlint` or Biome), using per-file/per-API allowlists (`paseo`) before disallowing new unapproved disables (`emdash`).
6. **Add a shrink-only ratchet bot for lint & typecheck counts only (`sandcastle` style)** — avoid a rising coverage floor that blocks deleting low-value tests from Week 1.
7. **Wire one `if: always()` `CI required` aggregator** (explicitly failing on `failure`/`cancelled` and allowing path-filtered `skipped` only) + a zero-checkout `pr-test-loc.yml` summary (`orca`).

### Week 3 — Trigger-Gated Only (Add Only If Your Repo Actually Needs It)
- **Weekly dependency bumps:** Add `minimumReleaseAge` (`4320` or `10080`), commented `allowBuilds`, and a dated-exemption sweeper.
- **Self-hosted SQL migrations:** Add `lock_timeout = '5s'` + CI `pg_dump`/restore smoke check.
- **Cached LLM prompts / evals:** Add `prefix-stability.test.ts` and `eval-gate` environment-approved behavioral evals with a spend cap.
- **Existing `SKILL.md` catalog:** Add installer-parser frontmatter CI, token-budget caps, and dual Claude+Codex manual-invocation flags.
- **Public fork PRs:** Add contributor gating (`VOUCHED.td` / `Ready` board / `HUMAN:` PR check) and `verify-skill-isolation.yml` on `.agents/skills/verify-*/`.
