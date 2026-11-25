# Pi (`earendil-works/pi`, formerly `badlogic/pi-mono`)

- **Snapshot:** `123,818★` · `15,995` forks · **`307` open issues** · `MIT` · Active (pushed 2026-11-25)
- **Primary Stack:** Plain npm workspaces TypeScript monorepo (31.0 MB TS), Node >= 22.19 **erasable TypeScript** (strip-only mode), Biome + GritQL plugin, Vitest + `node:test`, Nix flake. Core packages: `pi-ai`, `pi-agent-core`, `pi-coding-agent`, `pi-tui`, `pi-durable`, `chord`, `pi-telemetry`.
- **Data source:** [`data/chunk-02/earendil-works__pi.json`](../../data/chunk-02/earendil-works__pi.json)

## 1. Agent Instruction & Docs Hygiene
- **Masterclass in concise, high-density `AGENTS.md` (160 lines / 14.5 KB):** Zero fluff, zero emojis, strict conversational rules (*"state problem, concrete example/trace, then solution"*; *"explicitly say whether you agree or disagree before saying what you changed"*), and razor-sharp engineering constraints.
- **Multi-agent working-tree safety protocol:** Explicitly assumes **multiple parallel agents share one checkout** — bans `git add -A`, `git add .`, `git stash`, `git reset --hard`, `git checkout .`, `git commit --no-verify`, and `gh pr checkout` / `git switch` during PR reviews (review via `gh pr diff` and `git show <ref>:<path>` instead!).
- **Scoped vertical-slice specs & runnable examples:** `Chord v2` pairs `docs/design.md` + `docs/slices.md` (with explicit `Carry-over` lists) and requires numbered runnable examples (`test/examples/NN-topic.ts`) and GC tests for every `WeakMap` cache.
- **Strict anti-defensive-coding rules:** Bans runtime `typeof`/`instanceof`/`in` on already-typed values, mandates tagged unions (`kind`) over `in` narrowing, bans boolean flag parameters (use two functions or a tagged value), bans inline `await import()`.

## 2. Mechanical Gates & Quality Control
- **Best anti-slop contributor gate in open source (`issue-gate.yml`, `pr-gate.yml`, `approve-contributor.yml`):**
  - **Every issue and PR from an unapproved contributor is auto-closed on arrival.** Maintainers review auto-closed issues daily during working hours and reply `lgtmi` (issues) or `lgtm` (issues + PRs) to add the user to `.github/APPROVED_CONTRIBUTORS`.
  - **Result:** Only **307 open issues** on a **123.8k-star** repo (10× lower than T3 Code, 13× lower than OpenCode, 93× lower than Codex!).
  - Explicitly states in `CONTRIBUTING.md`: *"Why not let AI triage everything? Polished AI-generated issues can still be wrong, misleading, or expensive to investigate. Human review remains the final gate."*
- **Obsessive supply-chain & packaging discipline (`npm run check`):**
  - `check:pinned-deps` (all direct & workspace deps pinned to exact versions), `check:runtime-deps`, `check:ts-imports`, `check:entry-graphs`, `check:install-lock:coding-agent` (explicit allowlist for any dep with lifecycle scripts!), `check:released-changelogs` (ensures released changelog sections are immutable), `check:browser-smoke`, plus `npm ci --ignore-scripts` everywhere.
  - Pre-commit hook **blocks `package-lock.json` edits** unless `PI_ALLOW_LOCKFILE_CHANGE=1`.
- **Custom GritQL Biome plugin:** `./scripts/biome/model-type-comparison.grit` enforces semantic checks alongside Biome.
- **Evals & conformance:** Dedicated `@earendil-works/pi-evals` workspace, `test:mcp-conformance`, and faux-provider test harness (`test/suite/harness.ts`) so tests never touch paid APIs.

## 3. Architectural Bets & Craft
- **"Minimal core + extensions" philosophy:** Intentionally skips built-in plan mode, subagents, and built-in permission sandboxes in core — instead exposes clean SDK, RPC, extensions, skills, and containerization patterns (Gondolin micro-VM, Docker, OpenShell). This is why huge downstream projects like OpenClaw build directly on Pi.
- **Erasable TypeScript only:** Forces Node strip-only compatibility (no `enum`, `namespace`, or parameter properties), keeping runtime execution fast and bundler-free where possible.
- **Zero monorepo orchestration overhead:** Uses plain `npm` workspaces and explicit topological scripts instead of Nx or Turborepo — honoring radical simplicity.
- **Cost & memory discipline:** Bans module-level strong caches (require `WeakMap` + GC test) and adds in-memory telemetry cost guards to tests.

## 4. Commit, PR & Maintenance Reality
- **High craft, sustainable pace:** Last 50 commits span **1.7 days** (2026-11-23 to 2026-11-25), **90% conventional commits**, **60% fix/revert**, **2% explicit AI trailers**.
- **Elite small team:** Led by `badlogic` (Mario Zechner, 4,535 commits) and `mitsuhiko` (Armin Ronacher, 1,042 commits) plus ~6 core engineers (`davidbrai`, `christianklotz`, `cristinaponcela`, `vegarsti`, `petrroll`) and `robopipi[bot]` (95 commits).

## 5. Steal vs. Avoid
- **Steal:**
  1. **Default-closed `lgtmi`/`lgtm` contributor gate** if an open-source repo ever faces AI-slop PR/issue floods — proven to keep a 124k-star tracker down to 307 issues.
  2. **Multi-agent safe Git rules in `AGENTS.md`** (explicit path staging, banning `git add -A`/`stash`/`reset --hard`, reviewing PRs without switching branches).
  3. **Supply-chain lockfile & lifecycle-script gates** (`npm ci --ignore-scripts`, `check:pinned-deps`, `check:install-lock`, pre-commit lockfile guard).
  4. **Erasable TypeScript + tagged-union-only narrowing + no boolean flag params** — produces remarkably clean, agent-readable TypeScript.
  5. **`check:released-changelogs` & `WeakMap` GC tests** for long-lived server runtimes.
- **Avoid:**
  1. **Turning off `noExplicitAny` and `noNonNullAssertion` in `biome.json`** — relies on prose review instead of mechanical enforcement for those two rules.
  2. **Manual sequential `cd packages/a && npm run build && cd ../b ...` chains** once package count grows past ~12 (fragile compared to a real task graph).
