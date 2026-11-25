# Paradev (`ParadevAI/Paradev`, formerly Superset)

- **Snapshot:** `16,638★` · `1,501` forks · `1,263` open issues · `MIT` · Active (pushed 2026-11-25)
- **Primary Stack:** TypeScript monorepo (35.2 MB TS, 2.75 MB MDX, Swift, Kotlin, TLA+), Bun + Turborepo, Electron desktop, Next.js web/API, Expo mobile, Drizzle ORM (Postgres/Neon + local SQLite), tRPC, Lingui i18n.
- **Data source:** [`data/chunk-01/ParadevAI__Paradev.json`](../../data/chunk-01/ParadevAI__Paradev.json)

## 1. Agent Instruction & Docs Hygiene
- **Strong progressive disclosure:** `AGENTS.md` is 292 lines (16.2 KB), `CLAUDE.md` is a 1-line `@AGENTS.md` pointer (zero drift), and deep procedural guides live in 16 `.agents/skills/` folders (`cdp-verification`, `mobile-sim-verification`, `db-migrations`, `trpc-compat`, `verify-sandbox-asleep`, `incident-triage`, `dev-doctor`, etc.) plus scoped package guides (`packages/trpc/AGENTS.md`, `apps/desktop/AGENTS.md`, `apps/mobile/AGENTS.md`).
- **Lean `docs/` (only 5 root items):** `agent-tooling.md`, `deploy-workflows.md`, `environment-variables.md`, `plugins.md`, `runbooks/`. Explicitly bans committing plans/specs/research to the public repo (`docs: move internal design notes to ParadevAI/plans (#10191)`).
- **Self-driving CLI designed for agents:** `paradev schema` outputs every CLI command/option as JSON so agents query it with `jq` instead of scraping `--help`, and `--json` auto-enables in agent environments.
- **Comment discipline:** Explicit anti-slop rule with C++ good/bad examples and ASD-STE100 Simplified Technical English guidance.

## 2. Mechanical Gates & Quality Control
- **Best-in-class `biome.jsonc` architectural ratchets:** Uses `noRestrictedImports` (as `"error"`) to encode hard-won production bugs directly in the linter:
  - Bans `execSync`/`spawnSync`/`execFileSync` on Electron main, `host-service`, and `pty-daemon` event loops — paired with an explicit 3-file legacy allowlist frozen by ratchet tests.
  - Bans direct `@vercel/sandbox` imports outside `packages/trpc/src/lib/sandbox` so callers cannot accidentally wake stopped sandboxes.
  - Bans fleet-wide admin DB queries (`queryFleetCloudUsage*`) outside admin surfaces.
  - Bans TanStack Router `<Navigate>` in the desktop renderer (prevents React error #185 infinite render loops).
  - Bans `node:*` imports in renderer code.
- **22 CI workflows** with high operational maturity:
  - `sherif` (monorepo dependency consistency), `vale` (prose lint for marketing copy), `check:versions` (desktop == host-service == cli lockstep), `check:plugins` (generated manifest drift), `check:i18n && git diff --exit-code`, `check:durable-objects` (prevents silent storage loss when renaming Cloudflare Durable Objects).
  - Production DB migrations run with `PGOPTIONS="-c lock_timeout=5s -c statement_timeout=60s"`, `set -o pipefail`, targeted deadlock/lock-timeout retry loop, and a post-migration verification script.
- **Hard test-speed budget:** Whole CI targets ~2 minutes; `AGENTS.md` explicitly bans tests > 5s, bans `mock.module` on shared modules, bans heavy real-git stress suites, and splits Node-only PTY suites into `*.node-test.ts` so Turborepo runs them beside Bun suites.
- **Gap vs. T3 Code:** No `evals/` directory for model-facing prompt/tool evaluation, and no `knip` dead-code gate yet (dead component cleanup appears manually in commits like `refactor(ui): delete the unused FileDiffTool component`).

## 3. Architectural Bets & Craft
- **Full cloud + local + mobile SaaS platform:** Unlike T3 Code's single-server local/relay design, Paradev runs a full cloud backend (Next.js API, Neon Postgres with per-PR Neon branches, Vercel previews, Cloudflare Durable Objects, Vercel Sandboxes, Better Auth, billing via Autumn) alongside a local Electron desktop + `host-service` + `pty-daemon`.
- **Formal verification signal:** Contains `7.4 KB` of TLA+ specs — rare among agentic startups and signals serious concurrency modeling.
- **Heavy dependency patch burden:** 20 `patchedDependencies` in root `package.json` (`xterm` betas, `metro`, `react-native`, `node-pty`, `trpc-electron`, `@pierre/diffs`, `electron-chrome-extensions`).
- **CDP-first visual verification:** Dev desktop exposes Chrome DevTools Protocol (`RENDERER_REMOTE_DEBUG_PORT`) with an explicit safety check verifying `/json/list` matches the workspace's `DESKTOP_VITE_PORT` before interacting.

## 4. Commit, PR & Maintenance Reality
- **High velocity & discipline:** Last 50 commits span just **3.2 days** (2026-11-22 to 2026-11-25), **98% conventional commits**, **36% fix/revert** (healthy feature-to-fix balance), **0% explicit AI co-author trailers** (team strips or omits trailers even though agents clearly drive PRs; `paradev-app[bot]` has 25 contributions).
- **Tight core team:** 4 engineers dominate (`Kitenite` 2,848, `saddlepaddle` 1,943, `AviPeltz` 529, `harshithmullapudi` 201). CLA required for external contributors.
- **Open issue pressure:** 1,263 open issues, mitigated with `triage-issue.yml` and `stale-prs.yml`.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Domain-specific `noRestrictedImports` ratchets** in Biome/oxlint (blocking sync subprocesses on serving loops, tenant-scoping DB queries, unsafe router primitives) with tiny shrinking legacy allowlists.
  2. **2-minute test-suite culture** codified in `AGENTS.md` (ban real waiting, ban `mock.module` on shared modules, isolate PTY tests into `*.node-test.ts`).
  3. **`paradev schema` JSON introspection + auto-JSON under agent envs** for any CLI meant to be driven by coding agents.
  4. **Deployment safety invariants** (`check:durable-objects`, `lock_timeout=5s` + `pipefail` on Drizzle migrations, `sherif` for monorepo dep drift).
- **Avoid:**
  1. **Patching 20 upstream beta packages** unless truly necessary — creates continuous upgrade drag.
  2. **Mixing SaaS billing/cloud/admin/marketing/desktop/mobile into one monorepo** unless you have dedicated infra engineers (45 KB `deploy-preview.yml` + 45 KB `deploy-production.yml`).
