# Everything You Need to Know: Lessons from 35 Agentic OSS Repositories

*Executive brief distilled from primary-source GitHub API audits of **35 open-source coding agent, harness, orchestration, and skill-stack repositories** (**3.04M combined stars**, snapshot date: **2026-11-25**). For the full 35-repo matrix, raw metrics, and Week 1–3 implementation plan, see [`PLAYBOOK.md`](PLAYBOOK.md).*

---

## 1. The Macro Picture: Who Survives and Who Dies

Across all 24 repositories, **survival and shipping velocity correlate with mechanical discipline and scope restraint — not launch hype.**

- **What died or stalled:**
  - **`21st-dev/1code`** (5.6k★, **archived in 7 weeks**): Zero CI, zero linter, zero tests, dual lockfiles, stale WIP docs, and a one-way public mirror.
  - **`BloopAI/vibe-kanban`** (28.8k★, **sunsetting**): Strong Rust craft (`ts-rs`, `sqlx`, `clippy -D warnings`), crushed by 30 Rust crates + ElectricSQL + WebRTC relay + Tauri + Rust nightly on a 4-person team.
  - **`RooCodeInc/Roo-Code`** (24.2k★, **archived May 2026**) & its fork **`zgsm-ai/costrict`** (quiet since Sep 2026): Trapped inside a VS Code extension while every surviving peer (`Cline`, `OpenHands`, `Goose`) decoupled into an SDK + multi-surface ACP control plane.
- **Where the winners converged:**
  - **Architecture:** TypeScript monorepo + local daemon/server + multi-surface clients + **ACP** for structured agent providers (`t3code`, `Paradev`, `emdash`, `paseo`, `OpenHands`, `Goose`).
  - **Mobile split:** Either cross-platform Expo backed by deep subject docs (`t3code`, `paseo`) or pure native Swift + Kotlin (`slopus/happy`, which ripped out Expo/EAS after a stale-worktree OTA rollback incident).
  - **Autonomous maintenance bots are already live in production OSS:** `gascity-eddie[bot]` authored **41/50** recent commits in `beads`, `paseo-bot[bot]` **15/50** in `paseo`, and `opencode-agent[bot]` is #3 all-time in `opencode` (2,766 commits) — *only* sustainable because those repos enforce strict mechanical gates.

---

## 2. How to Run `AGENTS.md` & Docs

Prompts work as a **router and trap list**, never an encyclopedia.

