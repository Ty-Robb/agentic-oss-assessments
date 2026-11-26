# Sandcastle (`mattpocock/sandcastle`)

- **Snapshot:** `9,277★` · `997` forks · `137` open issues · `MIT` · Active (created Mar 17, 2026; pushed 2026-11-18)
- **Primary Stack:** **2.6 MB TypeScript** (`@ai-hero/sandcastle`), TypeScript 7 (`@typescript/native`), Effect (`effect` 3.20 + `@effect/language-service`), **`oxlint` + `oxlint-tsgolint`**, Biome (formatter only), Vitest, `tsup`, `@microsoft/api-extractor`, `dependency-cruiser`, Changesets; supports Bubblewrap (Linux/WSL2), Seatbelt (macOS), Docker, Podman, E2B, Daytona, Modal, Fly Sprites, and Vercel Sandboxes.
- **Data source:** [`data/chunk-06/mattpocock__sandcastle.json`](../../data/chunk-06/mattpocock__sandcastle.json)

## 1. Agent Instruction & Docs Hygiene
- **41-line `AGENTS.md` (5.0 KB) paired with mechanically tested user docs (`tests/docs-guide.test.ts`):**
  - Explicitly documents the TypeScript 7 (`tsc`) vs. TypeScript 6 (`typescript` alias for `tsup`) split and bans importing `typescript` in app code.
  - Treats `GLOSSARY.md` as the agents' terminology source and `docs/guide/glossary.md` as the hand-written reader glossary — and **enforces doc integrity in Vitest (`tests/docs-guide.test.ts`)**: fails CI if `docs/guide/`, `toc.json`, `README.md`, and `GLOSSARY.md` drift, if a term's first mention isn't linked, if `First explained in` points to the wrong home page, or if any user doc leaks an internal `docs/adr/` link!
- **Minor nit:** `CLAUDE.md` is a byte-for-byte duplicate of `AGENTS.md`.

## 2. Mechanical Gates & Quality Control
- **Arguably the tightest, cleanest small-repo engineering straitjacket in the entire 35-repo study:**
  1. **All-5-category type-aware `.oxlintrc.json` ("The straitjacket"):** Enables **`correctness`, `suspicious`, `pedantic`, `perf`, AND `style` all at `"error"`** with `typeAware: true` (`oxlint-tsgolint`), `reportUnusedDisableDirectives: "error"`, `eslint/complexity: max 15`, `max-statements: 20`, `import/no-cycle`, and **`eslint/no-restricted-properties` banning `Effect.runPromise`/`runSync`/`runFork`/`runCallback` everywhere except named entry points!**
  2. **Automated shrink-only ratchet bot (`lint-shrink.yml`):** Tracks 4 baselines (`lint-baseline.json`, `test-baseline.json`, `typecheck-baseline.json`, `coverage-baseline.json`). Fix PRs never need manual baseline edits; after every push to `main`, `sandcastle-agent[bot]` automatically opens/updates a PR lowering violation baselines and raising the E2E coverage floor (*"counts only fall and the floor only rises"*).
  3. **Public API boundary enforcement:** Runs `@microsoft/api-extractor` (`api-report/` diff routed via `CODEOWNERS` to Matt) AND `scripts/check-public-types-effect-free.mjs` (proving internal Effect types never leak into the public Promise API!).
  4. **Real OS sandbox proofs in CI (`ci.yml`):** Installs real **Bubblewrap** (`bwrap`) on Ubuntu, lifts AppArmor userns restriction (`kernel.apparmor_restrict_unprivileged_userns=0`), and **fails rather than skips** if `bwrap` cannot run; also runs real **Windows (`cmd.exe`)** and **macOS (Seatbelt)** E2E suites and merges Windows E2E coverage artifacts into `coverage-gate.ts`.
  5. **Safe label-driven autonomous agent workflows (`agent-explore.yml`, `agent-implement.yml`, `agent-implement-pr.yml`, `agent-review.yml`, `agent-update-branch.yml`):** Explicitly runs on `pull_request` (not `pull_request_target`) so fork PRs never get secrets, serializes per-PR mutations via `concurrency`, and pushes with exact-SHA `--force-with-lease="refs/heads/$BRANCH:$BRANCH_HEAD_SHA"`.

## 3. Architectural Bets & Craft
- **Composable sandboxed agent runner (`sandcastle.run()`):** Clean provider-agnostic TypeScript library wrapping local OS sandboxes (Bubblewrap, Seatbelt), containers (Docker, Podman), and cloud sandboxes (Daytona, E2B, Modal, Fly Sprites, Vercel) with configurable branch/merge strategies and subpath exports.
- **Effect internally, plain Promises externally:** Uses Effect + `@effect/language-service` for internal composition and typed errors while enforcing zero Effect leakage at the public boundary.
- **Dogfoods itself:** `.sandcastle/agent-workflows/` runs Sandcastle + Claude Code to implement and review PRs in its own repo.

## 4. Commit, PR & Maintenance Reality
- **Hyper-disciplined agent-assisted velocity:** **50 commits in 5.9 days** (`2026-11-10` to `2026-11-16`), **98% conventional commits**, **8% fix/revert**, **98% AI signal** (`mattpocock` 48/50 recent; 1,725 all-time + `sandcastle-agent[bot]` 104 all-time).
- The recent commit log shows the shrink-only ratchet actively working in real time: dozens of tiny, focused `chore(lint): split ... under max-lines` and `chore(lint): type-guard ...` PRs burning down baseline debt cleanly.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Automated shrink-only ratchet PR bot (`lint-shrink.yml`)** for lint, typecheck, test debt, and E2E coverage floor — zero friction on feature PRs, guaranteed monotonic improvement on `main`.
  2. **`oxlint` all-5-category straitjacket (`typeAware: true`) + `no-restricted-properties`** locking architectural boundaries (`Effect.run*` at entry points only).
  3. **Mechanically tested docs/glossary sync (`tests/docs-guide.test.ts`)** + **`api-report/` diff** routed to maintainers via `CODEOWNERS` + `check-public-types-effect-free.mjs`.
  4. **Fail-don't-skip containment CI** (proving real `bwrap` / Windows `cmd.exe` / macOS Seatbelt rather than silently skipping).
  5. **Exact-SHA `--force-with-lease="refs/heads/$BRANCH:$BRANCH_HEAD_SHA"`** in automated PR-mutating agent workflows.
- **Avoid:**
  1. **Enabling `pedantic` + `style` + `max-statements: 20` on an existing large team repo without a shrink-only baseline** — works brilliantly here *only* because `scripts/lint-ratchet.ts` + `lint-shrink.yml` absorb legacy debt cleanly.
