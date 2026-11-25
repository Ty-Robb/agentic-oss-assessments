# Agentic OSS Engineering Playbook

*Synthesized from primary-source GitHub API audits of **35 open-source agentic coding, orchestration, and skill-stack repositories** (**3,040,947 / ~3.04M combined GitHub stars**, snapshot date: **2026-11-25**).*

Every recommendation below is backed by real configuration files, CI workflows, lint plugins, and commit histories captured under [`data/`](../data/). Nothing here is taken from marketing pages or blog posts.

---

## Executive Summary: 6 Empirical Laws of High-Velocity Agentic Repos

1. **Mechanical invariants beat prose instructions 10-to-1.**
   - Every surviving high-velocity TypeScript codebase (`t3code`, `Paradev`, `emdash`, `opencode`, `openclaw`, `paseo`, `oh-my-openagent`) stopped lecturing agents in `AGENTS.md` and encoded recurring failure modes directly into **`oxlint` / Biome custom plugins, `ast-grep` rules, or meta-tests**.
   - Conversely, shouting in a 70.8 KB ALL-CAPS `AGENTS.md` (`oh-my-openagent`) drifts within months, while `21st-dev/1code` (zero CI, zero lint, zero tests) archived in 7 weeks.

2. **The Open-Issue Stress Test proves contributor gating is mandatory at scale.**
   - In an era where anyone can prompt an agent to open a PR in 90 seconds, open-by-default trackers collapse under review debt:
     - `openai/codex` (136.4k★, open tracker + triage bots): **28,619 open issues**
     - `manaflow-ai/cmux` (28.9k★, autonomous agent factory): **11,218 open issues**
     - `openclaw/openclaw` (395.2k★, 20-PR cap + bot sweepers): **9,182 open issues**
     - `pingdotgg/t3code` (78.8k★, `VOUCHED.td` + PR limits): **3,681 open issues**
     - `aaif-goose/goose` (57.0k★, `Ready`-board gate): **512 open issues**
     - `earendil-works/pi` (123.8k★, **default-closed `lgtmi`/`lgtm` gate**): **307 open issues** (a **93× reduction** vs. Codex)
   - `getpaseo/paseo` puts it most plainly in `CONTRIBUTING.md`: *"I can prompt an agent to write code just as you can. The bottlenecks are choosing what to build, shaping it, verifying its behavior, and taking responsibility for its maintenance."*

3. **CI has a Goldilocks zone — beware both 0 workflows and 200+ workflows.**
   - **Too little (`1code`: 0 workflows; `happy`: 1 workflow):** Only survives if you are a 2-person high-trust core pushing straight to `main` (`happy`); fails fast with broader contributors (`1code`).
   - **Too much (`cmux`: 231 workflows; `openclaw`: 133 workflows):** In `cmux`, roughly **80% of recent commits on `main`** are spent repairing the CI runner pools, nightly pickers, and autofix loops themselves.
   - **The sweet spot (`emdash`: 6, `paseo`: 12, `pi`: 16, `opencode`: 21, `Paradev`: 22, `OpenHands`: 25, `t3code`: 29):** Fast path-filtered CI, strict custom lint, dead-code checks, supply-chain cooldowns, and targeted behavioral/E2E gates.

4. **Verification must be independent of the implementor — and cannot silently pass by skipping.**
   - Agents naturally game soft checks: weakening tests to make CI green, claiming a filtered test run passed when 0 subtests matched, or reading a skipped CI job as green coverage.
   - The best defenses in the cohort are **Verification Skill Independence** (`OpenHands`: `verify-skill-isolation.yml`), **diff-scoped mutation testing** (`OpenHands`: `stryker-diff.mjs`), **uncommitted local QA evidence + `sha256sum` PR proofs** (`oh-my-openagent`), **explicit `### Observed / Not run` PR sections** (`cmux`), and **"verify the test actually ran"** (`beads`).

