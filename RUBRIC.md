# Assessment Rubric

Every repository in this study is evaluated against the same **5 axes** using primary-source GitHub data collected by `scripts/collect_chunk.py` (snapshot date: November 2026).

## 1. Agent Instruction & Docs Hygiene
- Presence, size (lines / bytes), and structure of `AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `.claude/`, `.cursor/rules/`.
- Progressive disclosure vs. bloated mega-prompts.
- Docs discipline: architecture/invariants docs vs. drifting feature catalogs or stale plans.

## 2. Mechanical Gates & Quality Control
- Linters, formatters, dead-code detectors (`oxlint`, `biome`, `eslint`, `knip`, `clippy`, `golangci-lint`), and strictness.
- CI workflows (`.github/workflows/`): fast branch-scoped checks, PR-size / slop moderation, security scanning, release automation.
- Testing & evals: unit/integration/e2e coverage, model-facing eval suites, bug-proof discipline.

## 3. Architectural Bets & Craft
- Stack & packaging choices (monorepo vs. single binary, Electron vs. Tauri vs. native Swift/Rust, server/client separation).
- Concurrency & isolation model (git worktrees, containers/sandboxes, PTY/tmux, RPC/event sourcing).
- Complexity budget: where complexity lives (adapter boundary vs. leaked into core/UI).

## 4. Commit, PR & Maintenance Reality
- Recent commit cadence, conventional commits usage, and fix/revert churn ratio.
- Explicit AI co-authorship / agent-authored commit signal (`Co-Authored-By`, bot commits, PR velocity).
- Maintainer concentration (bus factor vs. community scaling) and lifecycle health (active vs. archived / sunsetted).

## 5. Steal vs. Avoid (Transferable Takeaways)
- **Steal:** Concrete patterns, scripts, configs, or architectural ideas directly transferable to our own repos.
- **Avoid:** Visible failure modes, complexity traps, or maintenance burdens exposed in the repo's history.

---

## T3 Code (`pingdotgg/t3code`) Baseline Reference
- **Scale:** ~78.8k★, TypeScript monorepo (Effect-TS server, React/Vite web, Electron desktop, React Native mobile, shared `contracts` + `client-runtime`).
- **Agent hygiene:** Compact root `AGENTS.md` with pointer table to `docs/internals/00..17`, explicit "no drifting docs" rule, `.agents/skills/` for procedural playbooks.
- **Mechanical gates:** Custom lint rules (`oxlint` + custom plugins for comments, state sync, UI restyle), `vp run check:changed` for fast branch-scoped verification, `evals/` for model-facing text, PR contribution triage skill.
- **Architecture:** Event-sourced orchestration (`Orchestrator → EventSink → EffectWorker`), provider complexity isolated at adapter boundary, single-origin dev/remote WebSocket architecture.
