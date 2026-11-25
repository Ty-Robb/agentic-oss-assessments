# CoStrict (`zgsm-ai/costrict`)

- **Snapshot:** `4,464★` · `205` forks · `14` open issues · `Apache-2.0` · Slowing / quiet since Sep 30, 2026 (created Apr 10, 2025; pushed `2026-09-30`)
- **Primary Stack:** **15.1 MB TypeScript** (VS Code extension `src/` + React `webview-ui/` + `apps/` + `packages/`), pnpm 10 + Turborepo, ESLint 9 + Prettier + `knip`, Changesets, Husky + `lint-staged`, Docker Compose eval harness (Postgres + Redis).
- **Data source:** [`data/chunk-05/zgsm-ai__costrict.json`](../../data/chunk-05/zgsm-ai__costrict.json)

## 1. Agent Instruction & Docs Hygiene
- **6-line inherited `AGENTS.md` (615 bytes):** A direct forensic fingerprint of its lineage as an enterprise fork of Roo Code (itself a fork of Cline):
  - Rule 1 is **verbatim** Roo Code's 5-line `SettingsView` invariant (*bind inputs to local `cachedState`, not live `useExtensionState()`*).
  - Rule 2 is CoStrict's lone addition: *"Commit messages must be written in English and follow Conventional Commits (`type(scope): summary`). Never use Chinese in commit messages, even for local-only commits."*
- **Zero `docs/` directory and zero `.agents/` skills** (docs live externally at `docs.costrict.ai`); retains Roo Code's `.roomodes`, `.roo/`, `.rooignore`, `sync-upstream.md`, and an inherited Issue-First `CONTRIBUTING.md`.
- **Root clutter smells:** Stray files at repo root (`localhost`, `progress.txt`, `CHANGELOG_ARCHIVE.md`) alongside disabled Roo workflows (`website-deploy.yml.disabled`, `website-preview.yml.disabled`).

## 2. Mechanical Gates & Quality Control
- **11 workflows (9 active, 2 `.disabled`):** `code-qa.yml`, `codeql.yml`, `evals.yml`, `changeset-release.yml`, `cli-release.yml`, `deploy-vsix.yml`, `marketplace-publish.yml`, `nightly-publish.yml`, `update-contributors.yml`.
- **Dockerized Postgres + Redis eval runner (`evals.yml`):** Inherited from Roo Code, runs on `blacksmith-16vcpu-ubuntu-2404` when a PR receives the `evals` label or via `workflow_dispatch`, spinning up Postgres + Redis containers, running migrations, executing `pnpm --filter @roo-code/evals cli --ci`, and tearing down volumes with `if: always()`.
- **Disciplined CVE & dead-file hygiene:**
  - `pnpm-workspace.yaml` maintains **40+ targeted transitive CVE overrides**, `onlyBuiltDependencies` + `ignoredBuiltDependencies`, and `patchedDependencies` (`patches/axios@1.16.0.patch`).
  - `knip.json` (`pnpm knip` → `knip --include files`) actively tracks unused files across `src/`, `webview-ui/`, and `packages/`.
- **High conventional-commit compliance:** **92% conventional commits** across the last 50 commits — proof that even a single crisp 1-line rule in `AGENTS.md` (paired with a small team) produces clean git history.

## 3. Architectural Bets & Craft
- **Enterprise-hardened Roo Code fork ("Strict Mode" + RAG review + private deployment):** Adds structured Requirements → Architecture → Task Plan → Tests workflows ("Strict Mode"), repository-wide RAG multi-model code review, OpenSpec integration (`/openspec-init`), physical-isolation private deployment, and JetBrains companion support (`zgsm-sangfor/costrict-for-jetbrains`).
- **Practical security hardening in recent commits:** Shipped workspace trust approval for custom tools & MCP servers (`#1356`), remediated command injection / path traversal / SSRF (`#1353`), added JetBrains CSP nonce support (`#1344`), and distinguished authoritative model lists from cache (`#1348`).
- **Fork-inheritance overhang:** Internal package names (`@roo-code/types`, `@roo-code/evals`), comments (`# Should be apps/vscode`), `knip.json` ignores (`apps/web-roo-code`, `RooIgnoreController`), and disabled Vercel preview workflows (`<!-- roo-preview-comment -->`) all show the persistent tax of carrying a 15 MB upstream fork after upstream `RooCodeInc/Roo-Code` itself archived in May 2026.

## 4. Commit, PR & Maintenance Reality
- **Single-engineer enterprise maintenance:** **50 commits over 3.6 months** (`2026-06-13` to `2026-09-30`, `v3.0.16` → `v3.0.23`), **92% conventional**, **14% fix/revert**, **2% AI signal**.
- **`mini2s` authored 44 of the last 50 commits** (759 all-time), while upstream Roo/Cline founders `mrubens` (1,763) and `saoudrizwan` (962) remain #1 and #2 in git history.
- **Recent contraction / pause:** No commits pushed in ~8 weeks (`2026-09-30` to `2026-11-25`), and the final commits disabled quota purchase entries (`#1374`) and removed the code-completion feature & runtime installer (`#1372`).

## 5. Steal vs. Avoid
- **Steal:**
  1. **1-line language + commit-style invariant in `AGENTS.md`** — cheap, unambiguous, and empirically effective (92% compliance).
  2. **Active `pnpm.overrides` CVE pinning + `onlyBuiltDependencies` + `knip --include files`** for keeping a large TypeScript workspace patched and free of orphaned files.
  3. **Workspace-trust gating for custom tools and MCP servers** (`#1356`) — essential security control for any enterprise coding agent.
- **Avoid:**
  1. **Maintaining a heavily customized downstream fork of a 15 MB IDE extension with one engineer** once upstream pivots or archives — you inherit all the historical scaffolding (`@roo-code/*`, `.disabled` workflows, `sync-upstream.md`) without upstream velocity.
  2. **Leaving temporary debug/agent scratch files (`localhost`, `progress.txt`) committed at repo root.**
