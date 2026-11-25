# OpenCode (`anomalyco/opencode`)

- **Snapshot:** `229,098★` · `31,187` forks · `4,172` open issues · `MIT` · Active (default branch `dev`; pushed 2026-11-25)
- **Primary Stack:** TypeScript monorepo (63.2 MB TS + 11.8 MB Rust process daemon), Bun + Turborepo, Effect-TS v4.1, SolidJS + OpenTUI, Electron desktop, Drizzle SQLite, Hono, Nix flake.
- **Data source:** [`data/chunk-02/anomalyco__opencode.json`](../../data/chunk-02/anomalyco__opencode.json)

## 1. Agent Instruction & Docs Hygiene
- **High-signal, opinionated `AGENTS.md` (221 lines / 18.2 KB):** Packs dense architectural invariants (dependency DAG: `Schema → Core/Protocol → Server`, event-sourced `Session Core` inbox admission, async non-blocking plugin loading, experimental API graduation, feature-flag deletion) plus a strict TypeScript style guide tailored to stop LLM bloat (no speculative defensive checks, no single-use helpers, no `import *`, no `else`, inline single-use bindings).
- **Guard against accidental root test runs:** `"test": "echo 'do not run tests from root' && exit 1"` — forces agents to run package-scoped tests and consult `.opencode/skills/{unit-tests,tui-tests,app-e2e-tests,component-tests}`.
- **TUI Storybook for agents:** Fixture-driven TUI stories run via `OPENCODE_STORY=<id> bun run dev:live` with keybindings in `StoryFooter` so agents can inspect real components safely.
- **Live-window CDP pitfall documented:** Explicitly requires `chromium.connectOverCDP(endpoint, { noDefaults: true })` because Playwright otherwise flashes the user's live desktop window into light mode.

## 2. Mechanical Gates & Quality Control
- **Purpose-built `anti-slop` + `anti-slop-effect` `oxlint` plugins + tested `ast-grep` rules:**
  - `.oxlintrc.json` loads `./script/oxlint/anti-slop/index.ts` and `./script/oxlint/anti-slop/effect/index.ts` with 24 custom rules targeting exact LLM bad habits: `no-chained-type-assertions`, `no-widen-then-assert`, `no-known-value-widening`, `no-shape-in-symbol-names`, `no-module-mocking`, `no-runtime-typeof`, `no-unsafe-dictionary-type`, `require-safety-comment-for-type-assertion`, `no-manual-effect-error-tag`, `prefer-effect-match`.
  - Uses `ast-grep` for Effect pattern simplification, GUI plugin boundaries, and dialog sizes — with dedicated unit tests for the lint rules themselves (`test:lint-rules`, `test:effect-simplification-rules`)!
  - Bans raw `fetch` and `HttpClient` in `packages/ai/src/**` so every HTTP request goes through `RequestExecutor` middleware; bans `createEffect`/`createRenderEffect`/`createComputed` in GUI plugins in favor of SDK primitives (`createKeyed`, `createLatest`, `createVisitState`).
- **7 automated PR/issue triage workflows:** `triage-slop.yml`, `triage-pr-standards.yml`, `triage-contributor.yml`, `triage-compliance-close.yml`, `triage-close-issues.yml`, `triage-close-linked.yml`, `triage-close-prs.yml`.
- **Bot blast-radius containment (`check-bot-scope.yml`):** Auto-merged bot branches (`bot/nix-hashes`) are mechanically verified to touch *only* `nix/hashes.json` and pass a validator from the base branch.
- **Rust Miri verification (`check-process-daemon.yml`):** Runs **both Stacked Borrows and Tree Borrows** under Miri on the Rust process daemon, plus Zig/Ghostty cross-compilation tests on Linux, macOS, and Windows ARM64.
- **Dual typecheck strategy:** Local `bun typecheck` uses fast `bun check`; CI uses official `@typescript/native` (`tsc -b`) via Turborepo `transit` hashes.

## 3. Architectural Bets & Craft
- **Event-sourced Session Core + durable inbox:** Separates prompt admission (`session.inbox.enqueued` → `session_inbox`) from model execution (`SessionExecution.wake`), making ID reuse idempotent and projections minimal.
- **Async non-blocking plugins by contract:** Server handlers never await plugin activation or retry; they return current state while long-lived clients react to `*.updated` events — eliminating startup deadlocks.
- **Feature-flag lifecycle:** New user-visible or risky changes land behind `packages/schema/src/config/flag.ts` (default on in dev, off in release) and ship by *deleting* the flag.
- **Generated SDK aliases on breaking moves:** `compile(..., { aliases: true })` preserves `@deprecated` aliases for one minor automatically.

## 4. Commit, PR & Maintenance Reality
- **Extreme shipping velocity:** Last 50 commits landed in **12.3 hours** (PR `#66,370`), **100% conventional commits**, **60% fix/revert**, **4% explicit AI co-author trailers** — yet **`opencode-agent[bot]` is the #3 all-time contributor (2,766 commits!)** alongside `thdxr` (3,093), `rekram1-node` (2,894), `kitlangton` (2,497), and `adamdotdevin` (2,208).
- **Massive open-source gravity:** 229k stars, 31k forks, 4,172 open issues, 22 translated `README.*.md` files.

## 5. Steal vs. Avoid
- **Steal:**
  1. **`anti-slop` custom oxlint plugin + tested `ast-grep` rules** encoding recurring LLM TypeScript mistakes (`no-widen-then-assert`, `no-runtime-typeof`, `no-module-mocking`, `require-safety-comment-for-type-assertion`).
  2. **Blocking root `test` (`do-not-run-tests-from-root`)** + `lint:changed` so agents iterate at package scope instead of burning minutes on full monorepo runs.
  3. **`check-bot-scope.yml`** path-pinning any auto-merged bot branch to its exact allowed file(s).
  4. **Explicit "validate once at trust boundary" + "ship by deleting the feature flag"** policies in `AGENTS.md`.
  5. **Turborepo `transit` virtual dependency task** so source-exported packages invalidate dependents' caches without requiring full build steps before tests.
- **Avoid:**
  1. **Keeping all `anti-slop` rules at `"warn"` and turning off all built-in oxlint categories (`correctness: "off"`)** — warnings erode over time unless promoted to `"error"` or checked on changed files only.
  2. **22 manually mirrored root `README.*.md` files** polluting the repo root.
