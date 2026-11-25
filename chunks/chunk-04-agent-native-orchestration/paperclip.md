# Paperclip (`paperclipai/paperclip`)

- **Snapshot:** `116,922★` · `19,415` forks · `6,812` open issues · `MIT` · Active (created Mar 2, 2026; default branch `master`; pushed 2026-11-25)
- **Primary Stack:** TypeScript pnpm + Turborepo monorepo (**157.8 MB TypeScript**, 4.75 MB Rust `paperclip-runner`), Express REST API (`server/`), React + Vite board UI (`ui/`), Drizzle + embedded/external Postgres (`packages/db/`), `cli/`, `packages/adapters/*`, `packages/plugins/*`, Vitest, Playwright, Storybook, Promptfoo (`evals/promptfoo/`), Allure TestOps.
- **Data source:** [`data/chunk-04/paperclipai__paperclip.json`](../../data/chunk-04/paperclipai__paperclip.json)

## 1. Agent Instruction & Docs Hygiene
- **Header-indexed `rules/*.mdc` progressive disclosure (`AGENTS.md`, 221 lines / 10.9 KB):**
  - Instead of stuffing every architectural rule into `AGENTS.md`, Paperclip stores scoped rules in `rules/*.mdc` with frontmatter (`description`, `globs`, `alwaysApply`) and instructs agents to run `grep -E '^(description|globs|alwaysApply):' rules/*.mdc` first — reading full bodies only when a design decision requires it.
  - Also pairs with **37 `.agents/skills/`** (`verify-paperclip`, `create-verification-skill`, `maintain-verification-skill`, `fix-slow-queries`, `diagnose-why-work-stopped`, `pr-gardening`, `test-audit`, `honeycomb-tracing`, `terminal-bench-loop`) and machine-checked **`maps/feature-map/` + `maps/agent-access-map/`** (`check-maps.mjs`).
- **Explicit truth hierarchy:** States right in section 1 that *code and tests are source of truth; `doc/` is background and may be stale*.
- **Dogfooding-aware PR hygiene (`CONTRIBUTING.md`):**
  - **"No Internal Issue References"** rule prevents contributors running their own Paperclip instances from leaking private ticket IDs (`PAPA-123`) or `localhost` URLs into public PR bodies and branch names.
  - Mandatory **duplicate-PR search checkbox** verified by `commitperclip` bot.
  - Two bold mechanical anti-bloat PR rules: **never push a code file across 1,000 lines**, and **zero code comments in PRs**.

## 2. Mechanical Gates & Quality Control
- **Best incremental local verification ergonomics (`pnpm verify` + exit code 2):**
  - `pnpm verify` selects affected Vitest files using CI's exact conservative dependency policy (covering committed + staged + unstaged + untracked changes against `origin/master`), supports `--explain` and caching, and returns **exit code 2** when a change is too broad for incremental local proof — explicitly instructing agents *not* to blindly fall back to a full repo-wide run!
  - Even ships `scripts/typecheck-low-memory.mjs` for constrained agent sandboxes and `scripts/agent-preflight.mjs` to bootstrap new worktrees.
- **Real PostgreSQL backup & restore qualification CI (`backup-checkpoint-qualification.yml`):** Spins up Postgres 17, runs real `pg_dump` + `psql` restore into a clean DB via wrapper scripts bound to the container's matching client binaries, runs Vitest verification, and uploads a `qualification.json` evidence receipt!
- **41 workflows covering chaos, crash points & TestOps:** `crash-points.yml`, `runner-chaos-evals.yml`, `runner-live-evals.yml`, `runner-protocol-live-evals.yml`, `ci-work-benchmark.yml`, `ci-test-durations.yml`, `storybook-visual.yml`, `sentry-contract.yml`, `commitperclip-review.yml`, plus custom scripts (`check:tokens`, `check:token-gates`, `check:no-git-push`, `check:module-boundaries`, `check:node-version`).
- **Strong security boundary in TestOps workflows (`chat-catalog-testops-case.yml`):** Checks out trusted helpers from `github.sha` into `.testops-trusted`, verifies the untrusted target SHA does not own `.testops-trusted`, verifies SHA-256 checksums of build artifacts, and runs with `NODE_OPTIONS=''` and `AWS_EC2_METADATA_DISABLED='true'`.
- **Gap:** No root `.oxlintrc.json` or `biome.json` detected (relies on custom `check:*` scripts, `rules/*.mdc`, Greptile 5/5 score requirement, and `commitperclip` review).

## 3. Architectural Bets & Craft
- **Org-level control plane above coding agents:** Treats agents as employees inside a company with strict domain invariants enforced everywhere: company-scoping on every entity/route, single-assignee tasks, atomic issue checkout, approval gates, hard-stop budget auto-pause, and full mutation activity logs.
- **Core vs. Deployment Policy separation:** Explicitly forbids hardcoding Cloud allowlists or deployment defaults into Core (`AGENTS.md` rule 5), keeping OSS Core generic and cleanly deployable.
- **Rust runner + Node/TS server hybrid:** Runs a TypeScript/Express control plane with a 4.75 MB Rust `paperclip-runner` and patches 11 upstream packages (`embedded-postgres`, `acpx`, Claude/Codex ACP adapters, Slack/Discord/Telegram/Teams chat adapters) to smooth multi-agent execution.

## 4. Commit, PR & Maintenance Reality
- **Blistering founder+agent velocity:** **50 commits in 14.5 hours** (PR `#22,930` in just 8.5 months!), **94% conventional commits**, **56% fix/revert**, **58% explicit AI co-author trailers** (and PR template requires a `Model Used` field).
- **Highly concentrated core:** `cryppadotta` accounts for **5,675 contributions** (39 of last 50 commits!), with `devinfoley` (1,123) and `nickyleach` (585) next — while `open_issues` has surged to `6,812`.

## 5. Steal vs. Avoid
- **Steal:**
  1. **`grep`-indexed `rules/*.mdc` frontmatter** so agents scan all architectural rules in one cheap grep and load full bodies only when relevant.
  2. **`pnpm verify` with `--explain` and exit-code-2 ("too broad, let CI handle full suite")** — huge time/token saver for agents.
  3. **Real DB backup/restore CI (`backup-checkpoint-qualification.yml`)** and **`crash-points.yml` / `runner-chaos-evals.yml`** for durable systems.
  4. **1,000-line file ceiling rule** in PR review + **`scripts/agent-preflight.mjs`** for one-command worktree readiness.
  5. **Feature maps & agent access maps** (`maps/`) separating *coverage scope* from *live verification proof*.
- **Avoid:**
  1. **Relying on Greptile scores + prose `rules/*.mdc` without a fast root static linter (`oxlint`/`biome`)** — static lint rules catch violations in milliseconds before PR review.
  2. **Committing `doc/plans/` AND `docs/plans/` AND `screenshots/` into the main repo** alongside 158 MB of source — creates dual-docs drift (`doc/` vs. `docs/`).
