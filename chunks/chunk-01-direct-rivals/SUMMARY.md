# Chunk 1 Summary — Direct T3 Code Rivals (Worktree Orchestration GUIs)

*Snapshot date: 2026-11-25. Baseline: `pingdotgg/t3code` (78.8k★).*

## Side-by-Side Matrix

| Repo | Stars | Status | Primary Stack | `AGENTS.md` / `CLAUDE.md` | Lint / Static Gates | CI Workflows | Last-50 Velocity & Hygiene |
| --- | ---: | --- | --- | --- | --- | ---: | --- |
| **`pingdotgg/t3code`** *(baseline)* | 78.8k | Active | TS (Effect-TS, Vite+, Electron, RN) | 157 lines + `@AGENTS.md` + `docs/internals/` + 4 skills | Custom `oxlint` plugin, `knip`, `check:changed`, `evals/`, PR limits/vouch | 29 | 50 commits / **7 hrs** · 100% conv · 86% fix · 12% AI |
| **[`stablyai/orca`](orca.md)** | **137.8k** | Active | TS (143.7 MB, Electron, Web, Mobile, `orcad`, Ghostty, native Win addons) | Operational `AGENTS.md` + `docs/agents-md-refs/` (`"Tests are the exception"`) | 5 custom `oxlint` perf/IME plugins, `main-blocking-work`, `pr-test-loc`, `pr-description` perf gate, shadow test selection, 3d npm cooldown | **67** | 50 commits / **3.2 hrs** · 88% conv · 70% fix · 0% AI |
| **[`ParadevAI/Paradev`](paradev.md)** | 16.6k | Active | TS (Bun, Turbo, Electron, Next, Expo, tRPC, Drizzle) + TLA+ | 292 lines + `@AGENTS.md` + 16 `.agents/skills/` | `biome.jsonc` domain `noRestrictedImports` ratchets, `sherif`, `vale`, `check:i18n`, `check:durable-objects` | 22 | 50 commits / **3.2 days** · 98% conv · 36% fix · 0% AI |
| **[`BloopAI/vibe-kanban`](vibe-kanban.md)** | 28.8k | **Sunsetting** | 30-crate Rust (`axum`/`sqlx`/`ts-rs`/`tauri`) + pnpm React | 59 lines + duplicated 59-line `CLAUDE.md` + crate guides | `clippy -D warnings`, `ts-rs` typegen check, `sqlx` offline check, i18n & legacy-path ratchets | 9 | 50 commits / **7.5 mos** · 64% conv · 28% fix · 46% AI |
| **[`generalaction/emdash`](emdash.md)** | 6.3k | Active | TS (pnpm, Nx, Electron, Drizzle, Wire RPC, MobX) | 419 lines + `@AGENTS.md` + `agents/` + `CONTEXT.md` | Custom `oxlint` plugin (6 rules), `respectEslintDisableDirectives: false`, self-pruning allowlists, `nx affected` | 6 | 50 commits / **22 days** · 50% conv · 22% fix · 6% AI |
| **[`21st-dev/1code`](1code.md)** | 5.6k | **Archived** | Single-pkg Electron + React + tRPC + Drizzle (Bun) | 18-line stub + stale 274-line `CLAUDE.md` | None (only `tsgo --noEmit`, 0 workflows, 0 tests) | 0 | Archived Mar 2026 (< 2 mos public) · 24% conv · 22% AI |

## Key Patterns Across Direct Rivals

1. **The survival divide is mechanical discipline + scope restraint, not initial launch hype.**
   - `1code` (5.6k★) shipped fast with zero CI, zero tests, and a one-way `sync-to-public.sh` mirror — archived in 7 weeks.
   - `vibe-kanban` (28.8k★) had real systems craft (`ts-rs`, `sqlx`, `clippy -D warnings`), but sprawled into 30 Rust crates + ElectricSQL + WebRTC relay + Tauri + Rust nightly on a 4-person team — and had to sunset.
   - The three thriving control planes (`t3code`, `Paradev`, `emdash`) all converged on **TypeScript monorepos + custom lint rules encoding domain invariants + `@AGENTS.md` single-source agent instructions + ACP for structured providers**.

2. **Custom lint rules are the #1 weapon against agent-generated regressions.**
   - Every healthy team stopped relying on prose rules in `AGENTS.md` and encoded recurring failure modes into Biome or `oxlint` as `"error"`:
     - **Paradev:** bans sync subprocesses on serving loops, bans raw `@vercel/sandbox` handles, bans cross-tenant admin queries, bans `<Navigate>`.
     - **Emdash:** enforces module boundaries, sole-writer DB tables, `no-async-transaction-callback`, **disables `eslint-disable` comments (`respectEslintDisableDirectives: false`)**, and auto-prunes allowlists (`prune:boundary-allowlists`).
     - **T3 Code:** custom `oxlint-plugin-t3code` (no low-value comments, no unreasoned state sync, no UI primitive restyle) + `knip` + `evals/`.

3. **Zero-install & zero-friction dev environments matter hugely for parallel worktrees.**
   - Emdash's `devEngines.runtime` (`onFail: "download"`) eliminates Node/pnpm mismatch across worktrees.
   - Paradev's `paradev schema` JSON introspection and CDP port verification (`DESKTOP_VITE_PORT` check) make self-testing safe when 5+ worktrees run concurrently.
   - 1Code's local NDJSON log collector (`localhost:7799/log`) is a cheap, high-leverage debugging primitive worth adopting.

4. **T3 Code vs. Orca (the two heavyweight direct rivals in Chunk 1):**
   - **Orca (`137.8k★`, 50 commits / 3.2 hrs)** is the largest and fastest-moving direct rival on GitHub, leading the cohort on **performance-contract CI**, anti-test-slop discipline (`"Tests are the exception"` + zero-checkout `pr-test-loc.yml`), mandatory `## Performance` PR checks, custom `oxlint` perf/IME plugins (`quadratic-buffer-concat`, `ime-enter-guard`), hidden-window CDP/fixture UI checks, and Windows crash/update survival E2E — at the cost of `67` workflows and `9,918` open issues.
   - **T3 Code (`78.8k★`, 50 commits / 7.0 hrs)** stays leaner (`29` workflows, `3,681` open issues) and holds distinct moats in **model-facing `evals/`** and structured anti-slop contributor vouching (`VOUCHED.td`, `pr-limits.yml`, `contribution-triage`).
