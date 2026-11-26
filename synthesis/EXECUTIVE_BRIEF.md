# Everything You Need to Know: Lessons from 36 Agentic OSS Repositories

*Executive brief distilled from primary-source GitHub API audits of **36 public coding agent, harness, orchestration, and skill-stack repositories** (**3,040,947 / ~3.04M combined stars** from the 35 standalone repos, snapshot date: **2026-11-25**; path-scoped `cursor/plugins/pstack` added 2026-11-26 and excluded from the star sum), fact-checked and red-teamed by Codex (`gpt-6.2-astra`), Claude (`claude-opus-5-5`), and Grok (`grok-4.7`). For the full 36-repo matrix, caveats, and Week 1–3 plan, see [`PLAYBOOK.md`](PLAYBOOK.md) and [`MULTI_MODEL_REVIEW.md`](MULTI_MODEL_REVIEW.md).*

---

## 1. The Macro Picture: Who Thrives and Who Stalled

Across all 36 public repositories, **durable velocity correlates with mechanical discipline and scope matched to team size — not launch hype.**

- **What archived or sunset (4 of the 35 star-counted repos, for distinct reasons):**
  - **`21st-dev/1code`** (5.6k★, **archived**, 7 weeks creation-to-last-push): One-way public mirror (`sync-to-public.sh`) with zero public CI/tests, dual lockfiles, and stale WIP docs.
  - **`BloopAI/vibe-kanban`** (28.8k★, **sunsetting**): Strong Rust craft (`ts-rs`, `sqlx`, `clippy -D warnings`), carrying 30 Rust crates + ElectricSQL + WebRTC relay + Tauri + Rust nightly on a small team.
  - **`RooCodeInc/Roo-Code`** (24.2k★, **archived May 2026**): Remained coupled to a VS Code extension while surviving peers (`Cline`, `OpenHands`, `Goose`) decoupled into SDKs + multi-surface ACP control planes.
  - **`gsd-build/get-shit-done`** (64.1k★, **archived May 2026**): Security/governance event — commit `126b6b9e` warned the repo *"appears compromised"* and README migrated users to `open-gsd/gsd-core`.
- **Where the active leaders converged:**
  - **Architecture:** TypeScript monorepo + local daemon/server + multi-surface clients + **ACP** (`t3code`, `orca`, `Paradev`, `emdash`, `paseo`, `OpenHands`, `Goose`).
  - **Mobile split:** Cross-platform Expo/RN (`t3code`, `paseo`, `orca`) or pure native Swift + Kotlin (`slopus/happy`, which ripped out Expo/EAS after a stale-worktree preview OTA rollback).
  - **Autonomous maintenance bots in prod:** `gascity-eddie[bot]` (`41/50` recent commits in `beads`), `paseo-bot[bot]` (`15/50` in `paseo`), `orca-remote-automation[bot]` (`orca`), `lint-shrink.yml` (`sandcastle`), and `opencode-agent[bot]` (`2,766` commits in `opencode`) — all constrained by strict lint/CI gates.

---

## 2. How to Run `AGENTS.md` & Docs

Prompts work best as a **check command, trap list, and router**, not an encyclopedia.

- **Single source of truth:** Put a 1-line `@AGENTS.md` include in `CLAUDE.md` (`t3code`, `Paradev`, `emdash`, `beads` — safer than symlinks on Windows). Keep root `AGENTS.md` lean (`openclaw` caps at <20 KB) and move deep guides into `docs/agents-md-refs/` (`orca`) or `grep`-indexed `rules/*.mdc` (`paperclip`).
- **Every new rule cites an incident (`openclaw`, `happy`)** and **"prefer deleting an instruction to hedging it" (`BMAD`).**
- **Ban LLM over-engineering (`openclaw` — *"Choose good compromises"*)** and **LLM prose slop (`paseo` — `Doc voice`)**: forbid `"It's not X, it's Y"`, `"robust"`, `"seamless"`, `"and that matters"`, and append-only doc edits.
- **Maintain a compact `REVIEW.md` (`cmux`)** seeded strictly from your real PR review catches (never fabricated rules).

---

## 3. Mechanical Quality Gates & Anti-Test-Slop

When an agent makes a mistake twice, **move the rule out of prose and into a lint error or CI check.**

- **Custom `oxlint` / Biome plugins & baselines:**
  - **`mattpocock/sandcastle`:** 5 `oxlint` categories (`correctness`/`suspicious`/`pedantic`/`perf`/`style`) at `"error"` + type-aware `oxlint-tsgolint` + **`lint-shrink.yml` PR bot** lowering lint/typecheck baselines automatically on `main`.
  - **`stablyai/orca`:** 5 surgical `oxlint` plugins (`quadratic-buffer-concat`, `ime-enter-guard`, `app-store-performance`, `anti-slop-prefilter`, `renderer-scrollbar-style`), `no-restricted-imports` guarding lazy `@linear/sdk` loading, and `main-blocking-work.yml` ratcheting main-process sync spawns.
  - **`opencode`:** Custom `anti-slop` plugin + unit-tested `ast-grep` rules (`no-widen-then-assert`, `no-module-mocking`).
  - **`emdash` & `paseo`:** `respectEslintDisableDirectives: false`, sole-writer DB table bans, and per-file, per-API allowlists (`paseo/no-sync-io`).
