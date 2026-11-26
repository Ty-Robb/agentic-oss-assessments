# Happy (`slopus/happy`)

- **Snapshot:** `24,822★` · `2,139` forks · `1,154` open issues · `MIT` · Active (created Jul 18, 2025; pushed 2026-11-25)
- **Primary Stack:** **22.3 MB Swift** (native UIKit iOS app) + **14.6 MB Kotlin** (native Jetpack Compose Android app) + **3.2 MB TypeScript** (`happy-cli`, `happy-server` relay, `happy-wire`, Cloudflare Worker `happy-push-server`) + 628 KB Rust + **23.5 KB Lean**; pnpm 10 (`onlyBuiltDependencies`), Prisma/SQLite. Desktop (`slopus/happy-desktop`) and agent runtime (`slopus/happy-agent`) live in separate repos.
- **Data source:** [`data/chunk-05/slopus__happy.json`](../../data/chunk-05/slopus__happy.json)

## 1. Agent Instruction & Docs Hygiene
- **Ultra-lean, incident-scarred `AGENTS.md` (40 lines / 1.7 KB):** Contains just three sharp operational rules — zero fluff, zero architecture essay:
  1. **Release safety rule citing an exact production incident:** *"Release from a local `main` that is exactly `origin/main`, checked against a fetch made right then, with a clean tree. Not from a worktree. Not from a branch... Why: an OTA channel serves whatever was published last, not whatever is on `main`. On 2026-09-20 a preview OTA from a stale worktree silently rolled four shipped fixes off every preview phone for hours. Git looked fine the whole time."*
  2. **Hard ban on unapproved CI:** *"Never create or add GitHub Actions workflows, or add automatic triggers (`push`, `pull_request`, `schedule`) to existing ones, without an explicit user instruction. Actions minutes cost real money."*
  3. **Exact definition of colloquial team shorthand:** Defines `sync to main` (including the founder's typo `synt to main`!) as fetch → rebase on `origin/main` → `git push origin HEAD:main` (never force-push).
- **Focused `.agents/skills/` (9 skills) & 31 `docs/`:** Operational procedures live in skills (`release`, `dev`, `maintain`, `agent-browser`, `terminal-emulator`, `metrics-graphana`, `sessions`, `control-flow`, `office-hours`), while architecture specs live in `docs/` (`encryption.md`, `protocol.md`, `realtime-sync-and-rpc.md`, `chat-list-scrolling.md`, `permission-resolution.md`, `analytics-catalog.json`).

## 2. Mechanical Gates & Quality Control
- **Only 1 GitHub Actions workflow (`release-happy-cli.yml`) in the entire repo:** The most extreme anti-CI-bloat stance in the 35-repo study (contrast `cmux`'s 231 workflows and `openclaw`'s 133). There is **no automated PR test/lint workflow** in `slopus/happy`; quality relies on local developer/agent verification, release skills, and tight two-maintainer ownership.
- **Isolated local dev-environment harness (`package.json`):** Ships a first-class `packages/dev-environments` CLI (`pnpm env:new`, `env:up`, `env:up:authenticated`, `env:seed`, `env:server`, `env:cli`, `env:tailscale`, `env:down`) so agents and engineers spin up reproducible, authenticated local server+CLI stacks without touching production state.
- **Supply-chain hygiene:** Uses pnpm 10 `onlyBuiltDependencies` (`@prisma/client`, `better-sqlite3`, `esbuild`, `sharp`, `workerd`), explicit `pnpm.overrides`, and a small `Lean` formalization (23.5 KB) in the repo.

## 3. Architectural Bets & Craft
- **Boldest mobile engineering reversal in the study — abandoned Expo/EAS for pure native Swift (UIKit) + Kotlin (Jetpack Compose):**
  - `AGENTS.md` explicitly records: *"The former Expo/EAS app and OTA scripts have been removed; mobile clients are native iOS and Android."*
  - Replaced Expo's push service with a dedicated Cloudflare Worker (`packages/happy-push-server`) talking directly to APNs/FCM, while sharing JSON translations in `packages/happy-i18n` and wire contracts in `packages/happy-wire`.
  - Judging by the README badges (**4.9★ on iOS App Store, 5.0★ from 3.1k+ Google Play reviews**), native mobile craft is Happy's signature differentiator.
- **End-to-end encrypted multiplayer sessions:** Wraps Claude Code, Codex, Grok, Gemini (Antigravity), OpenCode, and ACP agents; encrypts everything traversing the relay (`happy-server`); supports live multi-user session steering.
- **Multi-repo split by surface:** Keeps mobile+CLI+relay (`slopus/happy`) separate from Electron desktop (`slopus/happy-desktop`) and agent runtime (`slopus/happy-agent`) — avoiding the 475 MB monorepo CI blast radius, at the cost of cross-repo coordination.

## 4. Commit, PR & Maintenance Reality
- **Steady, high-craft 2-person velocity:** **50 commits in 8.4 days** (`2026-11-17` to `2026-11-25`), **40% conventional commits**, **20% fix/revert**, **4% AI signal**.
- **Ultra-tight core team:** `ex3ndr` (**2,841** all-time; 13/50 recent) and `bra1nDump` (**1,474** all-time; 35/50 recent) account for **48 of the last 50 commits**, routinely landing paired `feat(ios):` and `feat(android):` commits within minutes of each other (e.g., `e6ede672` + `4daae8f8`, `10fd4240` + `57f31af2`), plus security hardening commits (`a4bada8b`, `8f935dfa`, `51312b7e`).
- **Backlog:** `1,154` open issues across mobile, CLI, and server — manageable for 24.8k★, though without PR CI gates outside contributors have no automated feedback loop.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Incident-cited release invariant (`main == origin/main`, clean tree, never from a worktree)** — prevents stale-worktree releases from silently rolling back production fixes.
  2. **Explicit CI-cost guardrail in `AGENTS.md`** forbidding agents from creating ad-hoc GitHub Actions workflows or triggers without approval.
  3. **`pnpm env:up --template authenticated-empty` + `env:seed` + `env:tailscale`** — disposable, templated local environments built as a first-class repo CLI.
  4. **Encoding team shorthand (even typos like `synt to main`)** directly into `AGENTS.md` so agents execute exact, safe git flows instead of guessing.
- **Avoid:**
  1. **Zero PR CI workflows** — viable only for a tiny, high-trust 2-person core pushing directly to `main`; breaks down the moment multiple engineers or autonomous PR agents contribute concurrently.
  2. **Splitting tightly coupled wire/client/desktop repos too early** unless each surface has an independent release cadence and dedicated owner.
