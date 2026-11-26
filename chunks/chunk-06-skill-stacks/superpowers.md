# Superpowers (`obra/superpowers`)

- **Snapshot:** `326,498★` · `28,969` forks · `372` open issues · `MIT` · Active (created Oct 9, 2025; pushed 2026-11-24)
- **Primary Stack:** Composable Markdown skills + 319 KB Shell + 197 KB JS + 24 KB Python + 9 KB TS; zero runtime dependencies; ships native plugin manifests for **15+ harnesses** (Claude Code, Antigravity, Codex, Cursor, Devin, Factory Droid, Gemini CLI, Copilot CLI, Grok Build, Kimi Code, OpenCode, Pi, Hermes, Muse).
- **Data source:** [`data/chunk-06/obra__superpowers.json`](../../data/chunk-06/obra__superpowers.json)

## 1. Agent Instruction & Docs Hygiene
- **Most brutally candid anti-AI-slop `AGENTS.md` in the entire 36-repo study (121 lines / 9.9 KB):**
  - Opens directly with: **"This repo has a 94% PR rejection rate. Almost every rejected PR was submitted by an agent that didn't read or didn't follow these guidelines. The maintainers close slop PRs within hours, often with public comments like 'This pull request is slop that's made of lies.'"**
  - Reframed the agent's job cleanly: *"Your job is to protect your human partner from that outcome... That is being a tool of embarrassment."*
  - **Hard anti-slop PR rules:**
    1. Human-authored summary (<200 words) — *"if an agent writes it, the PR will be closed."*
    2. Mandatory disclosure of model, harness, harness version, all installed plugins, and the human's original prompt.
    3. **Bans fixing someone else's issue** unless a maintainer asked (*"An open issue in the tracker is not a request for a PR"*), bans spray-and-pray batch PRs, bans theoretical/review-agent-only fixes, and bans "compliance" rewrites to match Anthropic's skill docs without before/after eval evidence.
    4. All PRs must target `dev`, not `main`.
- **Behavioral acceptance test for new harness ports:** *"Open a clean session and send `'Let's make a react todo list'`. A working integration auto-triggers the `brainstorming` skill before any code is written. Without the `using-superpowers` bootstrap at session start, skills are dead weight."*

## 2. Mechanical Gates & Quality Control
- **Zero GitHub Actions workflows (`workflows: []`)** inside `obra/superpowers` itself (uses `.pre-commit-config.yaml` + local `tests/`).
- **Dedicated external real-CLI eval lab (`prime-radiant-inc/superpowers-evals`):** Treats skills as *executable code that shapes agent behavior*, running Quorum + a Gauntlet QA agent against real Claude Code, Codex, and Gemini CLIs with adversarial pressure testing across multiple sessions plus deterministic post-checks.
- **Compaction resilience & circuit breakers:** Recent releases (`v6.2.0` → `v7.0.2`) specifically hardened skills to **survive context compaction**, added a **5-round fix-loop circuit breaker** + rationalization tables, and ran compression sweeps to keep plans lean.

## 3. Architectural Bets & Craft
- **Zero-dependency, bootstrap-triggered methodology:** Forces agents out of eager coding into a structured loop: *Brainstorm (tease out spec in readable chunks) → Implementation Plan (red/green TDD, YAGNI, DRY) → Subagent-Driven Development (isolated tasks + review loops)*.
- **Cross-harness native packaging:** Maintains first-class plugin/extension directories for every major harness (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`, `.antigravity-plugin/`, `.opencode/`, `.pi/`, `.hermes-plugin/`, `.kimi-plugin/`, `.muse-plugin/`, `gemini-extension.json`) rather than relying on fragile `npx skills` copy shims.

## 4. Commit, PR & Maintenance Reality
- **Tight solo-curated release train:** **50 commits over 4 months** (`2026-07-05` to `2026-11-03`, `v6.2.0` → `v7.0.2`), **78% conventional**, **12% fix/revert**, **14% AI signal**.
- **`obra` (Jesse Vincent) authored 46 of the last 50 commits** (529 all-time; `arittr` 79). Despite **326.5k★** and **28,969 forks**, aggressive slop rejection keeps open issues to just **372**.

## 5. Steal vs. Avoid
- **Steal:**
  1. **"Skills are code, not prose" + adversarial pressure-test evals** before merging wording changes to prompts or skills.
  2. **Mandatory concrete acceptance test for integrations** (`"Let's make a react todo list"` must auto-trigger `brainstorming`).
  3. **Hard-edged anti-slop `AGENTS.md` framing** (*"protect your human partner from embarrassment"*, human-written <200-word summary, full model/harness/plugin disclosure, *"an open issue is not a request for a PR"*).
  4. **Designing skills to survive context compaction** + **5-round fix-loop circuit breakers** preventing infinite agent thrashing.
- **Avoid:**
  1. **Zero in-repo GitHub Actions CI** — even a tiny markdown/manifest/test check in CI catches broken plugin manifests across 15+ harness directories before release.
