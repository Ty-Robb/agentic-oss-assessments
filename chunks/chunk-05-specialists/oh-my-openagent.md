# Oh My OpenAgent / OmO (`code-yeongyu/oh-my-openagent`)

- **Snapshot:** `71,105★` · `5,839` forks · `2,823` open issues · `SUL-1.0` (source-available; GitHub meta `NOASSERTION`) · Hyper-active (created Dec 3, 2025; pushed 2026-11-25; default branch `dev`)
- **Primary Stack:** **58.0 MB TypeScript** + 6.7 MB JS + **5.3 MB Rust** + 600 KB Shell + 443 KB Python across **45 workspace packages** and **23 Rust crates** (desktop/computer-use automation backends for macOS/X11/Wayland/Win32/AT-SPI + trust/git helpers); Bun 1.4.4 + Node 24, `oxlint`, `knip`, `tsgo`, `senpi` (fork of `pi-mono`), Next.js 15 + Cloudflare Workers (`get.omo.dev`).
- **Data source:** [`data/chunk-05/code-yeongyu__oh-my-openagent.json`](../../data/chunk-05/code-yeongyu__oh-my-openagent.json)

## 1. Agent Instruction & Docs Hygiene
- **Largest and loudest `AGENTS.md` in the 24-repo study (70.8 KB / 479 lines, duplicated byte-for-byte in `CLAUDE.md`):**
  - Opens with an ALL-CAPS profanity alert (*"HOLD THE FUCK UP. THIS ENTIRE GODDAMN CODEBASE IS BEING RIPPED APART AND REBUILT RIGHT NOW..."*), followed by an exhaustive multi-screen `STOP. QA IS MANDATORY` directive and a 7-step `MANDATORY CHANGE-EXECUTION PROTOCOL` (Explore → Plan on disk → Ultra-detailed todos → Fresh worktree → Open PR & stay until merged → `ulw-loop` → Obsessive todo tracking).
  - **Self-inflicted token & drift penalty:** Even with a `Generated: 2026-08-24` timestamp at the top (3 months stale relative to `v5.1.83` in Nov 2026!), 70.8 KB burns massive prompt context on every turn and relies on ALL-CAPS shouting where shorter, mechanically enforced rules work better.
- **High-craft operational patterns underneath the shouting:**
  - **14 `.agents/skills/`** (`opencode-qa`, `codex-qa`, `senpi-qa`, `work-with-pr`, `pre-publish-review`, `publish`, `remove-deadcode`, `tech-debt-audit`, `github-triage`, `security-research`, `hyperplan`).
  - **Unified cross-harness bootstrap (`script/agent/setup.sh` + `cleanup.sh`):** One script wired cleanly into Dev Containers, Docker, Cursor Cloud (`.cursor/environment.json`), Claude Code `SessionStart`/`SessionEnd` hooks, and Codex App `.codex/setup.sh`.

## 2. Mechanical Gates & Quality Control
- **Standout QA-evidence & hermeticity engineering (genuinely best-in-class ideas):**
  1. **Local-only `.omo/evidence/` + `sha256sum` PR proof + anti-commit CI test (`script/tracked-evidence-paths-audit.test.ts`):** Agents must drive the real harness (`opencode`, `codex app-server`, `senpi`) in isolated XDG/`CODEX_HOME`/`SENPI_CODING_AGENT_DIR` sandboxes, prove real user configs (`~/.codex/config.toml`, `opencode.db`) were untouched (via shasum / SQLite `SELECT count(*) FROM session` before & after), save captures to gitignored `.omo/evidence/<YYYYMMDD>-<slug>/`, paste decisive excerpts + `sha256sum` lines in the PR body — and CI **fails the build** if any evidence file is ever committed!
  2. **Root hermetic-test & temp-leak guards:** Ships dedicated meta-tests (`test-hermetic-home.test.ts`, `test-hermetic-home-teardown.test.ts`, `test-temp-leak-match.test.ts`, `test-temp-root.test.ts`, `test-git-environment.test.ts`) preventing tests from writing to real `$HOME` or leaking temp directories.
  3. **Strict `.oxlintrc.json` + `lint-ratchet`:** Unconditional 3-minute `lint-ratchet` job runs on *every* CI event regardless of docs/web fast-paths, requiring tracked file debt counts to match or drop below the committed baseline. Custom `./script/oxlint/biome-ports.ts` ports Biome rules into `oxlint`, paired with `typescript/no-explicit-any`, `no-non-null-assertion`, `ban-ts-comment`, and `knip`.
