# 1Code (`21st-dev/1code`)

- **Snapshot:** `5,565★` · `606` forks · `45` open issues · `Apache-2.0` · **Archived** (created 2026-01-14, last pushed 2026-03-06 — ~7 weeks of public life)
- **Primary Stack:** Single-package Electron + React 19 + TypeScript (5.1 MB TS), Bun, `electron-vite`, tRPC (`trpc-electron`), Drizzle + `better-sqlite3`, Jotai + Zustand + React Query, `@anthropic-ai/claude-agent-sdk`, `@zed-industries/codex-acp`.
- **Data source:** [`data/chunk-01/21st-dev__1code.json`](../../data/chunk-01/21st-dev__1code.json)

## 1. Agent Instruction & Docs Hygiene
- **Split & stale instructions:** Root `AGENTS.md` is just an 18-line OpenSpec boilerplate stub, while real instructions live in a 274-line `CLAUDE.md`. Worse, `CLAUDE.md`'s *"Current Status (WIP)"* section still says *"Planned: Git worktree per chat"* and *"Replacing mock-api.ts"* even though the README advertises 25 shipped features (worktrees, Kanban, cloud sandboxes, automations, voice, PWA). Classic drifting-docs failure mode.
- **Zero `docs/`, zero `.agents/skills/`:** All operational, debugging, and macOS notarization runbooks were dumped inline into `CLAUDE.md`.

## 2. Mechanical Gates & Quality Control
- **Virtually zero mechanical guardrails:**
  - **0 GitHub Actions workflows** (`.github/workflows/` does not exist in the public repo).
  - **No linter** (no Biome, oxlint, or ESLint config).
  - **No test script or test suite** in `package.json` — only `ts:check: tsgo --noEmit`.
  - **Two competing lockfiles committed** at root (`bun.lock` AND `bun.lockb`!).
  - **Hardcoded binary versions** downloaded manually during release (`claude:download --version=2.1.45`, `codex:download --version=0.98.0`).
- **One genuinely clever debugging pattern:** `CLAUDE.md` documents a lightweight local NDJSON debug log server (`localhost:7799/log` → `.debug/logs.ndjson`) so an agent can drop a zero-import `fetch('http://localhost:7799/log', ...).catch(()=>{})` probe into renderer or main code, have the user reproduce, read `.debug/logs.ndjson`, fix with evidence, and delete the probe.

## 3. Architectural Bets & Craft
- **Fast prototype stack that hit ceiling fast:** Single-package Electron app mixing **three** state systems at once (Jotai + Zustand + React Query) and **two** diff libraries (`@git-diff-view/react` + `@pierre/diffs`), plus Monaco, Mermaid, Xterm v5 + `@xterm/*` addons, and Motion.
- **Public mirror of a private repo:** `"sync:public": "./scripts/sync-to-public.sh"` reveals the public GitHub repo was a one-way snapshot mirror of a private monorepo, while `CONTRIBUTING.md` explicitly kept Sign-in/Sync, Background Agents, Auto-updates, and Automations closed-source behind `1code.dev`.

## 4. Commit, PR & Maintenance Reality
- **Single-author release dumps:** `serafimcloud` authored 66 of ~90 total commits; the last 20 commits before archival are almost all squashed `"Release v0.0.52"` … `"Release v0.0.72"` sync drops with zero atomic commit history.
- **Low discipline metrics:** 24% conventional commits, 22% explicit AI co-author trailers, archived after < 2 months.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Ephemeral local NDJSON debug log server (`localhost:7799/log`)** for agent-assisted UI/Electron runtime debugging — removes manual console copy-pasting during a hypothesis→reproduce→fix loop.
  2. **`tsgo --noEmit`** early adoption for fast typechecking.
- **Avoid:**
  1. **"Open-source launch hype" as a one-way mirror (`sync-to-public.sh`) with zero CI/tests/lint:** Attracts 5.5k stars in weeks, then collapses under maintenance debt or goes closed-source.
  2. **Leaving `Current Status (WIP)` sections in `CLAUDE.md`:** They rot within days and actively mislead coding agents about what exists in the codebase.
  3. **Stacking 3 frontend state libraries + 2 diff engines** in an un-linted prototype — makes every agent edit unpredictable.