- **Keep root `AGENTS.md` under ~150–200 lines (<20 KB) and single-sourced.** Symlink or `@AGENTS.md`-include `CLAUDE.md` (`t3code`, `Paradev`, `emdash`, `beads`). Copy-pasted duplicates drift; 70.8 KB ALL-CAPS shouting (`oh-my-openagent`) burns tokens on every turn and still gets ignored.
- **Every new rule must cite a real incident (`openclaw`, `happy`).** If you cannot name the bug or outage it prevents, cut the rule.
- **Explicitly ban LLM over-engineering (`openclaw` — *"Choose good compromises"*):** Instruct agents to prefer cheap, recoverable mechanisms (*idempotency key, one check, retry*) over speculative machinery (*fencing tokens, multi-phase admission*), and to note accepted edge cases rather than coding around them.
- **Explicitly ban LLM prose slop (`paseo` — `Doc voice`):** Forbid `"It's not X, it's Y"`, `"robust"`, `"seamless"`, `"and that matters"`, `"It's worth noting that"`, and append-only doc edits (*integrate, don't append; delete obsolete prose*).
- **Split operational knowledge into 3 layers:**
  1. **Root `AGENTS.md`:** Hard invariants + routing table.
  2. **`REVIEW.md` (`cmux`):** Compact living checklist of the recurring mistakes your PR reviews keep catching — agents self-audit against it before opening a PR.
  3. **Progressive `.agents/skills/` or `grep`-indexed `rules/*.mdc` (`paperclip`, `t3code`, `Paradev`):** Loaded only when working in that area.

---

## 3. Mechanical Quality Gates (The Real Competitive Edge)

If an agent makes a mistake twice, **stop putting it in `AGENTS.md` and make the linter or CI reject it.**

- **Custom `oxlint` / Biome plugins + `ast-grep` targeting LLM tics:**
  - **`openclaw`:** Sets `correctness`, `perf`, and `suspicious` to `"error"` + `no-floating-promises` + `switch-exhaustiveness-check`.
  - **`opencode`:** Custom `anti-slop` plugin + unit-tested `ast-grep` rules (`no-widen-then-assert`, `no-module-mocking`, `require-safety-comment-for-type-assertion`).
  - **`Paradev`:** Domain `noRestrictedImports` banning sync subprocesses on serving loops, raw sandbox handles, and cross-tenant admin queries.
  - **`emdash`:** Sets **`respectEslintDisableDirectives: false`** (stops agents from silencing errors with `eslint-disable`), enforces sole-writer DB table bans, and runs self-pruning allowlists (`prune:boundary-allowlists`).
  - **`paseo`:** Uses per-file, **per-API** debt allowlists (`paseo/no-sync-io`) — never directory-wide disables — and unit-tests its own lint rules in CI.
- **Independent, anti-vacuous verification (stop agents from gaming tests):**
  - **Verification Skill Independence (`OpenHands`):** `verify-skill-isolation.yml` blocks PRs from modifying both production code and verification skills/evals in the same PR.
  - **Diff-scoped mutation testing (`OpenHands`):** `stryker-diff.mjs` proves newly written tests kill mutants on changed lines rather than merely padding line coverage.
  - **Uncommitted local QA evidence + `sha256sum` proof (`oh-my-openagent`):** Save real-surface QA captures to gitignored `.omo/evidence/`, paste excerpts + `sha256sum` into the PR body, and fail CI if any evidence file is accidentally committed (`tracked-evidence-paths-audit.test.ts` / `t3code`'s `.github/pr-assets` check).
  - **Honest coverage disclosures (`cmux`, `beads`):** Require `### Observed / Not run` in PR bodies, treat skipped CI jobs as *not* coverage, verify filtered test runs executed >0 tests, and require `NOT_ENOUGH_INFO` when evidence runs out.

---

## 4. CI, Supply Chain, Data & LLM Ops

- **Stay in the CI Goldilocks zone (12–30 focused workflows):**
  - `0` workflows (`1code`) leads to instant rot.
  - `231` workflows (`cmux`) causes the CI factory itself to consume ~80% of daily commits on `main`.
  - Pair **path-filtered CI** with **one `if: always()` `CI required` aggregator job** (`codex`, `t3code`) and **one fast local diff-scoped checker** (`vp run check:changed`, `pnpm verify`, `verify-local.py --receipt -`) so agents never waste 15 minutes running full-repo suites locally.
- **10-line npm supply-chain shield (`codex`, `openclaw`, `OpenHands`, `paseo`):**
  - `minimumReleaseAge: 10080` (7-day npm cooldown) + `blockExoticSubdeps: true` + explicit `allowBuilds`/`onlyBuiltDependencies` + dated expiry comments on exemptions + `lockfile-lint`.
- **Database & deployment proofs that catch real outages:**
  - Prefix migrations with `lock_timeout = '5s'` + `pipefail` (`Paradev`).
  - Run a real Postgres `pg_dump` → restore → verify job in CI (`paperclip`).
  - Build the production Docker image in CI, boot it, and `curl` its health check (`bolt.diy`).
  - Test shell installers twice in an isolated `$HOME` + unreachable-mirror fallback (`oh-my-openagent`).
- **If you ship LLM/agent features:**
  - Add a **`prefix-stability.test.ts`** (`openclaw`) guaranteeing system prompts and tool definitions remain byte-stable across turns so provider KV prompt caching never silently busts.
  - Gate behavioral `evals/` (`gemini-cli`, `t3code`) behind a two-stage maintainer-labeled `pull_request_target` workflow (`eval-pr.yml`).

---

## 5. Multi-Agent Safety & Open-Source Governance

- **Assume 3–5 agents share the same developer machine concurrently:**
  - Isolate dev state per checkout (`.dev/<app>-home`, `paseo`; templated `pnpm env:up/seed`, `happy`).
  - Ban `git add -A`, `git stash`, and `git reset --hard`; review PRs without switching branches (`pi`).
  - Never kill processes by pattern or touch live user installs/DBs (`t3code`, `cmux`).
  - Add root meta-tests catching tests that write to real `$HOME` or leak temp files (`oh-my-openagent`).
  - Release **only** from a clean local `main` verified equal to freshly fetched `origin/main` — never from a worktree (`happy`).
- **If your repository is public, gate contributions before the AI PR flood hits:**
  - Open trackers collapse (`codex`: **28,619** open issues).
  - Gated trackers stay healthy: `pi` default-closed `lgtmi`/`lgtm` (**307** open issues at 123.8k★ — a **93×** reduction vs. Codex), `goose` `Ready`-board gate (**512**), `t3code` `VOUCHED.td` + PR size/count limits, `paseo` *"PRs closed by default"* + 3,000-line cap, `OpenHands` required `HUMAN:` PR section, and `cline` auto-stripping agent promo footers.

---

## 6. Skill Stacks (`gstack`, `pstack`, `mattpocock/skills`, `superpowers`, `spec-kit`, `OpenSpec`, `BMAD`, `GSD`)

Auditing the top **10 agent skill & workflow repos** (~1.17M stars) revealed a sharp split between **harness engineering** and **skill-stack engineering**:

- **Skills do not boost raw bug-fix rates — they enforce alignment, review, QA, and safety:** `garrytan/gstack` published an honest head-to-head benchmark right in its `README.md`: on 100 real GitHub bugs/features, Opus 5.5 solved **58 with `gstack`** vs. **61 of 99 without it** (and 29 vs. 29 on security fixes). Use skills for `/grill-me` alignment (`mattpocock/skills`), formal verification (`pstack`'s TLA+/Lean), browser QA, and shipping checklists — rely on **mechanical repo gates** for code quality.
- **Composable skills beat heavyweight SDLC frameworks:** `mattpocock/skills` (332.8k★) explicitly warns that process-owning stacks (`GSD`, `BMAD`, `Spec-Kit`) hide failure modes; `gsd-build/get-shit-done` (64.1k★) archived after a May 2026 compromise warning (`open-gsd/gsd-core`), and `gstack` swelled to **45.1 MB TS + 38 workflows** just to test its own skills.
- **Standout mechanical wins from Chunk 6:**
  - **`mattpocock/sandcastle`:** All-5-category type-aware `oxlint` straitjacket + **`lint-shrink.yml` bot** (automatically lowers debt baselines and raises the E2E coverage floor on every push to `main`) + `tests/docs-guide.test.ts` + real Bubblewrap/Windows/macOS containment CI.
  - **`mattpocock/skills` & `pstack`:** Always start subagents with a **fresh context window** (Codex forks parent context by default); pair `disable-model-invocation: true` with `agents/openai.yaml` so Codex doesn't auto-load explicit skills; use `pstack-claude`'s **`tools/forks.json`** to mechanically track every fork from upstream.
  - **`garrytan/gstack`:** Prompt/catalog token-budget ratchets (`2,292` token cap), **`egress-receipt-wiring.test.ts`** (fails CI on any unreceipted outbound network call), and pre-registered eval panels with a hard `$150/wk` spend cap.
  - **`github/spec-kit` & `Fission-AI/OpenSpec` & `BMAD`:** Firewall-sandboxed GitHub Agentic Workflows (`gh-aw`), **`startup-modules.test.ts`** CLI cold-start guards, *"length and ambiguity are paid on every run; prefer deleting to hedging"*, and `obra/superpowers`'s **94% PR rejection rate** anti-slop gate.

---

## 7. The 7 Fatal Traps to Avoid

1. **Shipping without CI, linter, or tests** (`1code`).
2. **Polyglot / multi-surface scope sprawl ahead of team size** (`vibe-kanban`, `cmux`).
3. **Human-less autonomous merging with `--override` waivers onto a red `main`** (`cmux`).
4. **Warning-only lint (`"info"`/`"off"`) or `continue-on-error: true` on quality gates** (`cline` legacy, `bolt.diy`) — agents ignore anything non-blocking.
5. **Committing generated bundles or scratch/evidence files into git** (`oh-my-openagent`, `costrict`) — causes endless worktree merge conflicts.
6. **Storing user API keys in JS-accessible browser cookies** (`bolt.diy`).
7. **Forgetting to delete replaced code and docs in the same PR** (`openclaw`'s *"one owner, complete cutover"* rule prevents zombie paths).

---

## 8. Minimum Viable Upgrade (First 6 Changes to Ship)

1. Trim `AGENTS.md` to <180 incident-cited lines, symlink `CLAUDE.md`, and add `Doc voice` + *"Choose good compromises"* + multi-agent Git safety rules.
2. Create a 1-page **`REVIEW.md`** seeded from your last 10–15 real PR review catches.
3. Add **`minimumReleaseAge: 10080` + `allowBuilds`** to `pnpm-workspace.yaml`.
4. Encode your top 3–5 architectural/security invariants as **hard lint errors** (and disallow silent `eslint-disable`).
5. Add one fast diff-scoped local command (`verify` / `check:changed`) + `knip` + a single `CI required` aggregator job.
6. Add **`### Observed / Not run`** to your PR template and a CI check rejecting committed temporary evidence/scratch files.
