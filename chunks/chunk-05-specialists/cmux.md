# cmux (`manaflow-ai/cmux`)

- **Snapshot:** `28,958★` · `2,707` forks · **`11,218` open issues** · Dual-licensed (`GPL-3.0-or-later` app + `BSL` server directories; GitHub meta `NOASSERTION`) · Hyper-active (created Jan 28, 2026; pushed 2026-11-25)
- **Primary Stack:** Massive polyglot monorepo: **115.2 MB Swift** (macOS/iOS app built on a `manaflow-ai/ghostty` fork) + **21.8 MB Python** (CI/verification automation) + **21.3 MB Rust** (`cmux-cua` engine, relays, TUI) + **20.2 MB TypeScript** (`web/`, `webviews/`, Cloudflare Workers) + 3.9 MB Shell + 2.1 MB Java + 2.1 MB C++ + 1.7 MB Go + 1.2 MB Zig; Xcode 26, Biome 2.5, Bun, CodeRabbit + Greptile + Cursor Bugbot.
- **Data source:** [`data/chunk-05/manaflow-ai__cmux.json`](../../data/chunk-05/manaflow-ai__cmux.json)

## 1. Agent Instruction & Docs Hygiene
- **Disciplined, high-signal 111-line `AGENTS.md` (8.2 KB)** with a sharp routing table mapping task areas to skills (`cmux-debugging`, `cmux-architecture`, `cmux-ghostty`, `cmux-localization`, `cmux-keyboard-shortcuts`, `cmux-testing`, `cmux-shared-behavior`, `cmux-review`, `cmux-socket-policy`), nested `AGENTS.md` pointers (`ios/`, `web/`, `cmux-tui/`), `STYLE.md`, and **120 `docs/`**.
- **`REVIEW.md` (institutional memory of review catches):** Explicitly instructs agents *"Before opening a PR and before merging, check it against `REVIEW.md`, the mistakes our review history keeps catching."*
- **Process & self-preservation safety:** Forbids quitting, killing, relaunching, or profiling the user's live `/Applications/cmux.app` (`com.cmuxterm.app`), mandating tagged builds (`reload.sh --tag <tag>`) and `CMUX_TAG=<tag> scripts/cmux-debug-cli.sh`.
- **Dual-license / CLA agent guardrail:** Explicitly lists BSL-licensed server paths (`web/`, `workers/ci-artifacts/`, `workers/iroh-v2/`, `workers/presence/`, `services/iroh-relay-minter/`, `cmux-tui/relays/cloudflare-do/`) and forbids agents from merging while CLA Assistant is red or copying outside contributor code there without a signed CLA.
- **Minor flaws:** `CLAUDE.md` is a byte-for-byte duplicate of `AGENTS.md`, and root contains stray audit/report artifacts (`PR-10599-AUDIT.md`, `cx-ci-failfast.report.md`, `reports.md`, `TODO.md`) plus private `cmuxterm-hq` links that 404 for external contributors.