- **Unified verification rule (resolving test-bloat vs. test-gaming):**
  1. **Test selectively (`orca`):** `"Tests are the exception"` — commit automated tests only for costly silent regressions (parsers, security boundaries, persistence, concurrency, cross-platform paths), delete brittle UI/mock tests, and post PR test-vs-prod LoC counts via zero-checkout `pr-test-loc.yml`.
  2. **Keep grading independent (`OpenHands`):** `verify-skill-isolation.yml` blocks PRs from editing both production code and `.agents/skills/verify-*/` together; `stryker-diff.mjs` mutation-tests critical diffs.
  3. **Disclose honestly (`cmux`, `oh-my-openagent`, `beads`):** Require `### Observed / Not run` + `## Performance` (`"None, because ..."` allowed), keep local QA captures gitignored (`.omo/evidence/` + anti-commit CI check), and verify filtered tests ran >0 subtests.

---

## 4. CI, Supply Chain, Data & LLM Ops

- **Match CI to team size (typically 8–30 YAML workflows for small/mid teams):**
  - Pair path-filtered CI with one **`if: always()` `CI required` aggregator** (explicitly failing on `failure`/`cancelled`, treating `skipped` as success only when caused by path filters) and one **cached diff-scoped local command** (`pnpm check:changed` — *"do not also re-run the full suite"*).
  - High-workflow stacks (`openclaw` 133, `orca` 67, `gemini-cli` 47) require dedicated runner/cache maintenance; at the extreme (`cmux`, 231 YAML workflows), ~17 of 20 stored Nov 25 commit subjects (19/20 by `teamleaderleo`, 1 CI commit by `austinywang`) touched CI/release maintenance.
- **Supply-chain locks (`codex`, `openclaw`, `orca`, `OpenSpec`, `paseo`):** `minimumReleaseAge` (3d `4320` or 7d `10080`), commented `allowBuilds`, dated expiry comments + sweeper, GHSA overrides in `pnpm-workspace.yaml`, and `lockfile-lint`.
- **Trigger-gated infra proofs:** `lock_timeout = '5s'` migrations (`Paradev`), CI Postgres `pg_dump`/restore (`paperclip`), prod Docker `curl` health check (`bolt.diy`), real `bwrap` OS-sandbox CI (`sandcastle`), `prefix-stability.test.ts` (`openclaw`), and `eval-gate` environment-approved behavioral `evals/` (`gemini-cli`: 38 `*.eval.ts` files).

---

## 5. Multi-Agent Safety & Public OSS Governance

- **Multi-agent machine isolation:** Checkout-local `.dev/` state (`paseo`), ban `git add -A` / `git stash` / `git reset --hard` (`pi`), hidden-window `ORCA_BACKGROUND_LAUNCH=1` (`orca`), never kill processes by pattern (`t3code`), hermetic `$HOME` meta-tests (`oh-my-openagent`), and release only from clean `main == origin/main` (`happy`).
- **Public tracker reality:** GitHub's `open_issues_count` combines open issues and PRs. Open trackers grow huge (`codex`: `28,619`; `orca`: `9,918`), while strict gates shrink queues (`pi`: `307` via auto-close on arrival; `superpowers`: `372` with a maintainer-reported 94% PR rejection rate; `goose`: `512` via `Ready`-board gate; `t3code`: `3,681` via `VOUCHED.td` + PR limits).

---

## 6. Skill Stacks (`mattpocock/skills`, `sandcastle`, `gstack`, `pstack`, `superpowers`, `spec-kit`, `OpenSpec`, `BMAD`, `GSD`)

- **Workflow discipline vs. raw fix rate:** In `garrytan/gstack`'s self-reported 100-task Opus 5.5 benchmark, the model solved **58% (58/100) with `gstack`** vs. **61.6% (61/99) without it** (29/60 each on security fixes). Use skills for alignment, review checklists, and safety workflows — rely on mechanical repo gates for code quality.
- **Standout mechanical wins from Chunk 6:** `sandcastle`'s 5-category `oxlint` + `lint-shrink.yml` + `tests/docs-guide.test.ts`; `mattpocock/skills`'s installer-parser YAML check + dual Claude (`disable-model-invocation: true`) & Codex (`agents/openai.yaml`) parity; `gstack`'s `catalog-budget.test.ts` (`2,292` tokens) + `egress-receipt-wiring.test.ts`; `github/spec-kit`'s firewall-sandboxed `gh-aw` workflows (19 YAML workflows); `OpenSpec`'s `startup-modules.test.ts`; and `pstack-claude`'s `tools/forks.json` fork tracker plus port-only Lean `WatchPoll.lean` and extra TLA+ (`PiScheduler.tla`); upstream `cursor/plugins/pstack` ships the TLA+ corpus and formal-verification skills without Lean.

---

## 7. Minimum Viable Week 1 Upgrade

1. Lean `AGENTS.md` + 1-line `@AGENTS.md` in `CLAUDE.md` (with `Doc voice`, *"Choose good compromises"*, multi-agent Git safety, and `orca`'s **`"Tests are the exception"`** rule).
2. One **cached diff-scoped local check** (`check:changed` / `verify`) — instruct agents not to also run the full suite.
3. PR template with `### Observed / Not run` + `## Performance` (`"None, because ..."` allowed) + zero-checkout `pr-test-loc` summary.
4. Seed `REVIEW.md` from real PR history (only if history exists).
5. In Week 2, commit baselines first, turn your top 3–5 real review catches into hard lint errors, add a lint/typecheck-only shrink bot, and wire one explicit `if: always()` `CI required` aggregator.
