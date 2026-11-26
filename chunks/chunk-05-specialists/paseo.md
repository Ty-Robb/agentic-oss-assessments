# Paseo (`getpaseo/paseo`)

- **Snapshot:** `25,293★` · `3,140` forks · `2,203` open issues · `Apache-2.0` (`package.json`, GitHub meta `NOASSERTION`) · Active (created Oct 13, 2025; pushed 2026-11-25)
- **Primary Stack:** **51.2 MB TypeScript** + 1.1 MB Kotlin + 852 KB Objective-C + 823 KB C++ + 542 KB Objective-C++ + 76 KB Swift; npm workspaces (`server` daemon, Expo mobile+web `app`, Electron `desktop`, `cli`, Cloudflare/Noise NK E2EE `relay`, `protocol`, `client`, `plugins`, `website`), `oxlint` + `oxfmt`, Vitest, `knip`, Lefthook, Nix flake + Fastlane + F-Droid.
- **Data source:** [`data/chunk-05/getpaseo__paseo.json`](../../data/chunk-05/getpaseo__paseo.json)

## 1. Agent Instruction & Docs Hygiene
- **Best docs-governance and anti-LLM-slop writing standard in the entire 36-repo study:**
  - `AGENTS.md` (205 lines / 24 KB) indexes **54 single-subject docs** in `docs/` and declares: *"The docs, check the docs, or check the X docs always mean this directory — not the web."*
  - **`Writing docs` rules:** *Integrate, don't append* (explicitly calls out `docs/custom-providers.md` as an anti-example of append-only drift); *Don't document logic*; *One fact, one doc*; *Respect the layers*; *One subject per doc*; *Delete obsolete sections*.
  - **`Doc voice` (explicit LLM cliché ban):** Forbids `"It's not X, it's Y"` setup-and-punchline prose, filler importance clauses (`"and that matters"`, `"this is critical"`), buzzwords (`"honest"`, `"robust"`, `"seamless"`, `"powerful"`, `"simply"`, `"just"`, `"delightful"`), hedging (`"generally"`, `"typically"`), and throat-clearing (`"It's worth noting that"`, `"In order to"`).
- **Safe self-hosting boundary:** Dev commands automatically bind `PASEO_HOME` to checkout-local `.dev/paseo-home` on `127.0.0.1:6768`, leaving the live `~/.paseo` daemon on port `6767` untouched, with a crisp rule: *"NEVER restart the main Paseo daemon on port 6767 without permission — if you're an agent, restarting it kills your own process."*
- **Minor hygiene flaw:** `CLAUDE.md` is a **byte-for-byte 24,042-byte duplicate** of `AGENTS.md` (both even start with `# CLAUDE.md`) rather than a symlink.

## 2. Mechanical Gates & Quality Control
- **Strict `.oxlintrc.json` (632 lines) with custom JS plugin + file-and-API-scoped debt ratchets:**
  - Sets `correctness`, `suspicious`, and `perf` to `"error"`, plus `complexity: max 20`, `max-depth: 4`, `max-nested-callbacks: 3`, `react-perf/jsx-no-new-{array,function,object}-as-prop`, `typescript/no-explicit-any`, and `preserve-caught-error`.
  - Custom `scripts/oxlint/paseo-plugin.mjs` enforces `paseo/no-sync-io` on `packages/server/src/**`, with **per-file, per-API allowlists** (`"server/agent/providers/pi/agent.ts": ["existsSync", "mkdtempSync", ...]`) annotated with `TODO:` migration plans — *"new APIs still fail in these files. Do not add directory-wide exceptions."*
  - **Unit-tests its own lint rules and CI contracts in CI:** `node --test scripts/oxlint/paseo-plugin.test.mjs` and **10 CI/release contract test suites** (`scripts/ci-workflow.test.mjs`, `daemon-launch-contract.test.mjs`, `reconcile-release.test.mjs`, etc.) run right inside the fast `changes` job!
- **Only 12 GitHub workflows** covering desktop, iOS, Android/F-Droid, Docker, Nix, relay, and website.
  - `ci.yml` uses `dorny/paths-filter` (`.github/ci-paths.yml`) and explicit step conditions (`!cancelled() && steps.install.outcome == 'success'`) so independent domains still report failures without masking errors behind `continue-on-error`.
  - Runs `lockfile-lint --allowed-hosts npm --validate-https --validate-integrity`, `knip`, `oxfmt --check`, `acp:version-drift:check`, and `fdroid:changelogs:check`.
- **Anti-slop PR gate (`CONTRIBUTING.md`):** **"Pull requests are closed by default."** *"I can prompt an agent to write code just as you can. The bottlenecks are choosing what to build, shaping it, verifying its behavior, and taking responsibility for its maintenance."* Caps core PRs at ~3,000 production lines and requires explicit QA evidence (`docs/qa.md` — failing-before regression test, commands + output, UI recording/screenshots, platform matrix).

## 3. Architectural Bets & Craft
- **Daemon-owned, client-thin multi-surface architecture:** Local daemon (`packages/server`) manages all agents (Claude Code, Codex, Copilot, OpenCode, Pi, Antigravity, Muse Code, fx, Hoplite), plugins, and file-based JSON state (atomic writes, Zod schemas, no DB migrations). Clients (Expo mobile+web, Electron, CLI) talk over dotted-namespace WebSocket RPCs validated via **`zod-aot`** compiled inbound validators (`docs/protocol-validation.md`) and version-drift `COMPAT` gating (`docs/protocol-compatibility.md`).
- **Write-once daemon plugins that project to mobile:** Plugins declare UI (screens, sidebar items, composer pills, timeline items, themes), lifecycle hooks, and custom providers once on the daemon and render natively across desktop, web, iOS, and Android.
- **Privacy-first E2EE remote access:** Optional Noise NK end-to-end encrypted relay (`packages/relay`), zero telemetry, no forced login, plus F-Droid reproducible Android source builds.

## 4. Commit, PR & Maintenance Reality
- **High solo-founder + bot cadence:** **50 commits in 57.2 hours (~2.4 days)** (`2026-11-23` to `2026-11-25`, PR `#10,800`), **44% conventional commits**, **26% fix/revert**, **28% AI signal**.
- **Human + autonomous maintenance bot pair:** Founder `boudra` (Mohamed Boudra) holds **5,406 all-time contributions** (33/50 recent), backed by `paseo-bot[bot]` (**779 all-time; 15/50 recent** — landing focused bugfixes and flaky-test stabilization PRs like `#10762`, `#10516`, `#10602`).

## 5. Steal vs. Avoid
- **Steal:**
  1. **The `Doc voice` LLM cliché ban + `Writing docs` rules** — immediately eliminates bloated, puffery-filled agent documentation.
  2. **Per-file, per-API lint debt allowlists** (`paseo/no-sync-io` naming exact functions per file instead of directory-wide disables) + unit tests for custom lint rules and CI scripts.
  3. **Checkout-local `.dev/<app>-home`** isolating dev daemons and CLIs from the developer's live `~/.app` install automatically.
  4. **"PRs closed by default" + 3,000-line cap + QA evidence bar** for solo/small-team open-source maintainers facing AI PR floods.
  5. **`lockfile-lint`** verifying npm lockfile integrity and HTTPS-only allowed registries in CI.
- **Avoid:**
  1. **Duplicating `AGENTS.md` and `CLAUDE.md` as separate 24 KB files** — use a symlink or thin wrapper so they cannot drift.
  2. **Re-building complex native text-selection/markdown/terminal layers inside Expo** unless mobile-first cross-platform parity is genuinely your core product (see `slopus/happy` for the opposite native bet).
