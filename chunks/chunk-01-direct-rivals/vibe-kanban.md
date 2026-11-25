# Vibe Kanban (`BloopAI/vibe-kanban`)

- **Snapshot:** `28,814★` · `3,072` forks · `537` open issues · `Apache-2.0` · **Sunsetting** (README banner: *"Vibe Kanban is sunsetting"*; last pushed 2026-11-15)
- **Primary Stack:** 30-crate Rust workspace (`axum`, `tokio`, `sqlx`, `git2`, `ts-rs`, `tauri`) + pnpm TypeScript monorepo (`local-web`, `remote-web`, `web-core`, `ui`) + `npx-cli` wrapper.
- **Data source:** [`data/chunk-01/BloopAI__vibe-kanban.json`](../../data/chunk-01/BloopAI__vibe-kanban.json)

## 1. Agent Instruction & Docs Hygiene
- **Compact root `AGENTS.md` (59 lines / 4.1 KB):** Crisp module map, exact build/typegen/check commands, and pointers to crate/package-local guides (`crates/remote/AGENTS.md`, `docs/AGENTS.md`, `packages/local-web/AGENTS.md`).
- **Avoidable duplication:** `CLAUDE.md` is an exact 59-line copy-paste of `AGENTS.md` instead of an `@AGENTS.md` symlink/include — guaranteed drift hazard.
- **Mintlify docs + leftover scratch:** 25 top-level entries in `docs/` including a stale `frontend-ui-library-refactor-audit.md` and root `mobile-testing.md` left behind in the repo.

## 2. Mechanical Gates & Quality Control
- **Strong Rust↔TS contract integrity:**
  - `ts-rs` generates `shared/types.ts` and `shared/remote-types.ts` directly from Rust structs (`#[derive(TS)]`), enforced in CI with `generate-types:check`.
  - `sqlx` offline query verification (`prepare-db:check` and `remote:prepare-db:check`) ensures SQL compiles against schema without a live DB.
  - `cargo clippy --workspace --all-targets -- -D warnings` (warnings as errors).
- **Practical frontend ratchets:** `check-unused-i18n-keys.mjs` and `check-legacy-frontend-paths.sh` (paired with `legacy-frontend-paths-allowlist.txt`) prevent regressions during UI refactors.
- **Path-filtered CI (`test.yml`):** Uses `dorny/paths-filter` to isolate `frontend`, `backend`, `backend-remote`, and `tauri` jobs so PRs only pay for touched subsystems.
- **CI/release fragility:** Pinned to **Rust nightly** (`nightly-2026-08-01`), a **1,166-line `pre-release.yml`**, and private deploy-key dependencies (`VK_PRIVATE_DEPLOY_KEY`) inside a public repo — recent commit `#3484` even added a local CI script to run workflow checks without GitHub Actions, and `#3507` moved releases to a local script.

## 3. Architectural Bets & Craft
- **Clever distribution (`npx vibe-kanban`):** Ships a Rust server + React SPA via an `npx` CLI wrapper for zero-install onboarding, later adding Tauri desktop + cloud/ElectricSQL remote sync + WebRTC/WS relay + embedded SSH.
- **Severe scope/crate explosion for team size:** 30 workspace crates plus 2 excluded crates (`crates/remote`, `crates/relay-tunnel`), dual databases (SQLite local + Postgres/ElectricSQL remote), dual frontends (`local-web` + `remote-web`), Tauri wrapper, and relay infrastructure. That architecture demands a 15-person systems team, not a 4-person startup.
- **Multi-agent adapter convergence:** Recent late-2026 commits show Vibe Kanban migrating toward the **ACP registry** (`feat: install and run agents from the ACP registry (#3489)`) rather than maintaining bespoke wrappers for every CLI — validating T3 Code's and Emdash's bet on ACP.

## 4. Commit, PR & Maintenance Reality
- **Slowing cadence post-sunset:** Last 50 commits span **7.5 months** (2026-03-31 to 2026-11-15), with **46% carrying explicit AI co-author signals** (highest in Chunk 1) as 1–2 maintainers (`anastasiya1155`, `stunningpixels`) keep critical ACP/Copilot/Codex compatibility alive and turn off analytics/crash reporting (`#3503`).
- **Commit hygiene:** 64% conventional commits (mix of `bugfix:`, `feat:`, and plain sentences), 28% fix/revert.
- **Ecosystem overlap:** Theo (`t3dotgg`) actually has 4 early contributions in `top_contributors` — highlighting how directly T3 Code learned from Vibe Kanban's early wins and pain points.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Single-source typegen + CI drift check** (`generate-types:check`, `prepare-db:check`) whenever bridging two runtimes/languages.
  2. **Refactor allowlist ratchets** (`scripts/check-legacy-frontend-paths.sh` + allowlist file) so migrations only move forward.
  3. **Zero-friction `npx <tool>` local server launch** as an onboarding wedge.
  4. **Path-filtered CI matrix** (`dorny/paths-filter`) when mixing slow compiled backends with fast TS frontends.
- **Avoid:**
  1. **Architectural over-indexing before product-market durability:** 30 Rust crates + ElectricSQL + WebRTC relay + Tauri + Rust nightly is a massive maintenance anchor for a small team.
  2. **Copy-pasting `AGENTS.md` into `CLAUDE.md`** instead of referencing `@AGENTS.md`.
  3. **1,100+ line YAML release workflows** coupled to private SSH deploy keys — impossible for community maintainers to keep running after a company pivots.