## 2. Mechanical Gates & Quality Control
- **231 GitHub Actions workflows — the largest CI surface in the entire 35-repo study (nearly 2× OpenClaw's 133):**
  - Spans owned macOS Mac mini pools + GCP JIT x64 runners + Blacksmith overflow + R2 binary/cache pruning + nightly rollback drills (`nightly-next-rollback-drill.yml`) + production synthetic canaries (`cloud-journey-prod.yml`, `real-login-canaries.yml`) + `required-checks-drift.yml` + `language-boundaries.yml`.
- **Standout mechanical innovations worth studying:**
  1. **`scripts/verify-local.py` with diff-scoped static checks + JSON `--receipt -`:** Compares against local `upstream/HEAD` without fetching, runs only touched checks (localization, Xcode/test wiring, feature flags, Swift parse), prints exact `--only` rerun commands on failure, and emits machine-readable verification receipts.
  2. **`app-host-test-rerun.yml` (compiled-product adoption):** When a change only touches `cmuxTests/`, skips compiling the native macOS app entirely by adopting compiled app-host products from the nearest upstream CI run and recompiling only the test bundle (with optional `--baseline` before/after comparison!).
  3. **Self-healing CI (`red-autofix.yml`, `main-regression-bisect.yml`, `ci-queue-janitor.yml`):** Runs a *"fix-forward and revert race for every base and nightly red"* plus automated regression bisection.
  4. **Deny-by-default `RemoteRelayCommandPolicy`:** Any PR expanding remote v2 socket allowlists must include threat analysis (local command execution, unowned object access, ID scoping) and policy tests, or review is blocked.
  5. **Temporary `BASH_ENV` GitHub REST API-budget logger:** Tracks every `gh`/API call across workflows (self-expiring after a fixed date) so the CI fleet doesn't exhaust GitHub's hourly REST quota.
- **Radical autonomous-merge policy:** *"A PR merges when an independent review subagent passes its head and it causes no red of its own; base reds, flakes and pending checks don't hold it, and no person approves it. Merge with `gh-merge-green`."* Even allows `--override "<reason>"` to waive stuck or known-red checks!
- **Under-enforced web lint:** Root `biome.json` has `formatter.enabled: false` and `assist.enabled: false`; `CONTRIBUTING.md` admits *"do not wire this into required CI until the remaining source lint diagnostics are paid down."*

## 3. Architectural Bets & Craft
- **Native Ghostty-based macOS terminal turned full cloud+mobile+multi-SDK platform:** Started as a Ghostty-powered macOS terminal multiplexer for coding agents, then expanded into iOS, a TUI, a web app, Cloudflare/iroh relays, Rust computer-use (`cmux-cua`), a `coderouter`, cloud VMs, and 5 language SDKs (npm, PyPI, crates.io, Go, Java) — all inside one 190 MB polyglot repo.
- **Reproduce-first bug-fix protocol:** Mandates committing the failing behavioral regression *before* its fix, naming the exact red/green command in the PR body, and adding an `### Observed / Not run` disclosure section.

## 4. Commit, PR & Maintenance Reality
- **Extreme autonomous-agent throughput — and the clearest warning about CI-factory self-consumption:**
  - **50 commits in 9.7 hours** (`2026-11-25T03:26Z` to `13:10Z`), PR **`#56,611` in just 10 months**, **100% AI co-author signal**, 40% conventional, 2% fix/revert.
  - `teamleaderleo` authored **49 of the last 50 commits** (all-time top: `lawrencecchen` 7,790, `austinywang` 7,585, `teamleaderleo` 2,964, `azooz2003-bit` 1,871).
  - **Crucial observation from the commit log:** Roughly **17 of the 20 sampled commits** on `main` are **maintaining the CI/runner/nightly/autofix machinery itself** (`red-autofix`, `pr_runner_pool`, `nightly picker`, `CI attribution`, `namespace autofix`, `auto-journey.yml`, `pr-media`, `cloud-journey-prod`), rather than shipping terminal features!
  - Meanwhile, **open items have exploded to `11,218`** (the 2nd highest open count in the 35-repo study behind `openai/codex`, despite having 1/5th the stars).

## 5. Steal vs. Avoid
- **Steal:**
  1. **`REVIEW.md` ("mistakes our review history keeps catching")** — a compact, living pre-PR self-audit checklist distilled from real review catches.
  2. **`scripts/verify-local.py` with `--receipt -` JSON receipts + exact `--only` rerun commands** — turns local verification into structured, auditable proof.
  3. **`### Observed / Not run` PR disclosure section** + explicit reminder that *"a skipped job is green and is not coverage."*
  4. **Compiled-artifact adoption for test-only reruns** (`app-host-test-rerun.yml`) for heavy native builds.
  5. **Deny-by-default remote command policy (`RemoteRelayCommandPolicy`)** requiring explicit threat-model proof for every new allowlist entry.
- **Avoid:**
  1. **231 GitHub Actions workflows + bespoke multi-cloud runner fleets + self-modifying autofix loops** — once your CI factory consumes 80%+ of daily commits just keeping itself green, the automation owns the team.
  2. **Zero-human-approval autonomous merging with `--override` waivers on a red `main`** — maximizes PR merge count (`#56,611`), but compounds flakiness, reverts, and `11,218` unresolved user issues.
  3. **Expanding a single-purpose native tool into 7 languages, 5 SDKs, cloud VMs, and a custom relay inside one repo** before taming core stability.
