# Emdash (`generalaction/emdash`)

- **Snapshot:** `6,306★` · `676` forks · `92` open issues · `Apache-2.0` · Active (YC W26; pushed 2026-11-23)
- **Primary Stack:** TypeScript pnpm + Nx monorepo (21.2 MB TS), Electron desktop (`apps/emdash-desktop`) + remote `apps/workspace-server`, Drizzle + SQLite, custom typed `Wire` RPC protocol, MobX stores, `oxlint` + `oxfmt`, Vitest + Playwright browser tests.
- **Data source:** [`data/chunk-01/generalaction__emdash.json`](../../data/chunk-01/generalaction__emdash.json)

## 1. Agent Instruction & Docs Hygiene
- **Rich topic hierarchy, heavy root file:** Root `AGENTS.md` is **419 lines / 24.5 KB** (largest in Chunk 1 — ~50% longer than Paradev's and 2.6× T3 Code's line count), though `CLAUDE.md` cleanly delegates via `@AGENTS.md`. Also maintains a dedicated `agents/` folder (including `agents/workflows/flows.md`, `agents/risky-areas/`) and `CONTEXT.md`.
- **Clean ADR-only `docs/`:** `docs/` contains only `adr/` (Architecture Decision Records), keeping prose docs disciplined while putting agent guidance in `agents/`.
- **Noticeable duplication risk:** `CONTRIBUTING.md` (453 lines / 14.7 KB) repeats much of `AGENTS.md`'s layout and command catalog.

## 2. Mechanical Gates & Quality Control
- **Standout custom `oxlint` architecture plugin (`./tooling/oxlint/index.js`):** Enables `typeAware: true`, `correctness: "error"`, `respectEslintDisableDirectives: false`, and 6 custom repo rules enforced as `"error"`:
  - `emdash/core-host-boundaries` & `emdash/core-module-boundaries`
  - `emdash/no-async-transaction-callback` (prevents subtle SQLite transaction corruption!)
  - `emdash/no-dynamic-imports` & `emdash/no-tsx-in-api` & `emdash/no-tooling-imports`
- **Allowlist lifecycle automation:** Ships both `check-allowlists.mjs` (in `lint`) AND `prune:boundary-allowlists` so stale lint exceptions are actively reaped as code improves!
- **Sole-writer DB enforcement in `.oxlintrc.json`:** `no-restricted-imports` forbids importing Drizzle's `workspaces` or `conversations` tables anywhere outside their respective Registry modules; also forbids importing `electron` outside `main/{host,gateway,bootstrap,core,db}`.
- **Smart, fast CI (`code-consistency-check.yml`):**
  - Uses `pnpm nx affected -t <format:check|lint|typecheck|test>` with `pnpm install --frozen-lockfile --ignore-scripts` and retry logic.
  - Solves the native-module CI headache cleanly: keeps `--ignore-scripts` for lint/typecheck/format, and for `test` only installs an anchored native side-project (`apps/emdash-desktop/tooling/node-deps`) + rebuilds `node-pty`.
  - Dedicated `workspace-server-package-check.yml` verifies Linux x64 and Apple Silicon macOS packaging/installers on PRs touching server packages.
- **One soft spot:** `typescript/no-floating-promises`, `no-misused-promises`, and `await-thenable` are still `"warn"` (not `"error"`), and Playwright browser tests are skipped in CI.

## 3. Architectural Bets & Craft
- **Disciplined vertical-slice + Wire architecture:** Features live under `src/core/features/<feature>/{api,node,browser,contributions}` and register through central manifests (`controllers.ts`, `browser-contributions.ts`, `task-tab-contributions.ts`, `command-catalog.ts`). Preload exposes only two primitives (`requestWirePort`, `getPathForFile`), keeping Electron IPC razor-thin.
- **Zero-prerequisite toolchain provisioning:** `package.json` uses pnpm's `devEngines.runtime` (`node 24.14.0`, `onFail: "download"`) + `packageManager: pnpm@10.28.2`, so any contributor with `pnpm` gets the exact checksummed Node & pnpm automatically — zero nvm/corepack friction.
- **True local-first + SSH remote model:** Local SQLite + SSH/SFTP + standalone `workspace-server` avoids Paradev's cloud SaaS complexity while supporting macOS, Windows, and Linux (including Azure Trusted Signing for Windows and Apple notarization).
- **Dual runtime path (PTY + ACP):** Legacy TUI agents run over PTY while structured chat runs over ACP in a dedicated Wire worker — cleanly isolating provider chaos.
- **Expected failures modeled with `Result<T, E>`** from `@emdash/shared` (lightweight alternative to Effect-TS).

## 4. Commit, PR & Maintenance Reality
- **Steady core team:** Last 50 commits span **22 days** (2026-11-01 to 2026-11-23), driven by ~5 core engineers (`jschwxrz` 2,863, `arnestrickmann` 2,758, `Davidknp` 2,209, `janburzinski` 1,123, `rabanspiegel` 785). Very healthy open-issue count (`92`).
- **Merge-commit history:** Uses GitHub merge commits (`Merge pull request #...`), which drops top-level conventional-commit ratio to 50% (actual feature commits inside PRs follow Conventional Commits). Low fix/revert ratio (`22%`) and low explicit AI trailer rate (`6%`), though branch names like `generalaction/codex/classic-readme` show active agent usage.
- **Commercial positioning shift:** Recent commits (`docs(readme): introduce Emdash Classic`) show the OSS desktop app being branded "Emdash Classic" alongside a hosted team product at `emdash.com`.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Sole-writer database table lint rules** (`no-restricted-imports` restricting raw Drizzle table imports to one Registry module) + `no-async-transaction-callback`.
  2. **Self-pruning boundary allowlists** (`check-allowlists.mjs` + `prune:boundary-allowlists`) + `respectEslintDisableDirectives: false` in `.oxlintrc.json` so agents cannot silently silence lint rules with `// eslint-disable`!
  3. **Zero-setup `devEngines.runtime` (`onFail: "download"`)** in `package.json` to eliminate contributor/agent Node-version drift.
  4. **`--ignore-scripts` CI installs** with isolated native test-only side projects — huge CI speed & reliability win for Electron/SQLite/PTY repos.
  5. **`agents/risky-areas/`** targeted pre-edit checklists for high-blast-radius subsystems (DB, PTY, SSH, updater).
- **Avoid:**
  1. **Letting root `AGENTS.md` (419 lines) and `CONTRIBUTING.md` (453 lines) grow redundant** — wastes agent context on every session and risks contradicting each other.
  2. **Leaving `no-floating-promises` at `"warn"`** in an async-heavy Electron/IPC app.
