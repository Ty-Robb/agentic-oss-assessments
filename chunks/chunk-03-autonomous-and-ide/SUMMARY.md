# Chunk 3 Summary — Mature Autonomous & IDE-Native Heavyweights

*Snapshot date: 2026-11-25. Combined stars in this chunk: **247,409★**.*

## Side-by-Side Matrix

| Repo | Stars | Status | Open Issues | Primary Stack | `AGENTS.md` / Skills | Signature Mechanical Gate | CI Workflows | Last-50 Velocity & Hygiene |
| --- | ---: | --- | ---: | --- | --- | --- | ---: | --- |
| **[`cline/cline`](cline.md)** | 71.9k | Active | 1,833 | TS (Bun, SDK + CLI/OpenTUI + VS Code gRPC + Tauri desktop) | 34-line trap-only `AGENTS.md` + 8 `.agents/skills/` | `repo-delete-agent-promo-comments`, `repo-strip-agent-badges`, fixture-only DMG/NSIS installer tests, `cline-bench` | 17 | 50 commits / **19.5 days** · 86% conv · 32% fix · 6% AI |
| **[`RooCodeInc/Roo-Code`](roo-code.md)** | 24.2k | **Archived** (May 2026) | 1,025 | TS (pnpm, Turbo, VS Code ext + React webview) | 5-line single-invariant `AGENTS.md` + `.roomodes` | `knip --include files`, CodeQL, `ellipsis.yaml` | 7 | Archived May 15, 2026 · 34% conv · 10% AI |
| **[`OpenHands/OpenHands`](openhands.md)** | 94.3k | Active | 1,252 | TS (React 19, Vite 8, Electron Agent Canvas) + external Python SDK | 133-line `AGENTS.md` + 10 `.agents/skills/` + repo ownership table | **`verify-skill-isolation.yml`**, **Stryker diff mutation testing**, `HUMAN:` PR check, 7-day `--min-release-age=7`, mock-LLM Playwright E2E | 25 | 50 commits / **2.0 days** · 100% conv · 36% fix · 26% bot/AI |
| **[`aaif-goose/goose`](goose.md)** | 57.0k | Active (AAIF) | **512** | Rust (`oi-kit` + ACP + `rmcp` + `candle` + `iroh`) + Electron UI | 132-line `AGENTS.md` + `@AGENTS.md` `CLAUDE.md` | `Ready`-board issue gate, `check-lean-size`, `wasm32` check, `cargo-machete`, `git cherry` release-branch gate, MCP/toolcall conformance | 39 | 50 commits / **5.0 days** · 94% conv · 16% fix · 58% Dependabot |

## Key Patterns Across Chunk 3

1. **Every surviving IDE/autonomous pioneer pivoted into a multi-surface SDK + ACP/control-plane platform.**
   - `Cline` grew from a VS Code extension into `@cline/sdk` + CLI + Tauri desktop.
   - `OpenHands` split its Python SDK out and turned its main repo into **Agent Canvas** — an ACP-compatible control center directly competing with T3 Code and Paradev.
   - `Goose` extracted `oi-kit` (Rust/Wasm/Python/Kotlin SDK) and made its Electron desktop speak **ACP** to its own backend.
   - `Roo Code` stayed centered on a forked VS Code extension and shut down in May 2026.

2. **OpenHands introduced two of the strongest anti-hallucination quality gates in this entire study:**
   - **Verification Skill Independence (`verify-skill-isolation.yml`):** Mechanically prevents an implementor PR from modifying its own verification specs/skills — eliminating the classic agent shortcut of weakening a test to turn CI green.
   - **Diff-scoped Mutation Testing (`stryker-diff.mjs`):** Verifies that newly added tests actually kill mutants across changed production TypeScript files (`git diff --name-only`) rather than merely boosting line coverage.

3. **Governance has matured beyond "please write good PRs":**
   - **OpenHands** enforces a human-only `HUMAN:` section in PR descriptions (`pr-description-check.yml`) and locks the `ready-for-dev` label to maintainers (`issue-readiness-check.yml`).
   - **Goose** gates external PRs on `Ready` status on its public design board and requires 1-line dispositions for every AI code-review comment.
   - **Cline** automatically strips promotional AI agent footers/badges from PRs and comments.
