# Gemini CLI (`google-gemini/gemini-cli`)

- **Snapshot:** `109,097★` · `15,003` forks · `751` open issues · `Apache-2.0` · Active enterprise maintenance (consumer/Gemini 4+ transitioned to Antigravity CLI in June 2026; pushed 2026-11-25)
- **Primary Stack:** TypeScript npm workspaces monorepo (23.3 MB TS), Node >= 20, Ink TUI, esbuild + Node SEA (Single Executable Application), ESLint (`--max-warnings 0`) + Prettier, Vitest, Docker/Podman sandboxes, OpenTelemetry.
- **Data source:** [`data/chunk-02/google-gemini__gemini-cli.json`](../../data/chunk-02/google-gemini__gemini-cli.json)

## 1. Agent Instruction & Docs Hygiene
- **Tool-specific instruction file (`GEMINI.md`):** Uses `GEMINI.md` + `.gemini/` + `.geminiignore` rather than the cross-agent `AGENTS.md` convention.
- **Heavy enterprise `CONTRIBUTING.md` (571 lines / 20.4 KB):** Documents Google CLA, `/assign` self-assignment (max 3 issues on `help-wanted`), mandatory issue linking (auto-closes unlinked PRs), and a dedicated local AI PR review script (`./scripts/review.sh <PR_NUMBER>`) that spins up an isolated worktree to review PRs before human maintainers look.
- **Generated & verified docs:** `docs:settings -- --check`, `docs:keybindings`, `docs-audit.yml`, and `lychee` broken-link CI checks keep 25 top-level `docs/` sections mechanically honest.

## 2. Mechanical Gates & Quality Control
- **Best-in-class behavioral eval suite (`evals/` — 47 files) & secure fork-PR eval gating (`eval-pr.yml`):**
  - Covers behavioral failure modes most teams never test: `answer-vs-act.eval.ts`, `frugalReads.eval.ts`, `frugalSearch.eval.ts`, `prompt_injection_mcp.eval.ts`, `shell_command_safety.eval.ts`, `sandbox_recovery.eval.ts`, `tool_output_masking.eval.ts`, `validation_fidelity.eval.ts`, `validation_fidelity_pre_existing_errors.eval.ts`, `interactive-hang.eval.ts`, plus `llm-judge.ts` and `eval:{validate,inventory,report,coverage}` CLIs.
  - **`eval-pr.yml` security pattern:** Runs on `pull_request_target`, checks out *trusted `main`* first to run `scripts/changed_prompt.js` on the fetched PR diff, posts an *"Action Required: Evaluation Approval"* comment if prompts/tools/steering changed, and **only** checks out fork code + spends LLM eval tokens after a maintainer approves the `eval-gate` GitHub environment!
  - Also runs on-demand SWE-bench Verified evals (`eval.yml`) inside a pinned Docker container (`@sha256:...`) and nightly memory/perf regression suites (`memory-tests/`, `perf-tests/`, `deflake.yml`).
- **Clever migration drift guard (`agent-session-drift-check.yml`):** During dual-implementation refactors (legacy vs. new `AgentSession`), watches paired files via the GitHub API (no checkout needed!), posts an upsert warning comment if only one side of a pair was modified, and **auto-deletes the comment** once both sides are updated!
- **Comprehensive lint stack (47 workflows total!):** ESLint (`--max-warnings 0`), `actionlint`, `shellcheck`, `yamllint`, `lychee`, `--sensitive-keywords`, `--check-github-actions-pinning` (uses `ratchet` SHA pinning comments), `pr-rate-limiter.yaml`, `pr-size-labeler.yml`, and `merge-queue-ci-skipper` to avoid redundant runs on merge queues.

## 3. Architectural Bets & Craft
- **Multi-runtime test matrix:** Integration tests explicitly run against `sandbox:none`, `sandbox:docker`, and `sandbox:podman`, plus Node SEA launch tests (`test:sea-launch`) and VS Code companion integration tests.
- **Full-lifecycle release train:** Automated daily `nightly`, weekly `preview`, weekly `stable` promotion, `release-rollback.yml`, and comment-triggered patch releases (`release-patch-0..3`).
- **Clear deprecation / product-boundary notice:** README prominently explains the June 2026 transition of free/Gemini 4+ users to Antigravity CLI (`agy`) while keeping `gemini-cli` focused on enterprise Google Cloud Code Assist.

## 4. Commit, PR & Maintenance Reality
- **Stabilization / maintenance mode:** Last 50 commits span **18.1 days** (2026-11-06 to 2026-11-24), **88% conventional commits**, **70% fix/revert**, **14% AI co-author** (mostly `gemini-cli-robot` automated changelogs).
- **Controlled tracker:** **751 open issues** (down dramatically for a 109k-star repo) thanks to aggressive bot automation (`gemini-automated-issue-dedup`, `gemini-automated-issue-triage`, `gemini-lifecycle-manager`, `pr-rate-limiter`, mandatory issue linking).

## 5. Steal vs. Avoid
- **Steal:**
  1. **Behavioral eval taxonomy** (`answer-vs-act`, `frugalReads`, `prompt_injection_mcp`, `validation_fidelity`, `validation_fidelity_pre_existing_errors`) + `eval:{validate,inventory,coverage}` scripts.
  2. **Two-stage `pull_request_target` eval gate (`eval-pr.yml`):** Detect prompt/tool changes from trusted `main` first, then gate expensive/secret-bearing eval runs behind a manual GitHub Environment approval.
  3. **File-pair migration drift bot (`agent-session-drift-check.yml`)** — zero-checkout API check that warns when a legacy/new parallel implementation drifts and self-deletes when fixed.
  4. **Automated `deflake` runner + `memory-tests/` + `perf-tests/`** with explicit baseline update scripts.
  5. **`lint.js` wrapping `actionlint` + `shellcheck` + `yamllint` + Actions SHA-pin verification** — catches CI bugs before they break `main`.
- **Avoid:**
  1. **47 GitHub Actions workflows** — heavy operational complexity that only makes sense for a large Google-staffed org with self-hosted 16-core runners.
  2. **571-line `CONTRIBUTING.md` + bespoke `GEMINI.md`** instead of a lean cross-tool `AGENTS.md`.