5. **Scope sprawl and weak governance kill projects faster than missing features.**
   - All four archived or sunsetting repos in this 34-repo study share clear structural failure modes:
     - `21st-dev/1code` (Archived < 2 mos): Zero CI/tests + one-way sync mirror + stale WIP docs.
     - `BloopAI/vibe-kanban` (Sunsetting): Strong Rust craft (`ts-rs`, `sqlx`), crushed by 30 Rust crates + ElectricSQL + WebRTC relay + Tauri + Rust nightly on a 4-person team.
     - `RooCodeInc/Roo-Code` (Archived May 2026): Trapped inside a VS Code extension architecture while every surviving rival (`Cline`, `OpenHands`, `Goose`) decoupled into multi-surface SDKs + ACP control planes.
     - `gsd-build/get-shit-done` (64.1k★, Archived May 2026): Heavy CommonJS + TS SDK process sprawl, ultimately abandoned and migrated to `open-gsd/gsd-core` after a repo-compromise warning in git history.

6. **Skill stacks do not boost raw bug-fix rates — they enforce alignment, review, QA, and safety.**
   - `garrytan/gstack` published the most honest empirical receipt in the study right inside its `README.md`: on 100 real GitHub bugs/features, Opus 5.5 solved **58 with `gstack`** vs. **61 of 99 without it** (and 29 vs. 29 on 60 security fixes).
   - Skills are for **workflow discipline** (`/grill-me`, `brainstorming`, `GLOSSARY.md`, formal verification via `pstack`'s TLA+/Lean, and shipping evidence). Raw code quality still comes from **mechanical repo gates** — exemplified by Matt Pocock's `sandcastle` (all-5-category `oxlint` straitjacket + automated `lint-shrink.yml` ratchet bot).
   - Skill repos also face extreme AI-PR slop (`obra/superpowers` reports a **94% PR rejection rate**; `mattpocock/skills` and `OpenSpec` restrict PRs to collaborators/invited authors only).

---

## Master 35-Repository Matrix

| Chunk | Repository | Stars | Open Issues | Status | Primary Stack | Workflows | Last-50 Velocity | Signature Practice to Know |
| --- | --- | ---: | ---: | --- | --- | ---: | --- | --- |
| Base | [`pingdotgg/t3code`](../RUBRIC.md) | 78.8k | 3,681 | Active | TS (226.7 MB, Effect, Vite+, Electron, RN) | 29 | 50 / **7.0 hrs** | `oxlint-plugin-t3code`, `VOUCHED.td`, `evals/`, `agent-context-budget` |
| C1 | [`stablyai/orca`](../chunks/chunk-01-direct-rivals/orca.md) | **137.8k** | 9,918 | Active | TS (143.7 MB, Electron, Web, Mobile, `orcad`, Ghostty) | 67 | 50 / **3.2 hrs** | `"Tests are the exception"`, `pr-test-loc`, `## Performance` CI gate, `quadratic-buffer-concat` oxlint |
| C1 | [`ParadevAI/Paradev`](../chunks/chunk-01-direct-rivals/paradev.md) | 16.6k | 1,263 | Active | TS (35.2 MB, Bun, Turbo, Electron/Next/Expo, Drizzle) + TLA+ | 22 | 50 / **3.2 days** | Domain `noRestrictedImports` in Biome, `paradev schema`, 2-min test budget |
| C1 | [`BloopAI/vibe-kanban`](../chunks/chunk-01-direct-rivals/vibe-kanban.md) | 28.8k | 537 | **Sunsetting** | 30-crate Rust (`axum`/`sqlx`/`ts-rs`/`tauri`) + React | 9 | 50 / **7.5 mos** | `ts-rs` codegen check, `sqlx` offline check (warning: scope sprawl) |
| C1 | [`generalaction/emdash`](../chunks/chunk-01-direct-rivals/emdash.md) | 6.3k | 92 | Active | TS (21.2 MB, pnpm, Nx, Electron, Drizzle, MobX) | 6 | 50 / **22 days** | `respectEslintDisableDirectives: false`, self-pruning allowlists, sole-writer DB lint |
| C1 | [`21st-dev/1code`](../chunks/chunk-01-direct-rivals/1code.md) | 5.6k | 45 | **Archived** | TS (5.1 MB, Electron, Bun, tRPC, Drizzle) | **0** | Archived Mar '26 | Ephemeral NDJSON log server (`localhost:7799/log`); anti-pattern on CI/mirror |
| C2 | [`anomalyco/opencode`](../chunks/chunk-02-agent-harnesses/opencode.md) | 229.1k | 4,172 | Active | TS (Effect v4, Bun, Solid/OpenTUI) + Rust daemon | 21 | 50 / **12.3 hrs** | `anti-slop` oxlint plugins, unit-tested `ast-grep`, Miri, 7 triage workflows |
| C2 | [`earendil-works/pi`](../chunks/chunk-02-agent-harnesses/pi.md) | 123.8k | **307** | Active | TS (npm workspaces, erasable TS, Biome) | 16 | 50 / **1.7 days** | Default-closed `lgtmi`/`lgtm` gate, multi-agent Git safety rules, GritQL Biome |
| C2 | [`openai/codex`](../chunks/chunk-02-agent-harnesses/codex.md) | 136.4k | 28,619 | Active | Rust (90.7 MB, Bazel/Cargo) + pnpm SDKs | 31 | 50 / **14.7 hrs** | 7-day npm cooldown (`minimumReleaseAge: 10080`), `CI required` aggregator |
| C2 | [`google-gemini/gemini-cli`](../chunks/chunk-02-agent-harnesses/gemini-cli.md) | 109.1k | 751 | Active | TS (npm workspaces, Ink, esbuild/SEA) | 47 | 50 / **18.1 days** | 47 behavioral `evals/` + 2-stage `eval-pr.yml`, zero-checkout drift check |
| C3 | [`cline/cline`](../chunks/chunk-03-autonomous-and-ide/cline.md) | 71.9k | 1,833 | Active | TS (Bun, SDK + CLI + VS Code gRPC + Tauri) | 17 | 50 / **19.5 days** | 34-line trap-only `AGENTS.md`, strip agent promo footers, fixture installer tests |
| C3 | [`RooCodeInc/Roo-Code`](../chunks/chunk-03-autonomous-and-ide/roo-code.md) | 24.2k | 1,025 | **Archived** | TS (pnpm, Turbo, VS Code ext + webview) | 7 | Archived May '26 | 5-line single-invariant `AGENTS.md`, `.roomodes`, clean pre-archive strip |
| C3 | [`OpenHands/OpenHands`](../chunks/chunk-03-autonomous-and-ide/openhands.md) | 94.3k | 1,252 | Active | TS (React 19, Vite 8, Electron Agent Canvas) | 25 | 50 / **2.0 days** | **`verify-skill-isolation.yml`**, **Stryker diff mutation**, `HUMAN:` PR check |
| C3 | [`aaif-goose/goose`](../chunks/chunk-03-autonomous-and-ide/goose.md) | 57.0k | 512 | Active | Rust (`oi-kit` + ACP + `rmcp`) + Electron | 39 | 50 / **5.0 days** | `Ready`-board gate, `check-lean-size`, `wasm32`, `git cherry` release check |
| C4 | [`openclaw/openclaw`](../chunks/chunk-04-agent-native-orchestration/openclaw.md) | 395.2k | 9,182 | Active | TS (**474.7 MB**) + Swift/Kotlin/Rust, Kysely | 133 | 50 / **2.3 hrs** | <20 KB `AGENTS.md` ("cite an incident"), all-error `oxlint`, `prefix-stability` test |
| C4 | [`paperclipai/paperclip`](../chunks/chunk-04-agent-native-orchestration/paperclip.md) | 116.9k | 6,812 | Active | TS (157.8 MB, Express/React/Drizzle/PG) + Rust | 41 | 50 / **14.5 hrs** | `grep`-indexed `rules/*.mdc`, `pnpm verify` (exit 2), real PG `pg_dump`/restore CI |
| C4 | [`openai/symphony`](../chunks/chunk-04-agent-native-orchestration/symphony.md) | 28.2k | **0** | Active | `SPEC.md` + 914 KB Elixir/OTP + Burrito | 4 | 47 / **6.0 mos** | Spec-as-product ("implement `SPEC.md` in your language"), `mix pr_body.check` |
| C4 | [`gastownhall/beads`](../chunks/chunk-04-agent-native-orchestration/beads.md) | 29.0k | 1,828 | Active | Go (51.4 MB) + Bazel + Dolt | 23 | 50 / **8.0 days** | `gascity-eddie[bot]` (41/50 commits), `NOT_ENOUGH_INFO`, "verify test ran" |
| C5 | [`getpaseo/paseo`](../chunks/chunk-05-specialists/paseo.md) | 25.3k | 2,203 | Active | TS (51.2 MB, Expo/Electron, Noise NK relay) | 12 | 50 / **2.4 days** | Anti-slop `Doc voice`, per-file/API `no-sync-io` allowlist, "PRs closed by default" |
| C5 | [`slopus/happy`](../chunks/chunk-05-specialists/happy.md) | 24.8k | 1,154 | Active | **Native Swift (22.3 MB) + Kotlin (14.6 MB)** + TS | **1** | 50 / **8.4 days** | Incident-cited `main == origin/main` release rule, CI-cost ban, `env:up/seed` CLI |
| C5 | [`manaflow-ai/cmux`](../chunks/chunk-05-specialists/cmux.md) | 29.0k | 11,218 | Active | **Swift (115.2 MB)** + Py/Rust/TS + Ghostty | **231** | 50 / **9.7 hrs** | `REVIEW.md`, `verify-local.py --receipt -`, compiled-app reuse (warning: CI bloat) |
| C5 | [`smtg-ai/claude-squad`](../chunks/chunk-05-specialists/claude-squad.md) | 8.9k | 54 | Active | **263 KB Go** (Bubble Tea) + `tmux` + worktrees | 5 | 50 / **17 mos** | Unix composition over reinvention, `golangci-lint --only-new-issues` |
| C5 | [`stackblitz-labs/bolt.diy`](../chunks/chunk-05-specialists/bolt-diy.md) | 20.1k | 2 | Active | TS (3.4 MB, React Router, WebContainers, AI SDK) | 13 | 50 / **5.3 days** | Prod Docker `curl` smoke test in CI, `.performance-budgets.json`, Lighthouse CI |
| C5 | [`code-yeongyu/oh-my-openagent`](../chunks/chunk-05-specialists/oh-my-openagent.md) | 71.1k | 2,823 | Active | TS (58.0 MB) + Rust (5.3 MB), 45 pkgs, Bun | 48 | 50 / **19.2 hrs** | Local `.omo/evidence/` + `sha256sum` proof + anti-commit test, hermetic `$HOME` tests |
| C5 | [`zgsm-ai/costrict`](../chunks/chunk-05-specialists/costrict.md) | 4.5k | 14 | Slowing | TS (15.1 MB, Roo Code enterprise fork, pnpm) | 11 | 50 / **3.6 mos** | 1-line English commit rule (92% conv), 40+ CVE overrides, workspace-trust MCP gate |
| C6 | [`mattpocock/skills`](../chunks/chunk-06-skill-stacks/mattpocock-skills.md) | 332.8k | 251 | Active | Markdown skills + 20 KB Shell/JS, Changesets | 4 | 50 / **7.1 wks** | Bucket lifecycle, fresh-context subagents, Codex `openai.yaml` parity, collab-only PRs |
| C6 | [`mattpocock/sandcastle`](../chunks/chunk-06-skill-stacks/mattpocock-sandcastle.md) | 9.3k | 137 | Active | TS (2.6 MB, TS 7, Effect, `oxlint-tsgolint`) | 8 | 50 / **6.0 days** | **All-5-cat `oxlint` straitjacket + `lint-shrink.yml` bot**, real `bwrap` CI, `docs-guide.test.ts` |
| C6 | [`obra/superpowers`](../chunks/chunk-06-skill-stacks/superpowers.md) | 326.5k | 372 | Active | Markdown skills + 520 KB Shell/JS, 15+ harnesses | **0** | 50 / **4.0 mos** | **94% PR rejection rate**, external Quorum eval lab, `"react todo list"` bootstrap test |
| C6 | [`github/spec-kit`](../chunks/chunk-06-skill-stacks/spec-kit.md) | 151.4k | 230 | Active | Python (11.9 MB, `uv`, Typer, MCP SDK) | 29 | 50 / **7.0 days** | **Firewall-sandboxed `gh-aw` agentic workflows**, Evidence Gate, Ruff `S602`–`S605` |
| C6 | [`garrytan/gstack`](../chunks/chunk-06-skill-stacks/gstack.md) | 142.6k | **45** | Active | TS (**45.1 MB**), Bun, Playwright/Aside CLIs | 38 | 50 / **1.8 days** | Honest **58 vs 61/99** eval, `egress-receipt-wiring`, token-budget ratchets, `$150/wk` cap |
| C6 | [`Fission-AI/OpenSpec`](../chunks/chunk-06-skill-stacks/openspec.md) | 75.7k | 214 | Active | TS (5.8 MB, Node 22+, pnpm 10, Vitest 5) | 5 | 50 / **25 days** | **`startup-modules.test.ts`** CLI cold-start guard, GHSA-annotated overrides, 2-PR features |
| C6 | [`gsd-build/get-shit-done`](../chunks/chunk-06-skill-stacks/get-shit-done.md) | 64.1k | 0 | **Archived** | 7.3 MB CJS + 2.6 MB TS SDK, `node:test` | 20 | Archived May '26 | `prompt-injection-scan.sh`, `<issue#>-<slug>` ADRs (postmortem: compromise redirect) |
| C6 | [`bmad-code-org/BMAD-METHOD`](../chunks/chunk-06-skill-stacks/bmad-method.md) | 55.7k | 116 | Active | Python (1.8 MB, `uv`, Jinja2, Ruff) + Astro | 5 | 50 / **27 days** | *"Length paid on every run; prefer deleting to hedging"*, PEP 723 skill scripts, `ready_for_review` AI |
| C6 | [`pstack`](../chunks/chunk-06-skill-stacks/pstack.md) (`backnotprop` / `pstack-claude`) | 5.2k / 4.9k | 2 / 16 | Active | Agent Skills + 1.8 MB TS/JS + **Lean/TLA+** | 0 / 6 | 50 / **6.5 days** | Formal verification skills (TLA+/Lean), `tools/forks.json` CI check, `--check-rules` |

---

## Tier 1 — Steal Immediately (High ROI, < 1 Day Each)

These practices require minimal infrastructure and pay off on day one for any team using coding agents.

### 1. Trap-Only, Incident-Cited `AGENTS.md` + Single Source of Truth
- **Sources:** `openclaw` (*"A new rule cites an incident"*, <20 KB hard cap), `cline` (34 lines), `happy` (40 lines citing exact `2026-09-20` rollback), `t3code` / `Paradev` / `emdash` (`CLAUDE.md` = `@AGENTS.md` or symlink).
- **Rule:** Never put prose architecture tutorials or WIP status in `AGENTS.md`. Keep it under ~150–200 lines. Every rule must cite a real bug/incident or point to a subject doc/skill. Symlink or `@AGENTS.md`-include `CLAUDE.md` so the two can never drift.
- **Add `paseo`'s `Doc voice` + `openclaw`'s `Choose good compromises`:** Ban LLM puffery (`"It's not X, it's Y"`, `"robust"`, `"seamless"`, `"and that matters"`) and explicitly instruct agents to prefer simple, recoverable mechanisms (idempotency key + check + retry) over speculative machinery.

### 2. Progressive Rule & Skill Indexing
- **Sources:** `paperclip` (`rules/*.mdc` with frontmatter headers scanned via `grep`), `cmux` (`REVIEW.md` of recurring review catches), `Paradev` / `t3code` / `OpenHands` (`.agents/skills/`).
- **Rule:** Put task-specific checklists in `.agents/skills/` or `rules/*.mdc` with 1-line frontmatter descriptions rather than stuffing everything into root `AGENTS.md`. Maintain a compact **`REVIEW.md`** containing the top 10–20 real bugs code review keeps catching, and require agents to check their diff against it before opening a PR.

### 3. Anti-Slop & Domain-Invariant Custom Lint Rules (with Debt Ratchets)
- **Sources:** `opencode` (`anti-slop` oxlint plugin + `ast-grep`), `openclaw` (`correctness`/`perf`/`suspicious` = `"error"`), `orca` (`quadratic-buffer-concat`, `ime-enter-guard`, `app-store-performance`, `no-restricted-imports` guarding lazy SDK loads, `main-blocking-work.yml` sync-spawn ratchets), `Paradev` (`noRestrictedImports` banning sync subprocesses, raw sandbox handles, cross-tenant queries), `emdash` (`respectEslintDisableDirectives: false` + sole-writer DB table bans + `prune:boundary-allowlists`), `paseo` (per-file, per-API allowlists + unit-tested lint plugin), `sandcastle` (all-5-category type-aware `oxlint` + automated `lint-shrink.yml` PR bot).
- **Rule:** Turn every repeated PR review comment into a lint error within the same week. If legacy violations exist, use **per-file, per-API allowlists** (never directory-wide disables) and **ban unapproved `eslint-disable` comments**. Unit-test your custom lint rules in CI.

### 4. Multi-Agent Git & Isolation Safety Rules
- **Sources:** `pi` (ban `git add -A`, `git stash`, `git reset --hard`; review PRs without switching branches), `paseo` (checkout-local `.dev/<app>-home`), `t3code` / `cmux` (never kill processes by pattern or touch the user's live running app/DB), `oh-my-openagent` (`test-hermetic-home.test.ts` + `test-temp-leak-match.test.ts`).
- **Rule:** Assume 3–5 agents share the developer's machine simultaneously. Isolate dev data per worktree (`.dev/`), never let tests touch real `$HOME`, and forbid destructive broad git commands.

### 5. Supply-Chain Cooldown & Lockfile Integrity
- **Sources:** `codex` & `openclaw` (`pnpm-workspace.yaml`: `minimumReleaseAge: 10080` [7 days], `blockExoticSubdeps: true`, `strictDepBuilds: true`, dated expiry comments on exemptions), `OpenHands` (`--min-release-age=7`), `paseo` (`lockfile-lint`), `pi` (`npm ci --ignore-scripts`).
- **Rule:** Adding a 7-day npm release cooldown + explicit `allowBuilds` / `onlyBuiltDependencies` takes 10 lines of YAML and neutralizes almost every zero-day npm supply-chain compromise.

### 6. Honest Verification Disclosures, Anti-Vacuous Checks & Anti-Test-Slop
- **Sources:** `orca` (`"Tests are the exception"` policy + zero-checkout `pr-test-loc.yml` on `ubuntu-slim` + mandatory `## Performance` PR check + `ORCA_BACKGROUND_LAUNCH=1` hidden-window CDP + `unit-selection-evidence.yml` shadow-mode diff test selection), `cmux` (`### Observed / Not run` PR section + *"a skipped job is green and is not coverage"*), `beads` (*"Check That the Test Actually Ran"* + `NOT_ENOUGH_INFO` rule), `oh-my-openagent` (local gitignored `.omo/evidence/` + `sha256sum` in PR body + CI test failing if evidence is committed), `t3code` (`git ls-files .github/pr-assets` check).
- **Rule:** Require every PR body to list the exact commands run, observed output, and explicitly what was **not** run — and ban low-value UI/mock unit tests that pad PR diffs without protecting costly invariants. Never commit temporary QA screenshots/logs into git — upload them to the PR or keep them gitignored with a CI guard.

### 7. Fast Local Diff-Scoped Checker + Single Required CI Aggregator
- **Sources:** `paperclip` (`pnpm verify` with exit code 2 when diff is too broad), `cmux` (`scripts/verify-local.py --receipt -`), `t3code` (`vp run check:changed`), `codex` (`CI required` aggregator with `if: always()`).
- **Rule:** Give agents one fast, diff-scoped local command (`check:changed` / `verify`) so they don't burn 15 minutes running the whole repo locally, and pair path-filtered CI jobs with a single `if: always()` aggregator job for branch protection so skipped jobs never hang PRs.

---

## Tier 2 — Steal as You Scale (Multi-Agent, Production DB, or Public OSS)

Adopt these once your repo has multiple concurrent agents, stateful databases, LLM prompt pipelines, or external contributors.

1. **Verification Skill Independence (`OpenHands`):** Add a CI check (`verify-skill-isolation.yml`) blocking PRs that touch both production code and verification skills/eval harnesses in the same commit, stopping agents from weakening acceptance criteria to pass.
2. **Diff-Scoped Mutation Testing (`OpenHands`):** Run Stryker (`stryker-diff.mjs`) strictly on changed lines of critical domain logic so AI-written tests are proven to kill mutants instead of padding line coverage.
3. **Real Database Backup/Restore & Lock-Safe Migration Gates (`paperclip` & `Paradev`):**
   - `paperclip`: Spin up real Postgres in CI, seed data, run `pg_dump` → restore → verify schema/rows (`backup-checkpoint-qualification.yml`).
   - `Paradev`: Prefix Drizzle/SQL migrations with `lock_timeout = '5s'` and `set -euo pipefail` so a blocked migration never takes down production tables.
4. **Prompt-Prefix KV-Cache Stability Tests & Behavioral Evals (`openclaw`, `gemini-cli`, `t3code`):**
   - Test that system prompt + tool schema serialization stays byte-stable across turns (`prefix-stability.test.ts`).
   - Build a small suite of behavioral evals (`frugalReads`, `answer-vs-act`, `prompt_injection_mcp`) gated behind a secure two-stage `pull_request_target` maintainer label (`eval-pr.yml`).
5. **Production Container / Installer Smoke Tests (`bolt.diy`, `oh-my-openagent`, `cline`):**
   - Build the production Docker image in CI, boot it, `curl` its health endpoint, and assert `State.Running == true` (`bolt.diy`).
   - Test shell installers twice in an isolated `$HOME` (proving idempotency + fallback on unreachable mirrors) with `shellcheck` (`oh-my-openagent`).
6. **Review-Capacity Defenses for Public OSS (`pi`, `t3code`, `paseo`, `OpenHands`, `goose`, `cline`):**
   - Pick an explicit gate: `lgtmi`/`lgtm` default-closed (`pi`), `VOUCHED.td` + PR limits (`t3code`), `Ready`-board gate (`goose`), or "PRs closed by default" + 3,000-line cap (`paseo`).
   - Require a short `HUMAN:` section in PR bodies (`OpenHands`) and strip automated agent promotional badges/footers (`cline`).
7. **Autonomous Bug-Burn Bot Pipeline (`beads`, `opencode`, `paseo`):**
   - Once your mechanical gates and test suite are rock-solid, a dedicated bot (`gascity-eddie[bot]`, `opencode-agent[bot]`, `paseo-bot[bot]`) operating on explicitly labeled, scoped issues with strict `check-bot-scope.yml` permissions can sustainably clear routine bug backlogs.
8. **Zero-Checkout Migration Drift Bot (`gemini-cli`):**
   - During large refactors, run a lightweight GitHub API workflow checking if a PR edited legacy file `A` without updating migrated counterpart `B`, posting a reminder comment in seconds with zero runner checkout cost.

---

## Tier 3 — Anti-Patterns & Postmortems to Avoid

| Anti-Pattern | Real-World Evidence | Why It Hurts |
| --- | --- | --- |
| **Zero CI + one-way public mirror** | `21st-dev/1code` (archived in 7 weeks) | Dual lockfiles, stale WIP docs, zero external trust, impossible to accept PRs safely. |
| **Scope & language sprawl ahead of team size** | `BloopAI/vibe-kanban` (30 Rust crates + ElectricSQL + WebRTC + Tauri on 4 people → sunsetting); `cmux` (7 languages, 5 SDKs, 231 workflows → 11,218 open issues) | Maintenance and build friction consume the team; users leave over core instability. |
| **Self-consuming CI factory + human-less `--override` merges** | `manaflow-ai/cmux` (231 workflows; ~80% of sampled `main` commits are fixing CI/runner pools/autofixers) | Automation stops serving product velocity and becomes the primary workload; red `main` normalizes regressions. |
| **ALL-CAPS mega-`AGENTS.md` + duplicated `CLAUDE.md`** | `oh-my-openagent` (70.8 KB, 3 mos stale); `vibe-kanban` / `paseo` / `cmux` (copy-pasted duplicates) | Burns thousands of tokens every turn, drifts from reality, and encourages agents to ignore buried rules. |
| **Downgrading lint rules to `"info"` / disabling formatter** | `cline` (`apps/vscode` Biome rules `"info"`/`"off"`), `cmux` (`biome.json` formatter off), `bolt.diy` (`continue-on-error: true` on PR gate) | Silent quality decay — agents never fix warnings or non-blocking checks. |
| **Committing generated bundles & scratch files to git** | `oh-my-openagent` (constant bundle-regen commits), `costrict` (`localhost`, `progress.txt`), `cmux` (`PR-10599-AUDIT.md`) | Merge conflicts across parallel worktrees and noisy diffs that hide real bugs. |
| **Storing user API keys in JS-accessible cookies** | `bolt.diy` (`README.md` warning) | Any XSS turns into immediate credential exfiltration. |
| **Staying trapped in a single-editor fork after upstream pivots** | `RooCodeInc/Roo-Code` (archived May 2026) → `zgsm-ai/costrict` (1 maintainer carrying 15 MB `@roo-code/*` scaffolding, quiet since Sep '26) | Inherited complexity without upstream momentum. |

---

## Practical Adoption Blueprint (Small/Mid-Size TypeScript Monorepo)

For a real-world TypeScript product monorepo (e.g., Next.js / React + API/ORM + Drizzle/Postgres + Vitest/Playwright + GitHub Actions), here is the highest-leverage ordered rollout drawn from all 34 repos:

### Week 1 — Foundation (High Signal, Near-Zero Maintenance)
1. **Tighten `AGENTS.md` (<180 lines) + symlink `CLAUDE.md` → `AGENTS.md`:** Add incident-cited traps, `paseo`'s `Doc voice` anti-slop list, `openclaw`'s *"Choose good compromises"*, and `pi`'s multi-agent Git safety rules.
2. **Add `REVIEW.md`:** Seed it with the last 10–15 real bugs caught in your PR reviews; reference it from `AGENTS.md`.
3. **Lock down supply chain (`pnpm-workspace.yaml`):** Enable `minimumReleaseAge: 10080` (7 days), `blockExoticSubdeps: true`, and explicit `allowBuilds` / `onlyBuiltDependencies`.
4. **Add one diff-scoped local verification command (`verify` / `check:changed`):** Typecheck + lint + affected unit tests, plus `knip` for dead files/exports.

### Week 2 — Mechanical Guardrails
5. **Encode 3–5 repo-specific invariants as lint errors (`oxlint` or Biome):** Ban cross-tenant/unscoped DB queries (`Paradev`), ban `eslint-disable` without justification (`emdash`), enforce `no-floating-promises` + `no-explicit-any` (`openclaw`), and add unit tests for custom lint rules (`paseo`).
6. **Harden CI with a single `CI required` aggregator (`codex`) + `### Observed / Not run` PR template (`cmux`):** Add a CI step rejecting committed scratch/evidence files (`t3code` / `oh-my-openagent`).
7. **Add hermetic test & DB guards:** Enforce `lock_timeout = '5s'` on migrations (`Paradev`), add a real Postgres migration + `pg_dump`/restore smoke job if stateful (`paperclip`), and a production container `curl` health check if Dockerized (`bolt.diy`).

### Week 3+ — As Agent Autonomy Scales
8. **Separate verification from implementation (`OpenHands`):** Protect `.agents/skills/*-qa/` or `evals/` via `CODEOWNERS` / `verify-skill-isolation.yml`.
9. **Add diff-scoped mutation testing (`stryker-diff.mjs`)** on billing, auth, and core state machines.
10. **If shipping LLM features:** Add a deterministic `prefix-stability.test.ts` (`openclaw`) and 5–10 core behavioral evals (`gemini-cli` / `t3code`) gated behind a manual PR label.
