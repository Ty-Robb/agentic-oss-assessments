# OpenHands (`OpenHands/OpenHands`, Agent Canvas)

- **Snapshot:** `94,306★` · `12,632` forks · `1,252` open issues · `MIT` · Active (created Mar 2024; pushed 2026-11-25)
- **Primary Stack:** TypeScript React 19 + React Router 8 + Vite 8 + Electron frontend (`@openhands/agent-canvas`, 15.8 MB TS) consuming a cleanly separated Python `software-agent-sdk` backend, Docker/Helm self-hosting, ESLint + Prettier, Vitest, Playwright (mock-LLM, Docker, live, bind-policy, Windows-install), **Stryker mutation testing**, `release-please`.
- **Data source:** [`data/chunk-03/OpenHands__OpenHands.json`](../../data/chunk-03/OpenHands__OpenHands.json)

## 1. Agent Instruction & Docs Hygiene
- **One of the best-engineered `AGENTS.md` files in the entire study (133 lines / 10.6 KB):**
  - **Explicit multi-repo ownership table** (`OpenHands` Canvas UI vs. `software-agent-sdk` Python backend/wire contracts vs. `extensions` vs. `automation`) preventing agents from reimplementing backend logic in the frontend.
  - **10 domain skills under `.agents/skills/`** (each storing detailed rules in `references/guide.md`, explicitly forbidding copying them back into `AGENTS.md`).
  - **Verification Skill Independence (standout innovation):** Implementor agents must treat `.agents/skills/verify-*/` as **read-only**. They are forbidden from modifying verification maps, drivers, or expected results in the same PR as product code — enforced mechanically in CI via `verify-skill-isolation.yml`!
  - **`HUMAN:` PR section protection:** Explicitly forbids AI agents from writing, editing, or removing the `HUMAN:` section of PR descriptions (enforced by `pr-description-check.yml`), guaranteeing human-authored intent on every PR.
  - **Shell commit safety tip:** Documents `git commit -F <file>` instead of long multi-line `-m` strings to avoid shell corruption.

## 2. Mechanical Gates & Quality Control
- **Diff-scoped Mutation Testing (`stryker.config.mjs`):** Ships `test:mutation`, `test:mutation:diff` (`scripts/stryker-diff.mjs`), and `test:mutation:incremental` — directly fights the #1 AI testing failure mode (tests that pass without actually asserting behavior)!
- **Multi-layer E2E pyramid (6 Playwright configs!):** `mock-llm` (fast deterministic agent flows), `mock-llm-docker`, `bind-policy` (security/network binding), `windows-install`, and `live` (runs on `main` pushes with Haiku + video recording via `ci.yml`).
- **7-day Dependency Release-Age Policy:** Enforces `npm install --min-release-age=7` and pins `npm@11.12.1` (explicitly documenting that `npm@10.5.0` silently ignored `--min-release-age`!), plus Dependabot `cooldown.default-days: 7` and exact-pinned direct dependencies.
- **CI script unit testing & governance:** `ci-script-tests.yml` runs `pytest` on `.github/scripts/tests/`; `verify-skill-isolation-tests.yml` tests the isolation checker; `issue-readiness-check.yml` automatically strips the `ready-for-dev` label if applied by a non-maintainer; `issue-duplicate-checker.yml` dogfoods OpenHands Cloud to detect and auto-close aged duplicate issues after 3 days.
- **Release hygiene:** `ci.yml` never cancels `push` runs (so `release-please` tag rulesets always see green checks on the exact tagged commit) and rejects temporary `.pr/` artifacts in release PRs.

## 3. Architectural Bets & Craft
- **Clean multi-repo decomposition:** Split the monolithic Python+TS OpenHands repo into 4 focused repos (`OpenHands` Canvas UI, `software-agent-sdk`, `extensions`, `automation`) with explicit minimum-version compatibility checks (`compatibility.minimumAgentServer` in `config/defaults.json`).
- **Repositioned into a direct T3 Code / Paradev competitor:** OpenHands Agent Canvas now runs OpenHands, Claude Code, Codex, Gemini, Pi, OpenCode, or any ACP agent across local, Docker, VM, and Cloud backends with scheduled/webhook automations — while keeping the frontend a single clean npm package (`agent-canvas`).
- **Strong testing philosophy in `AGENTS.md`:** Bans mirroring literal source/fixture/class-string definitions in tests and forbids exporting internals solely for testability.

## 4. Commit, PR & Maintenance Reality
- **High, orderly cadence:** Last 50 commits span **2 days** (2026-11-23 to 2026-11-25), **100% conventional commits**, **36% fix/revert**, **26% AI/bot signal** (includes `openhands-release-bot[bot]` and `dependabot[bot]`).
- **Balanced team of ~8 core engineers** (`hieptl`, `tofarr`, `enyst`, `xingyaoww`, `rbren`, `malhotra5`, `neubig`, `amanape`). Healthy `1,252` open issues for a 94k-star repo.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Verification Skill Independence (`verify-skill-isolation.yml`):** Mechanically forbid an implementing PR from editing its own verification specs/skills — closes the "agent weakens the test to make CI green" loophole.
  2. **Diff-scoped mutation testing (`stryker-diff.mjs`):** Run Stryker only on changed lines to prove agent-written tests actually catch real bugs.
  3. **`HUMAN:` PR section validator (`pr-description-check.yml`)** + unit tests for CI scripts (`ci-script-tests.yml`).
  4. **7-day npm/PyPI release-age policy** (`npm@>=11.10` `--min-release-age=7` + Dependabot cooldown) + exact-pinned deps.
  5. **Mock-LLM Playwright E2E** (`playwright.mock-llm.config.ts`) for deterministic, zero-token end-to-end UI verification of agent conversations.
- **Avoid:**
  1. **High Dependabot commit volume on `main`** (11 of last 50 commits are individual Dependabot bumps) — grouping updates more aggressively reduces noise and CI churn.
  2. **6 separate root `playwright.*.config.ts` files** — cleaner grouped under `tests/e2e/configs/`.
