# OpenSpec (`Fission-AI/OpenSpec`)

- **Snapshot:** `75,717★` · `5,180` forks · `214` open issues · `MIT` · Active (created Aug 5, 2025; pushed 2026-11-25)
- **Primary Stack:** **5.8 MB TypeScript** (`@fission-ai/openspec`), Node `>=22.20`, pnpm 10, ESLint 10 + `typescript-eslint`, Vitest 5, Zod 4, Commander 14, Changesets, Nix flake + Homebrew + npm OIDC trusted publishing.
- **Data source:** [`data/chunk-06/Fission-AI__OpenSpec.json`](../../data/chunk-06/Fission-AI__OpenSpec.json)

## 1. Agent Instruction & Docs Hygiene
- **Ironic blind spot:** Root **`AGENTS.md` is literally `0` bytes (empty)**! All real developer and agent engineering conventions live in a crisp 67-line `CONTRIBUTING.md`, 27 `docs/` files (`agent-contract.md`, `writing-specs.md`, `opsx.md`), 4 `.agents/skills/`, and OpenSpec's own `openspec/` specs folder.
- **Stray root clutter:** `README_OLD.md` and `openspec-parallel-merge-plan.md` remain committed at repo root.
- **Clear contribution gating (`CONTRIBUTING.md`):** **PRs are limited to maintainers and invited contributors** (after discussing on an issue and receiving the `approved` label) — keeping open issues to just **`214`** at **75.7k★**.
- **Two-PR feature workflow:** Features split into PR 1 (**Proposal**: `openspec/changes/<name>/` only, `Part of #123`) and PR 2 (**Implementation**: code + checked-off `tasks.md` after proposal merges, `Closes #123`).

## 2. Mechanical Gates & Quality Control
- **Ultra-lean 5-workflow CI (`ci.yml`, `binaries.yml`, `release-prepare.yml`, `security.yml`):**
  1. **CLI startup module-count regression test (`test/cli-e2e/startup-modules.test.ts`):** After discovering `openspec --version` loaded **485 modules (~0.5s on Windows)**, OpenSpec enforced lazy `await import()` inside command actions and wrote a test that **fails CI** if any command definition starts eagerly importing heavy modules (`zod`, `yaml`, `ora`, `tinyglobby`).
  2. **CI docs-only path parity test (`test/ci-docs-only.test.ts`):** Verifies that the docs-only `dorny/paths-filter` ignore list stays identical across `ci.yml` and `binaries.yml`.
  3. **Cross-OS + oldest-supported-Node matrix:** Tests Ubuntu, macOS, and Windows PowerShell on exact floor `Node 22.20.0` plus current Node 22 & 24 LTS, with SHA-pinned GitHub Actions (`actions/checkout`, `pnpm/action-setup`, `setup-node`).
  4. **Best-documented `pnpm-workspace.yaml` CVE override discipline in the study:** Every override cites exact GHSA/CVE IDs, marks whether it's dev-only or shipped, gives the exact removal check (`pnpm why ...`), and documents a crucial pnpm 10 trap (*`pnpm.overrides` in `package.json` silently replaces rather than merges `pnpm-workspace.yaml` overrides!*).
  5. **Passwordless npm OIDC trusted publishing** (`id-token: write`, Node 24) + GitHub App token for Changesets PRs so version PRs still trigger normal CI.

## 3. Architectural Bets & Craft
- **Lightweight, brownfield-first Spec-Driven Development:** Plain Markdown delta specs (`ADDED`/`MODIFIED` requirements + `WHEN`/`THEN` scenarios) under `openspec/changes/<name>/`, designed to be iterative rather than waterfall, plus a `/openspec` router (`v2.2.0`) and cross-repo **Stores** (beta) for multi-repo team planning.
- **Built-in bug-report telemetry helper:** `openspec feedback "what happened"` auto-populates version and platform into a prefilled GitHub issue form.

## 4. Commit, PR & Maintenance Reality
- **High-craft, AI-accelerated maintenance:** **50 commits in 25 days** (`2026-10-30` to `2026-11-24`, `v1.17.0` → `v2.2.0`, PR `#2,302`), **86% conventional**, **40% fix/revert**, **98% AI signal**.
- Very tight core: `clay-good` authored **35/50** recent commits (232 all-time), alongside founder `TabishB` (523 all-time) and `openspec-release-bot[bot]` (7/50).

## 5. Steal vs. Avoid
- **Steal:**
  1. **`startup-modules.test.ts`** — mechanically guarding CLI cold-start time by asserting which modules each subcommand loads (massive win for any CLI invoked frequently by coding agents!).
  2. **GHSA-annotated `pnpm-workspace.yaml` overrides + removal commands (`pnpm why ...`)** and never duplicating `pnpm.overrides` in `package.json`.
  3. **Two-PR proposal-then-implementation flow** for architectural features + maintainers/invited-only PR gating.
  4. **CI path-filter parity tests (`test/ci-docs-only.test.ts`)** + **npm OIDC trusted publishing** (zero long-lived npm tokens).
- **Avoid:**
  1. **Leaving a `0`-byte `AGENTS.md` at repo root** (and stray `README_OLD.md` / merge-plan docs) — put the startup-module invariant and test commands directly into `AGENTS.md`.
