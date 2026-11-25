# Get Shit Done / GSD (`gsd-build/get-shit-done`)

- **Snapshot:** `64,113★` · `5,442` forks · `0` open issues · `MIT` · **Archived (May 31, 2026 — moved to `open-gsd/gsd-core` after a compromise warning)**
- **Primary Stack:** **7.3 MB CommonJS JavaScript** + **2.6 MB TypeScript** (`sdk/`) + 44 KB Shell; Node `>=22`, built-in `node:test` + `c8` (70% line coverage floor), Vitest for SDK, custom Changeset & security scan scripts.
- **Data source:** [`data/chunk-06/gsd-build__get-shit-done.json`](../../data/chunk-06/gsd-build__get-shit-done.json)

## 1. Agent Instruction & Docs Hygiene
- **Compact 41-line `AGENTS.md` (3.1 KB)** covering the hybrid CommonJS (`get-shit-done/`, `tests/*.test.cjs`) + ESM TypeScript (`sdk/`) split, `node:test` conventions, and mandatory pre-release security scans (`secret-scan.sh`, `base64-scan.sh`, `prompt-injection-scan.sh`).
- **Massive governance overhead before archival:** **791-line / 44.3 KB `CONTRIBUTING.md`** mandating 3 strict issue-first tiers (`confirmed-bug`, `approved-enhancement`, `approved-feature`), banning draft PRs completely, and using GitHub issue numbers as ADR/PRD prefixes (`docs/adr/<issue#>-<slug>.md` — *"never compute a next sequential number locally"*).
- **Visible repo clutter:** 44 `docs/` files including 11 archived release-candidate markdowns, `QUICK-WINS-CONFIRMED-BUGS.md`, `TEST-EXAMPLES.md`, and `.plans/`.

## 2. Mechanical Gates & Quality Control
- **20 GitHub Actions workflows — heavy PR-policing and freshness automation:**
  - **10 freshness checks** in `package.json` (`check:alias-drift`, `check:state-document-fresh`, `check:configuration-fresh`, `check:secrets-fresh`, `check:decisions-fresh`, etc.) + `lint:no-source-grep` (`scripts/lint-no-source-grep.cjs`, banning fragile grep-of-source tests!) + `lint:skill-deps` + `lint:descriptions`.
  - **Prompt-injection & secret scanning (`security-scan.yml`):** Dedicated `prompt-injection-scan.sh`, `base64-scan.sh`, and `secret-scan.sh` — crucial for any repo shipping Markdown prompts installed into users' coding agents!
  - **Aggressive PR policing:** `close-draft-prs.yml` (auto-closes every draft PR), `require-issue-link.yml`, `changeset-required.yml`, `docs-required.yml`, `pr-gate.yml` (size labels + 500-line warning), and **`dismiss-unauthorized-pr-approvals.yml`** (auto-dismissing reviews from non-collaborators and a hardcoded blocked username, with a 15-minute cron fallback because `pull_request_review` from outside collaborators stalls in `action_required`!).
  - **Clean archival redirect (`auto-close-deprecated.yml`):** Auto-comments, closes, and locks any new issue/PR pointing contributors to `open-gsd/gsd-core`.

## 3. Architectural Bets & Craft
- **Meta-prompting & context-engineering SDLC engine:** Pioneered structured phase-based `.planning/` context files and multi-runtime command routing across Claude Code, OpenCode, Gemini CLI, and Codex, later extracting a TypeScript `sdk/` alongside its legacy 7.3 MB CommonJS core.
- **Process heaviness tradeoff:** Matt Pocock's `skills` README explicitly singled out GSD (alongside BMAD and Spec-Kit) as an example of process-owning frameworks that take control away from engineers and make process bugs painful to debug.

## 4. Commit, PR & Maintenance Reality
- **Dramatic governance/security collapse right in the commit history:**
  - On **May 22, 2026** (commit `126b6b9e`), top maintainer `trek-e` (1,435 contributions vs. original creator `glittercowboy` 945) pushed **`"WARNING: This repository appears compromised — use the fork at GSD-redux/get-shit-done-redux"`**, followed by auto-closing PRs/issues and redirecting the community to `open-gsd/gsd-core` before archiving on May 31, 2026!
  - Across its final 50 commits (`2026-05-18` to `2026-05-31`): 80% conventional, 40% fix/revert, 72% AI signal (`trek-e` 39/50, `jeremymcs` 9/50).

## 5. Steal vs. Avoid
- **Steal:**
  1. **`prompt-injection-scan.sh` + `base64-scan.sh` in CI** for any repository shipping prompts, skills, or templates consumed by LLMs.
  2. **Using GitHub issue numbers (`docs/adr/<issue#>-<slug>.md`) as ADR/PRD prefixes** — eliminates merge-number collisions across parallel worktrees!
  3. **`lint-no-source-grep.cjs`** — mechanically banning brittle tests that regex-grep source files instead of testing real behavior.
  4. **The `dismiss-unauthorized-pr-approvals` insight** (knowing that outside-collaborator review events pause in `action_required`) and clean archival redirect workflows (`auto-close-deprecated.yml`).
- **Avoid:**
  1. **7.3 MB of legacy CommonJS glued to a separate TS SDK + 44 KB of bureaucratic contribution rules** (like auto-closing every draft PR) — high cognitive friction and brittle ownership boundaries.
  2. **Weak org/maintainer ownership security on a 64k★ repo that executes install scripts and prompts on developer machines** — a prime supply-chain target.
