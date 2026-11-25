# Cline (`cline/cline`)

- **Snapshot:** `71,891★` · `7,962` forks · `1,833` open issues · `Apache-2.0` · Active (created Jul 2024; pushed 2026-11-23)
- **Primary Stack:** Bun workspaces TypeScript monorepo (32.7 MB TS + 143 KB Rust for Tauri v2 desktop shell), `@cline/{shared,llms,agents,core,sdk}`, CLI (`OpenTUI`), VS Code extension (gRPC/Protobuf + React webview), Tauri + Next.js + Bun sidecar desktop app, Biome, Vitest, Playwright, `evals/` (`cline-bench`).
- **Data source:** [`data/chunk-03/cline__cline.json`](../../data/chunk-03/cline__cline.json)

## 1. Agent Instruction & Docs Hygiene
- **Ultra-lean 34-line `AGENTS.md` (5.4 KB):** Skips generic coding advice completely and focuses purely on non-obvious environment/build traps (must run `bun run build:sdk` because exports point only to `dist/`; `DISPLAY=:1` virtual X display; `bun run protos` for `.proto` edits; known cloud-VM `git insteadOf` test failure; Rust `edition2024` >= 1.85 requirement).
- **Multi-agent compatibility:** Ships `.agents/skills/` (8 skills including `cline-sdk`, `opentui`, `tuistory`, `publish-*`), `.claude/{commands,hooks,skills}`, `.clinerules/`, `.codex/`, `.worktreeinclude`, and `.greptile/`.
- **Docs:** 26 top-level `docs/` entries (Mintlify `docs.json`) plus `evals/` with `ARCHITECTURE.md`, `benchmarks/`, `cline-bench`, `e2e/`, and `smoke-tests/`.

## 2. Mechanical Gates & Quality Control
- **Anti-spam repo hygiene bots:** Ships two clever community-defense workflows: `repo-delete-agent-promo-comments.yml` and `repo-strip-agent-badges.yml` to automatically scrub promotional AI agent footers/badges from PRs and comments.
- **Fast, isolated packaging tests (`desktop-test.yml`):** Tests macOS DMG background generation and Windows NSIS installer/uninstaller process cleanup using pinned `nsis-3.13.zip` (SHA1-verified) and a disposable fixture executable — without building the full Electron/Tauri app! Also notes a real CI quirk: `setup-bun` with `no-cache: true` on dependency-free Windows jobs prevents a cache-save post-step hang.
- **Cross-repo PR verification (`ext-jb-test-integration.yml`):** Auto-triggers private JetBrains plugin integration tests for team members and via `/test-jetbrains` for external PRs, explicitly sanitizing untrusted PR titles/branch names via `jq -n --arg` before building JSON payloads.
- **Brownfield lint debt in `biome.json`:** While `sdk/` and `apps/{cli,cline-hub}` run strict `biome check --diagnostic-level=error`, the legacy `apps/vscode/**` override downgrades ~30 rules (`useExhaustiveDependencies`, `useHookAtTopLevel`, `noAsyncPromiseExecutor`, `noExplicitAny`, `noDangerouslySetInnerHtml`) to `"info"` or `"off"`.
- **Heavy pre-commit hook (`lint-staged`):** Runs full `bun run types` on every staged commit in `sdk/**` or `apps/**`.

## 3. Architectural Bets & Craft
- **Successful multi-surface pivot:** Evolved from a single VS Code extension (`claude-dev`) into a shared `@cline/sdk` powering CLI, VS Code, JetBrains (closed-source plugin talking to OSS core), and a Tauri v2 + Bun sidecar desktop app (`@cline/code`).
- **Measured CI optimization:** Explicitly comments in `ext-vscode-test-e2e.yml` that they *removed* Bun install caching because restoring the cache took as long as installing fresh — evidence of empirical CI measurement rather than cargo-culting caches.
- **Security hygiene:** `.gitleaks.toml`, third-party license notices bundled across VSIX, CLI, and desktop, and security-conscious git invocation fixes (`fix: pass commit search terms to git as arguments, not shell text (#15378)`).

## 4. Commit, PR & Maintenance Reality
- **Steady mature cadence:** Last 50 commits span **19.5 days** (2026-11-04 to 2026-11-23), **86% conventional commits**, **32% fix/revert**, **6% explicit AI trailers**.
- **Healthy core team:** Founder `saoudrizwan` (2,880 commits) remains active alongside ~8 regular engineers (`abeatrix`, `mkondratek`, `BarreiroT`, `dominiccooney`, `johnwschoi`, `arafatkatze`).

## 5. Steal vs. Avoid
- **Steal:**
  1. **Trap-focused 34-line `AGENTS.md`** that lists only concrete build/env footguns instead of generic style lectures.
  2. **`repo-delete-agent-promo-comments.yml` / `repo-strip-agent-badges.yml`** to keep public PR threads free of tool-spam footers.
  3. **Lightweight installer/packaging unit tests** (`desktop-test.yml`) verifying NSIS/DMG behavior on fixture binaries without waiting for full release builds.
  4. **Explicit `jq -n --arg` sanitization** when forwarding PR metadata in `pull_request_target` / `issue_comment` dispatches.
- **Avoid:**
  1. **Leaving legacy packages (`apps/vscode/**`) on `"info"`/`"off"` for correctness & security lint rules** (`useHookAtTopLevel`, `noDangerouslySetInnerHtml`, `noAsyncPromiseExecutor`) — freezes technical debt in place.
  2. **Compiled-only workspace `dist/` exports without dev conditions** — forces every agent to remember `bun run build:sdk` before testing downstream packages.
