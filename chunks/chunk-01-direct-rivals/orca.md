# Orca (`stablyai/orca`)

- **Snapshot:** `137,847★` · `8,828` forks · `9,918` open issues · `MIT` · Active (created Mar 17, 2026; pushed `2026-11-25T21:36:35Z`) · YC-backed (`https://orca.dev`)
- **Primary Stack:** **143.7 MB TypeScript** (`electron-vite`, `vite.web.config.ts`, `mobile/` iOS/Android, `native/` Windows addons & journal file lock, `cloud/`, Ghostty/xterm terminal, `orcad` daemon, `pnpm` global virtual store, `oxlint` + `oxfmt`, Vitest, Playwright CDP); BYOS fleet runner for Claude Code, Codex, Grok, Agy, OpenCode, Pi, and Hermes.
- **Data source:** [`data/chunk-01/stablyai__orca.json`](../../data/chunk-01/stablyai__orca.json)

## 1. Agent Instruction & Docs Hygiene
- **High-signal, operational `AGENTS.md` backed by `docs/agents-md-refs/` progressive disclosure:**
  - Opens directly with **`# Checks`** and a **cached `pnpm check:changed`** rule: *"A pass is cached, so don't rerun it 'to be sure', and don't also run `pnpm tc`, `pnpm lint`, or the full suite. Never `--no-verify`."*
  - Explicitly forbids backgrounding checks and polling with `sleep`: *"Run checks in the foreground with `timeout 900`."* For CI, mandates `gh pr checks --watch` / `gh run watch --compact --exit-status` and `grep -nE "error|FAIL|✗"` on long logs.
  - **Standout anti-test-slop policy (`"Tests are the exception."`):** Flips the usual AI over-testing default on its head: *"Prove a change by running it (app via CDP screenshot, CLI, script), not by committing a test. Commit one only for logic where a silent regression is costly: parsers/codecs/round-trips, security boundaries, persistence/migrations/data loss, concurrency or state-machine invariants, cross-platform paths... Never test UI behavior ('button does X'), wiring/IPC glue, mock calls, copy, constants, or timing. Delete low-value tests you touch instead of updating them."* Backed by `docs/agents-md-refs/test-antipatterns.md`.
  - **Anti-dumping-ground naming rule:** Explicitly bans `helpers`, `utils`, `common`, `misc`, and `shared-stuff` for files/folders, forcing domain-specific names (`tab-group-state.ts`, `terminal-orphan-cleanup.ts`).
  - **Hidden-window Electron validation:** Mandates `ORCA_BACKGROUND_LAUNCH=1`, bans `show()`/`showInactive()`/`bringToFront()`/`app.focus()` so agents never steal the developer's monitor focus, uses CDP screenshots of hidden renderers, and offers `pnpm fixtures:shot <id>` to screenshot presentational components *without launching Electron*.
  - **Design-system guard:** Points all UI work to `docs/STYLEGUIDE.md`, `src/renderer/src/assets/main.css`, and `src/renderer/src/components/ui/`.

## 2. Mechanical Gates & Quality Control
One of the deepest **performance-first static analysis & CI verification** rigs in the entire 35-repo study:
- **5 surgical custom `oxlint` plugins (`config/oxlint-plugins/`):**
  - `anti-slop-prefilter.mjs`
  - `app-store-performance.mjs`
  - `ime-enter-guard.mjs` (prevents CJK/IME composition Enter-key send bugs!)
  - `quadratic-buffer-concat.mjs` (catches O(n²) buffer concatenation in streaming/terminal hot paths!)
  - `renderer-scrollbar-style.mjs`
- **Strict `.oxlintrc.json` + lazy-load bundle guards:**
  - Enables `react/no-deriving-state-in-effects: "error"`, `react/set-state-in-render: "error"`, `typescript/no-explicit-any: "error"`, and `typescript/switch-exhaustiveness-check: ["error", { allowDefaultCaseForExhaustiveSwitch: false }]`.
  - Uses `no-restricted-imports` to ban value-importing `@linear/sdk` (*"hoists its ~2.6MB CJS bundle into the eager top-level require block and defeats the lazy loader. Use `import type` plus `loadLinearSdk()`"*).
- **Main-process blocking-work ratchets (`main-blocking-work.yml`):**
  - Runs `run-main-blocking-ratchets.mjs` + `check-main-sync-spawn-ratchet.mjs` over the full tree on every push to `main` so Electron main-process blocking calls and sync spawns cannot regress.
