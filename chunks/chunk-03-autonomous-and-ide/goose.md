# Goose (`aaif-goose/goose`, formerly `block/goose`)

- **Snapshot:** `56,978★` · `6,670` forks · **`512` open issues** · `Apache-2.0` · Active (Linux Foundation AAIF; pushed 2026-11-25)
- **Primary Stack:** Rust workspace (`oi-kit` reusable agent runtime + `goose` CLI/ACP backend, 11.1 MB Rust, `axum`, `rmcp`, `agent-client-protocol`, `candle` in-process local inference, `iroh` P2P relay, `tree-sitter`, OpenTelemetry) + Electron desktop UI (`ui/desktop`, 3.5 MB TS), `Justfile`, Hermit toolchain manager, Nix flake, `release-plz`.
- **Data source:** [`data/chunk-03/aaif-goose__goose.json`](../../data/chunk-03/aaif-goose__goose.json)

## 1. Agent Instruction & Docs Hygiene
- **Crisp 132-line `AGENTS.md` (6.2 KB) + 1-line `@AGENTS.md` `CLAUDE.md`:** Clearly encodes issue-board governance, exact cargo/just/UI commands, Rust simplicity rules (no redundant `.context("Failed to X")`, booleans default to `false` not `Option<bool>`, trust the Rust type system instead of defensive checks), and concrete OS traps (never overwrite a live macOS binary in place — unlink/atomic-rename or macOS SIGKILLs with `Code Signature Invalid`!).
- **Issue-first engineering culture (`CONTRIBUTING.md`):**
  - Every external PR must implement an issue already in **Ready** status on the public Goose Issues board; *"the unit of contribution is taking a problem to a verified solution, not writing the patch."*
  - Explicitly embraces AI-assisted contributions (*"You are contributing to an agent, it would be odd if you had not"*), requires addressing or rebutting every Codex AI code-review comment in one line, and coaches contributors on LLM failure modes (*"Think first"*, *"Spot the laziness"*).
- **Retiring custom registries in favor of standards:** Explicitly retiring its legacy `servers.json` MCP list in favor of the official MCP Registry and steering new LLM providers to user-installable JSON files rather than core PRs.

## 2. Mechanical Gates & Quality Control
- **Strong Rust + multi-target CI (39 workflows):**
  - `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo-deny`, `cargo-machete` (unused Cargo deps — Rust equivalent of `knip`), OpenSSF `scorecard.yml`, `quarantine.yml` (flaky test isolation).
  - **Binary size & Wasm budgets:** `just check-lean-size` enforces a size budget on the lean ACP binary, and `rust-check-wasm` verifies `oi-kit` crates compile & pass tests on `wasm32`.
  - **Protocol conformance suites:** `mcp-conformance.yml` and `model-toolcall-conformance.yml` test real protocol & tool-calling compliance.
  - **Release branch cherry-pick gate (`check-release-pr.yaml`):** Runs `git cherry origin/main HEAD` to prove every commit in a `release/*` PR already exists on `main`, preventing hotfixes from getting stranded on release branches.
- **Packed npm artifact verification (`ci.yml`):** Packs `goose-acp` tarballs and validates `package.json` versions inside the extracted `.tgz` before publish.

## 3. Architectural Bets & Craft
- **Foundation-grade SDK split inside one repo (`oi-kit` + `goose`):** Decomposed Goose's core agent loop into reusable `oi-kit` Rust crates (state machine, operations, providers, compaction, with Python/Kotlin bindings and `wasm32` support) while keeping `goose` as the flagship CLI/Desktop/ACP reference app.
- **ACP-native desktop architecture:** `goose Desktop` talks to its own backend over `goose acp` (Agent Client Protocol) — explicitly banning legacy OpenAPI client generation (`@hey-api/openapi-ts`) in `ui/desktop`.
- **In-process local inference (`candle`) + P2P networking (`iroh`):** Unusual, forward-looking bets inside the Rust core that avoid requiring Ollama or centralized relays.

## 4. Commit, PR & Maintenance Reality
- **Low open-issue count (512 on 57k★)** thanks to the **Ready**-board gate, `stale.yml`, and `take.yml`.
- **Important metric nuance in last 50 commits (5 days, 2026-11-20 to 2026-11-25):** 94% conventional commits, 16% fix/revert, and `64%` matched our bot/AI regex — **because 29 of the last 50 commits (58%) are auto-merged `dependabot[bot]` PRs** (`dependabot-auto-merge.yml`), while active human engineering in this window is heavily concentrated in `lifeizhou-ap` (13 commits) alongside broader Block/AAIF maintainers (`DOsinga`, `alexhancock`, `jamadeo`, `michaelneale`, `angiejones`).

## 5. Steal vs. Avoid
- **Steal:**
  1. **Board-gated `Ready` issue requirement:** Forces design alignment and a verification plan *before* anyone (or any agent) writes code.
  2. **`check-release-pr.yaml` (`git cherry origin/main HEAD`):** Tiny 60-line workflow guaranteeing release branches never diverge from `main`.
  3. **Binary size budget (`check-lean-size`) + `cargo-machete` + protocol conformance CI** (`mcp-conformance`, `model-toolcall-conformance`).
  4. **Mandatory 1-line disposition of AI review findings** (fix or write a 1-line reason why it's a false positive) — keeps automated review high-signal.
  5. **Dogfooding your own public protocol:** Desktop talking to backend over ACP guarantees ACP never rots.
- **Avoid:**
  1. **Unbundled Dependabot auto-merge storms** (29 separate bump commits in 5 days) — group Dependabot updates by ecosystem/minor to keep `git log` readable.
  2. **Root directory doc sprawl** (`BUILDING_DOCKER.md`, `BUILDING_LINUX.md`, `CUSTOM_DISTROS.md`, `I18N.md`, `MERGE_FIXES.md`, `RELEASE_CHECKLIST.md`, `RISCV_SETUP.md` all sitting at root).
