# bolt.diy (`stackblitz-labs/bolt.diy`)

- **Snapshot:** `20,135★` · **`10,626` forks** (>0.5× fork-to-star ratio!) · **`2` open issues** · `MIT` · Active (created Oct 13, 2024; pushed 2026-11-21)
- **Primary Stack:** **3.4 MB TypeScript** + 51 KB SCSS + 36 KB JS; React Router v8 + Vite + StackBlitz WebContainers (`@webcontainer/api`) + Vercel AI SDK v7 (`ai@7.0.176`, 22+ providers) + CodeMirror 6 + xterm.js + Nanostores + UnoCSS + MCP SDK; deploys to Cloudflare Workers (`wrangler`), Docker, and Electron (`electron-builder`).
- **Data source:** [`data/chunk-05/stackblitz-labs__bolt.diy.json`](../../data/chunk-05/stackblitz-labs__bolt.diy.json)

## 1. Agent Instruction & Docs Hygiene
- **Zero agent-facing instruction files:** No `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, or `.cursor/` directory.
- **Traditional human contributor docs:** 260-line emoji-formatted `CONTRIBUTING.md` covering manual fork-and-PR setup, Docker profiles, Dev Containers, and testing, plus 12 files in `docs/` built with MkDocs + Python Poetry (`PERFORMANCE_OPTIMIZATION.md`, `performance-architecture.md`, `mcp-tool-migration.md`, `plugin-system-implementation-plan.markdown`).
- **Honest security documentation in `README.md`:** Explicitly warns users that *"Keys entered in the UI are stored in JavaScript-accessible browser cookies and sent to the application server with requests... Protect access to the browser and use HTTPS for remote deployments."*

## 2. Mechanical Gates & Quality Control
- **Solid 13-workflow CI suite** for a 3.4 MB app (`ci.yaml`, `docker.yaml`, `electron.yml`, `performance.yaml`, `pr-release-validation.yaml`, `preview.yaml`, `quality.yaml`, `security.yaml`, `semantic-pr.yaml`, `stale.yml`, `test-workflows.yaml`, `update-stable.yml`, `docs.yaml`):
  - **Real production Docker smoke test in `ci.yaml`:** Builds `--target bolt-ai-production --no-cache`, starts the container on `127.0.0.1:5173`, polls `curl -fsS http://127.0.0.1:5173/` while verifying `State.Running == true`, dumps `docker logs` via `trap` on exit, then validates the dev target and `docker compose config --quiet`.
  - **First-class performance gating:** `.lighthouserc.json`, `.performance-budgets.json`, `vitest bench`, `perf:analyze` (`scripts/analyze-bundle.js`), `perf:check` (`scripts/check-performance-budgets.js`), and `performance.yaml`.
  - **Graceful-skip Cloudflare Workers PR previews (`preview.yaml`):** Checks whether `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` exist; if absent (e.g., on forks), passes cleanly with a helpful setup message instead of failing red; when present, deploys via `wrangler preview --json`, smoke-tests with `curl --retry 3`, and updates a single PR comment.
  - **Commit/PR validation:** SHA-pinned `amannn/action-semantic-pull-request` (`semantic-pr.yaml`), Husky pre-commit, ESLint cache + Prettier, Playwright deterministic CI browser tests (`test:e2e:ci`), `pnpm-workspace.yaml` `allowBuilds` allowlist, and `pr-release-validation.yaml` enforcing `CHANGES.md` entries on `stable-release` PRs.
- **CI smell:** `pr-release-validation.yaml` uses `lewagon/wait-on-check-action` polling for `Test` and `CodeQL Analysis` with `continue-on-error: true` on the required-check script — fragile compared to a single workflow aggregator job.

## 3. Architectural Bets & Craft
- **In-browser Node.js sandbox via WebContainers (`@webcontainer/api`):** Uniquely runs full-stack web apps, terminals, and live previews *inside the browser tab* without needing a local daemon or cloud VM — explaining its massive 10.6k fork count as a starter kit for custom AI app builders.
- **Multi-provider Vercel AI SDK + prompt library:** Abstracts 22+ cloud/local LLM providers cleanly behind Vercel AI SDK v7 and lets users swap system prompts per model size (`Simple Sal`, `Tiny Tim`).
- **Triple-target distribution strain:** Maintaining Cloudflare Workers (`wrangler`), Docker/Node, and Electron (`vite-electron.config.ts`, `notarize.cjs`, `electron-builder.yml`) in one single-package repo adds notable config surface (`56` root entries, dual Playwright configs, separate `.env.local` vs `.env` copy step for Docker).

## 4. Commit, PR & Maintenance Reality
- **Extreme Bus Factor 1:** **`dustinwloring1988` authored all 50 of the last 50 commits** (`2026-11-16` to `2026-11-21`, 5.3-day span; 566 all-time contributions, overtaking original creator `coleam00` at 85).
- **Noisy commit history despite `semantic-pr.yaml`:** Only **34% conventional commits**, **6% fix/revert**, **0% AI signal** — because PRs are merged via GitHub merge commits (`Merge pull request #2342 from dustinwloring1988/main`) from the maintainer's own fork, preserving informal WIP commits (`updated deps`, `fix chat reloads` twice, `Cleaned up test files left behind`).
- **Artificially tiny issue count (`2` open issues):** Driven by `stale.yml` plus single-maintainer triage rather than low user volume (10.6k forks, 20.1k★).

## 5. Steal vs. Avoid
- **Steal:**
  1. **Production Docker build + `curl` liveness smoke test in CI (`ci.yaml`)** — catches broken production container builds, missing runtime env/assets, and crash-on-boot regressions before release.
  2. **Explicit `.performance-budgets.json` + bundle analyzer + Lighthouse CI** wired into `package.json` scripts and CI.
  3. **Fork-friendly preview workflow (`preview.yaml`)** that checks for secrets, smoke-tests the deployed URL, and gracefully passes with instructions when secrets aren't configured.
- **Avoid:**
  1. **Storing user LLM API keys in JavaScript-accessible browser cookies** — any XSS becomes instant key exfiltration; keep keys server-side or in OS keychains/encrypted stores.
  2. **Non-squash merge commits from a personal `main` fork** — defeats `semantic-pr.yaml` and litters git history with duplicate WIP commits (`fix chat reloads`).
  3. **`continue-on-error: true` on a PR quality-gate script** — silently neutralizes the gate it exists to enforce.