- **48 GitHub workflows (`ci.yml` alone is 1,905 lines / 91.8 KB!):**
  - **Measured p95×2 job timeouts** (commented with exact measurement date & PR `#14573`) so regressions fail loudly instead of creeping.
  - **Cost-guarded `ci:full-matrix` label (`ci-full-matrix-label.yml` + `pr-platform-decision.yml`):** Refuses expensive macOS/Windows matrices in seconds on Linux unless platform paths changed or the PR body includes `Platform-reason: <why>`.
  - **Real installer integration testing (`get-worker-ci.yml`):** Runs `shellcheck` on `install.sh`, `PSScriptAnalyzer` on `install.ps1`, installs twice into an isolated `HOME` (proving idempotency and single `.bashrc` block), and tests fallback to GitHub Releases when the mirror domain is unreachable (`OMO_INSTALL_BASE_URL=https://get.omo.invalid`).
  - **Workflow linting (`lint-workflows.yml`):** Runs pinned `actionlint` on every workflow edit, plus `npm-dist-tag-rollback.yml`, `windows-flake-soak.yml`, `trust-mutations.yml`, and `review-claims.yml`.

## 3. Architectural Bets & Craft
- **From OpenCode plugin → multi-harness Agent OS on a Pi fork (`senpi`):** Originally `oh-my-opencode`, now mid-refactor into 20 pure-TS Core packages + 4 MCP servers (`lsp-tools-mcp`, `git-bash-mcp`, `lsp-daemon`, `ast-grep-mcp`) + adapters for OpenCode (`omo-opencode`), Codex CLI (`omo-codex` / `lazycodex`), and its own `pi-mono` fork (`omo-senpi` / `omo-native` + `senpi-task` DAG engine) + 23 Rust crates for cross-OS GUI/computer-use automation.
- **Zero-copy third-party skill provenance via git submodules:** Brand/UI references live *only* as pinned git submodules under `packages/shared-skills/upstreams/` and are materialized into gitignored paths at build time (non-fatal offline), keeping third-party assets out of git history.
- **Exact-pinned Rust workspace dependencies (`Cargo.toml`):** Every crate dependency uses `=x.y.z` exact pins (e.g., `serde = "=1.0.229"`, `tokio = "=1.53.1"`), paired with `proptest` and explicit `fake` desktop backends for headless testing.

## 4. Commit, PR & Maintenance Reality
- **Extreme solo-driver + multi-worktree velocity:** **50 commits in 19.2 hours** (`2026-11-24T14:29Z` to `2026-11-25T09:40Z`, PR `#14,924`), **52% conventional**, **8% fix/revert**, **0% AI co-author trailer** (though `sisyphus-dev-ai` has 680 and `MoerAI` has 575 all-time contributions).
- **Astonishing single-account concentration:** **`code-yeongyu` has `31,010` all-time contributions and `50 of the last 50 commits`**, landing parallel worktree branches (`wt/14920-consent-b`, `wt/14920-telemetry-a`, `train/thread-11`) via **merge commits** (explicitly banning squash/rebase merges in `AGENTS.md`).
- **Visible bundle/golden churn:** Several recent commits are pure bundle regenerations (`chore(senpi): regenerate the plugin bundles`, `chore: restore dev's generated extension bytes`) and golden re-recordings — a classic tax of checking generated plugin bundles into git alongside 45 packages.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Local-only `.omo/evidence/` + `sha256sum` PR proof + `tracked-evidence-paths-audit.test.ts`** — solves the "prove real-surface QA without bloating git with screenshots/logs" problem cleanly.
  2. **Hermetic `$HOME` & temp-leak meta-tests** (`test-hermetic-home.test.ts`, `test-temp-leak-match.test.ts`) + before/after shasum assertions proving QA never mutated real user config.
  3. **Idempotent + fallback-tested installer CI (`get-worker-ci.yml`)** with `shellcheck` + `PSScriptAnalyzer` + unreachable-mirror test.
  4. **Unconditional `lint-ratchet` job + p95×2 measured CI timeouts + `Platform-reason:` cost gate** for expensive macOS/Windows runners.
  5. **One cross-harness `script/agent/setup.sh`** wired into Dev Containers, Claude Code, Codex, and Cursor hooks.
- **Avoid:**
  1. **70.8 KB ALL-CAPS profanity-laden `AGENTS.md` (duplicated in `CLAUDE.md`)** — burns tens of thousands of tokens per session, drifts within months (`Generated: 2026-08-24`), and proves that shouting in prompts is a weak substitute for compact routing + mechanical gates.
  2. **1,905-line single `ci.yml` + 45 packages + 23 Rust crates + 6 `bunfig.*.toml` shard configs** under one person's `dev` branch — extreme cognitive and merge-bundle tax.
  3. **Committing generated plugin bundles into git** — causes constant regeneration churn on every parallel worktree PR.