- **Cross-OS performance & survival CI (`67` workflows):**
  - `performance-contracts.yml`: Runs `*.performance.test.*` contracts across Linux, macOS, and Windows.
  - `pr-test-loc.yml` (on `ubuntu-slim`, **zero repo checkout**, fetching trusted scripts from `default_branch` via `gh api`!): Computes a **test LoC vs. non-test LoC breakdown** on PRs and posts a PR comment when the token has write access (gracefully skipping the write on read-only fork 403s so untrusted fork code never gets `pull-requests: write`).
  - `pr-description.yml`: Sparsely checks out `.github/scripts/check-pr-performance-section.mjs` and enforces that every PR body fills out a mandatory **`## Performance`** section (`"None, because ..."` or concrete measurements).
  - `unit-selection-evidence.yml`: Runs diff-based unit test selection in **shadow mode** alongside the full 24-shard unit test suite and compares recall against full results to empirically prove safety before trusting selective test runs.
  - Native Windows/OS survival suites: `win-crash-survival-e2e.yml`, `win-update-survival-e2e.yml`, `win-orcad-serve-switch-e2e.yml`, `windows-wsl-e2e.yml`, `linux-wayland-gpu-sandbox.yml`, and 3-OS `journal-file-lock.yml`.
- **Supply-chain & dependency hygiene (`pnpm-workspace.yaml`):**
  - `minimumReleaseAge: 4320` (3-day npm cooldown), explicit `allowBuilds` with inline comments justifying every `true`/`false`, `supportedArchitectures: current` for fast local dev, and **`ignoredOptionalDependencies`** excluding all 8 platform `@anthropic-ai/claude-agent-sdk-*` (~95 MB/platform) bundled CLIs so the user's own CLI override stays mandatory.
  - Repo root allowlist discipline (`pnpmfile: config/pnpmfile.cjs` — *"under `config/` because the repo root only admits allowlisted entries"*).

## 3. Architecture & Runtime Boundaries
- **Largest direct T3 Code rival on GitHub (`137.8k★` vs. `t3code`'s `78.8k★`):** Full multi-surface ADE — Electron desktop (`electron-vite`), web client (`vite.web.config.ts`), native mobile (`mobile/`, releasing `android-v0.0.71` alongside desktop `v1.4.274`), remote daemon (`orcad`), cloud runtime (`cloud/`), native OS addons (`native/windows-*`, `native/journal-file-lock`), and declarative plugin/ACP codegen (`generate:acp-protocol`, `verify:rpc-params-catalog`).
- **PR template (`pull_request_template.md`) enforces 7 disciplined checks:** `ELI5`, `What Changed`, `Why`, `Linked Issue` (*"outside contributor PR without an issue will be ignored"*), `Visual Proof` (before/after tabs, **never committed to git**), `Performance` (CI-enforced), `Risk` (`Low/Medium/High` + revertability), and external-only `AI Disclosure`.

## 4. Velocity, Governance & Scale Stress Signals
- **Blistering velocity — 2nd fastest in the entire 35-repo study:** **50 commits in 3.2 hours** (`2026-11-25 18:17Z` → `21:28Z`), nearly **49,300 PRs/issues in 8 months** (`#49277`), `88%` conventional commits, strong multi-maintainer team (`nwparker` 8,257; `brennanb2025` 3,619; `OrcaWin` 3,085; `AmethystLiang` 2,660; `Jinwoo-H` 2,647; `AmoabaKelvin` 1,553; plus `orca-remote-automation[bot]` shipping UI polish PRs).
- **Real scale stress signals to watch:**
  - **9,918 open issues** — 3rd highest in the 35-repo study (behind only `codex` at 28,619 and `cmux` at 11,218, and slightly above `openclaw`'s 9,182), even with the `Fixes #` outside-contributor gate.
  - **70% fix/revert commits** in the last 50 (heavy continuous bug-burn across i18n, Windows clipboard/WSL, mobile cards, and connectors at 3.2-hr/50-commit velocity).
  - **67 workflows** — above the 8–30 CI Goldilocks zone, with 6 dedicated CI cache-warmup/sweep/runner-demand workflows (`ci-cache-warmup*`, `ci-runner-demand.yml`, `ci-branch-cache-sweep.yml`) needed to keep 24-shard unit tests + 3-OS E2E fast.

## 5. Stealable Patterns vs. Anti-Patterns
- **Steal immediately:**
  1. **`"Tests are the exception"` + `pr-test-loc.yml` (zero-checkout `ubuntu-slim` default-branch script):** Stops AI agents from flooding repos with brittle mock/UI unit tests while keeping PR reviewers informed of test-vs-prod LoC ratios safely.
  2. **Mandatory `## Performance` PR section (`pr-description.yml`) + `quadratic-buffer-concat` / `ime-enter-guard` `oxlint` plugins + `no-restricted-imports` for heavy lazy-loaded SDKs.**
  3. **Cached `pnpm check:changed` + hidden-window `ORCA_BACKGROUND_LAUNCH=1` + `pnpm fixtures:shot <id>`** (UI verification without stealing developer focus or booting Electron).
  4. **Shadow-mode diff test selection (`unit-selection-evidence.yml`)** to measure recall empirically before trusting selective CI.
  5. **`ignoredOptionalDependencies` + commented `allowBuilds`** in `pnpm-workspace.yaml` to strip ~95 MB/platform unused SDK CLIs.
- **Watch out for:**
  - At **50 commits / 3.2 hrs** across Desktop + Mobile + Windows native + Cloud, `67` workflows and `9,918` open issues require a full multi-engineer core team and dedicated CI cache/runner maintenance to stay upright.
