# Roo Code (`RooCodeInc/Roo-Code`)

- **Snapshot:** `24,234★` · `3,449` forks · `1,025` open issues · `Apache-2.0` · **Archived** (created Oct 2024; extension shut down & repo archived May 15, 2026)
- **Primary Stack:** TypeScript pnpm + Turborepo monorepo (10.9 MB TS), VS Code extension + React webview, ESLint 9 + Prettier, `knip` (`knip --include files`), Changesets, Renovate, Ellipsis AI reviewer (`ellipsis.yaml`).
- **Data source:** [`data/chunk-03/RooCodeInc__Roo-Code.json`](../../data/chunk-03/RooCodeInc__Roo-Code.json)

## 1. Agent Instruction & Docs Hygiene
- **Minimal single-invariant `AGENTS.md` (5 lines / 445 bytes):** Contains literally one high-signal rule — `SettingsView` inputs must bind to local `cachedState`, never live `useExtensionState()`, to avoid save race conditions. Instead of a big `AGENTS.md`, Roo used its own `.roo/` and `.roomodes` config.
- **Clean shutdown hygiene:** Before archiving on May 15, 2026, maintainers stripped cloud, telemetry, MDM, MCP marketplace, and dead corporate links (`#12323`–`#12375`) and pointed users in README to both the community fork (`ZooCode`) and upstream (`Cline`) — an unusually responsible OSS sunset.
- **Minor clutter:** Left a root `progress.txt` and messy `pnpm-workspace.yaml` comments (`- "src" # Should be apps/vscode`) reflecting its fast fork origins.

## 2. Mechanical Gates & Quality Control
- **Good baseline tooling for an IDE extension:** Turborepo with `--log-order grouped --output-logs new-only`, CodeQL (`codeql.yml`), `knip --include files` dead-file detection, `.git-blame-ignore-revs`, Renovate, and `ellipsis.yaml` automated PR review.
- **Only 7 workflows** — lean CI (`code-qa.yml`, `codeql.yml`, release/marketplace/nightly pipelines), though `packages/evals` was removed during the pre-shutdown strip (`#12328`).

## 3. Architectural Bets & Craft
- **Pioneered "Custom Modes" (`.roomodes`):** Roo Code's biggest lasting contribution to the entire agentic ecosystem was formalizing role-scoped agent modes (`Code`, `Architect`, `Ask`, `Debug`, `Custom`) with per-mode tool restrictions and instructions.
- **Strategic cautionary tale (the fork squeeze):** Forked from Cline (`saoudrizwan` is still #2 all-time contributor with 962 commits), gained 24k stars and shipped 3.54 releases, then pivoted toward cloud/remote agents (`roomote.dev`) and shut down the VS Code extension when standalone CLI/control-plane agents (Claude Code, Codex, OpenCode, T3 Code) eroded IDE-extension differentiation.

## 4. Commit, PR & Maintenance Reality
- **Final 50 commits (Mar–May 2026):** 34% conventional commits, 10% AI co-author, driven by `mrubens` (2,068 commits), `cte` (716), `daniel-lxs` (444), `hannesrudolph` (352), plus `roomote-v0[bot]` and `R00-B0T`.
- **1,025 open issues** left at archive time.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Bug-driven micro-invariants in `AGENTS.md`:** Even a 1-bullet rule documenting a non-obvious state-buffering trap (`cachedState` vs. live state) prevents repeat regressions.
  2. **`knip --include files`** as a low-noise first step toward dead-code enforcement + `.git-blame-ignore-revs` for formatting migrations.
  3. **Graceful sunset commits:** Stripping telemetry/cloud/MDM and linking successors before archiving is the gold standard if you ever retire an OSS project.
- **Avoid:**
  1. **Competing purely as a feature fork of a fast-moving upstream IDE extension** without owning an orthogonal distribution/runtime layer (SDK/CLI/control plane).
  2. **Deferring workspace directory hygiene** (`src` and `webview-ui` at root with `# Should be apps/vscode` comments forever).
