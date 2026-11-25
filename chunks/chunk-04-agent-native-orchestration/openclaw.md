# OpenClaw (`openclaw/openclaw`)

- **Snapshot:** `395,184★` · `82,972` forks · `9,182` open issues · `MIT` · Active (OpenClaw Foundation 501(c)(3); created Nov 24, 2025; pushed 2026-11-25)
- **Primary Stack:** Massive multi-platform monorepo (**474.7 MB TypeScript**, 23.1 MB Swift, 14.2 MB JS, 10.2 MB Kotlin, 2.2 MB Rust, 1.4 MB Python), pnpm isolated linker + APFS clone installs, `oxlint` + `oxfmt`, Vitest, Kysely (SQLite + Postgres), SolidJS Control UI, native macOS/iOS/Android/Windows/Linux companions, 20+ messaging channels.
- **Data source:** [`data/chunk-04/openclaw__openclaw.json`](../../data/chunk-04/openclaw__openclaw.json)

## 1. Agent Instruction & Docs Hygiene
- **Hard-budgeted, battle-scarred `AGENTS.md` (123 dense lines / 19.7 KB):** Explicitly capped under 20,000 characters (*"the size OpenClaw loads whole"*) with a strict anti-bloat rule: **"A new rule cites an incident."**
- **Best anti-overengineering manifesto in the study (`Choose good compromises`):**
  - Directly counters LLM tendencies to invent theoretical complexity: *"Use cheap mechanisms: idempotency key, one check, retry, best-effort record with a warning. Fencing tokens, revocation generations, multi-phase admission, nonce-matched settlement and cross-thread handshakes need buy-in."*
  - *"Name an accepted edge case in a comment or the PR. Do not write code for it. A rare, visible, recoverable fault is better than permanent complexity."*
  - *"Delete before batching, cache last."*
- **55 `.agents/skills/`** covering every recurring operational loop (`pr-simplify`, `autoreview`, `claw-score`, `clawsweeper`, `openclaw-test-heap-leaks`, `openclaw-performance`, `security-triage`, `proof-video`, `telegram-e2e-userbot`, `discord-e2e`, `slack-e2e`, `control-ui-e2e`).
- **One owner, complete cutover:** Mandates tracing and removing retired paths/wrappers/tests/docs in the same PR so competing implementations never linger.

## 2. Mechanical Gates & Quality Control
- **Strictest TypeScript `.oxlintrc.json` in the entire 23-repo study (557 lines):**
  - Sets all three categories — **`correctness`, `perf`, and `suspicious` — to `"error"`**.
  - Enforces `typescript/no-explicit-any: "error"`, `no-floating-promises: "error"`, `no-misused-promises: "error"`, `switch-exhaustiveness-check: "error"`, `oxc/no-accumulating-spread: "error"`, `oxc/no-async-endpoint-handlers: "error"`, `eslint/no-warning-comments: "error"`, and custom JS boundary rules (`scripts/oxlint-boundary-guards.mjs`, e.g., `openclaw-boundaries/no-recursive-readdir`).
- **Prompt-prefix KV-cache stability test:** `src/agents/agent-tools.prefix-stability.test.ts` mechanically guarantees that system prompts and tool definitions remain deterministic across turns so provider prompt caching never silently busts!
- **Industrial-grade supply-chain hardening (`pnpm-workspace.yaml`):**
  - `minimumReleaseAge: 10080` (7 days) + `minimumReleaseAgeStrict: true` + `blockExoticSubdeps: true`, with **dated expiration comments** on every single temporary exemption (`# remove after 2026-11-30...`).
  - `nodeLinker: isolated` + `packageImportMethod: clone-or-copy` + `verifyDepsBeforeRun: false` (prevents sibling worktrees from mutating shared `node_modules` or compiler `ctime`s).
- **133 GitHub workflows** covering everything from `opengrep-precise` SAST and CodeQL (Android/macOS/critical) to `ios-periphery` / `macos-periphery` dead-Swift checks, `dated-todo-sweep.yml`, `maturity-scorecard.yml`, `real-behavior-proof.yml`, `mantis-*-proof.yml` channel E2Es, and `ci-boat-recovery.yml` (auto-retrying quota-only runner setup failures with `zizmor` security audit annotations).
- **PR governance:** Hard cap of **20 open PRs per author** (`r: too-many-prs`), bans refactor-only PRs and test/CI-only PRs chasing known `main` failures, and routes features to third-party plugins via `openclaw/plugin-sdk/*`.

## 3. Architectural Bets & Craft
- **Trusted gateway + untrusted execution + plugin SDK:** Local Gateway owns state/sessions/credentials; models, agent harnesses (Pi, Claude, Codex, local), and 20+ messaging channels plug in via documented `openclaw/plugin-sdk/*` contracts (no core internal imports allowed).
- **Zero-trust cache key discipline:** Mandates keying every cache/memo/in-flight join by *all* inputs affecting the answer (agent, account, credential, session, workspace, mode, deadline) and proving isolation with interleaved work-count tests.
- **Egress-only log redaction:** Logs write raw structured data and redact only at egress (`logs.tail`, support bundles, OTel export), while banning logging message/tool contents.

## 4. Commit, PR & Maintenance Reality
- **Unprecedented OSS velocity:** **50 commits in 2 hours 20 minutes** (PR `#205,351` in just 12 months of repo existence!!), **98% conventional commits**, **64% fix/revert**, **8% AI trailer** (explicitly bans agent-attribution trailers in `AGENTS.md`: *"verified human credit, no agent-attribution trailers"* — even while `roboclaw-bot` has 3,873 commits and `openclaw-mantis[bot]` has 1,001!).
- **Hyper-prolific leadership:** Founder `steipete` (Peter Steinberger) has **70,042 contributions**, followed by `vincentkoc` (17,667), `shakkernerd` (5,208), `obviyus` (3,595).

## 5. Steal vs. Avoid
- **Steal:**
  1. **"A new rule cites an incident" + "Choose good compromises"** — the single best antidote to both `AGENTS.md` bloat and LLM over-engineering.
  2. **Strict `oxlint` triad (`correctness`, `perf`, `suspicious` = `"error"`)** + `no-floating-promises` + `switch-exhaustiveness-check`.
  3. **Prompt-prefix stability tests** (`prefix-stability.test.ts`) for any agentic app relying on LLM prompt caching.
  4. **Dated expiry comments on `minimumReleaseAgeExclude`** in `pnpm-workspace.yaml` + `dated-todo-sweep.yml`.
  5. **`pr-simplify` pre-PR self-review skill** and **dead-code checks across native codebases** (`periphery` for Swift).
- **Avoid:**
  1. **133 GitHub workflows & 158 KB root `package.json`** — necessary at 395k-star multi-OS scale, catastrophic maintenance overhead for a normal product team.
  2. **25+ `.mjs`/`.d.mts` bootstrap files scattered across the repo root** (cleaner under `bin/` or `runtime/`).
