# Chunk 5 Summary — Mobile, Terminal & Guardrail Specialists

*Snapshot date: 2026-11-25. Combined stars in this chunk: **183,645★**.*

## Side-by-Side Matrix

| Repo | Stars | Open Issues | Primary Stack | `AGENTS.md` / Skills | Signature Mechanical Gate | CI Workflows | Last-50 Velocity & Hygiene |
| --- | ---: | ---: | --- | --- | --- | ---: | --- |
| **[`getpaseo/paseo`](paseo.md)** | 25.3k | 2,203 | TS (51.2 MB) + Expo/Electron + Noise NK E2EE relay + plugins | 205-line `AGENTS.md` + **54 subject docs** + anti-slop `Doc voice` + 2 skills | `.oxlintrc.json` (632 lines) + per-file/per-API `paseo/no-sync-io` debt allowlist + unit-tested lint/CI contracts + `lockfile-lint` + "PRs closed by default" | 12 | 50 commits / **2.4 days** · 44% conv · 26% fix · 28% AI (`paseo-bot[bot]` = 15/50) |
| **[`slopus/happy`](happy.md)** | 24.8k | 1,154 | **Native Swift UIKit (22.3 MB) + Kotlin Compose (14.6 MB)** + TS CLI/relay + Lean | 40-line incident-cited `AGENTS.md` + 9 skills + 31 docs | Local `pnpm env:up/seed/tailscale` dev harness + `release` skill (`main == origin/main`) + **explicit ban on adding CI** | **1** | 50 commits / **8.4 days** · 40% conv · 20% fix · 4% AI (2-person core = 48/50) |
| **[`manaflow-ai/cmux`](cmux.md)** | 29.0k | **11,218** | **Swift (115.2 MB)** + Python (21.8 MB) + Rust (21.3 MB) + TS (20.2 MB) + Ghostty | 111-line `AGENTS.md` + **`REVIEW.md`** + 120 docs + task skills | `scripts/verify-local.py` (`--receipt -`), `app-host-test-rerun.yml` (compiled-product reuse), `red-autofix.yml`, deny-by-default `RemoteRelayCommandPolicy`, autonomous `gh-merge-green` | **231** | 50 commits / **9.7 hrs** · 40% conv · 2% fix · **100% AI** (`teamleaderleo` = 49/50, mostly CI maintenance!) |
| **[`smtg-ai/claude-squad`](claude-squad.md)** | 8.9k | **54** | **263 KB Go** (Bubble Tea) + `tmux` + `git worktree` + `gh` | None (162-line README) | `golangci-lint --only-new-issues` + `gofmt` + GoReleaser | 5 | 50 commits / **17 mos** · 82% conv · 36% fix · 16% AI |
| **[`stackblitz-labs/bolt.diy`](bolt-diy.md)** | 20.1k | **2** | TS (3.4 MB), React Router + WebContainers + AI SDK + Electron + CF Workers | None (260-line `CONTRIBUTING.md`) | Prod Docker build + `curl` smoke test in CI, `.performance-budgets.json` + Lighthouse CI, fork-safe CF preview | 13 | 50 commits / **5.3 days** · 34% conv · 6% fix · 0% AI (**Bus factor 1**: `dustinwloring1988` = 50/50) |
| **[`code-yeongyu/oh-my-openagent`](oh-my-openagent.md)** | 71.1k | 2,823 | TS (58.0 MB) + Rust (5.3 MB), **45 pkgs + 23 crates**, `senpi` (Pi fork), Bun | **70.8 KB / 479-line ALL-CAPS `AGENTS.md`** + 14 skills | Local-only `.omo/evidence/` + `sha256sum` PR proof + `tracked-evidence-paths-audit.test.ts`, hermetic `$HOME`/temp-leak tests, unconditional `lint-ratchet`, `get-worker-ci.yml` installer tests | 48 | 50 commits / **19.2 hrs** · 52% conv · 8% fix · 0% AI (`code-yeongyu` = 50/50; 31k total!) |
| **[`zgsm-ai/costrict`](costrict.md)** | 4.5k | 14 | TS (15.1 MB) Roo Code enterprise fork, pnpm + Turbo, Docker evals | 6-line `AGENTS.md` (Roo invariant + English-only commits) | Docker Postgres+Redis `evals.yml`, `knip --include files`, 40+ `pnpm.overrides` CVE pins | 11 | 50 commits / **3.6 mos** (quiet since Sep 30) · **92% conv** · 14% fix · 2% AI (`mini2s` = 44/50) |

## Key Patterns Across Chunk 5

1. **The CI Inversion Paradox (`Happy` = 1 workflow vs. `cmux` = 231 workflows):**
   - Chunk 5 spans the entire spectrum of CI investment. `slopus/happy` explicitly bans GitHub Actions in `AGENTS.md` (*"Actions minutes cost real money"*) and ships top-rated native iOS/Android apps with 2 engineers. At the exact opposite extreme, `manaflow-ai/cmux` has **231 workflows** and a 100%-AI-assisted autonomous merge loop — where ~80% of recent commits on `main` are now spent repairing the CI/runner/autofix factory itself while open issues climb past `11,218`.
   - **`getpaseo/paseo` hits the sweet spot:** **12 workflows**, path-filtered CI, unit-tested lint/CI contracts, `lockfile-lint`, strict `oxlint` with per-file/per-API debt allowlists, and checkout-local `.dev/` state.

2. **Two opposite mobile bets — both validated by real engineering constraints:**
   - **`Paseo`** bets on Expo + Electron + daemon-driven plugins (write a plugin once, render it on desktop, web, iOS, and Android) and pays for deep subject docs (`unistyles.md`, `mobile-panels.md`, `native-text-selection.md`, `expo-router.md`) to tame React Native edge cases.
   - **`Happy`** tried Expo/EAS + OTA, got burned (including a stale-worktree OTA rollback incident), and ripped it all out for **pure native Swift UIKit + Kotlin Jetpack Compose** + a Cloudflare push worker.

3. **Three genuinely novel agent-verification inventions from Chunk 5:**
   - **Anti-LLM-slop `Doc voice` (`Paseo`):** Banning specific LLM rhetorical patterns (`"It's not X, it's Y"`, `"robust"`, `"seamless"`, `"that matters"`) right in `AGENTS.md` keeps internal docs crisp and durable.
   - **Uncommitted local QA evidence + `sha256sum` proof + anti-commit CI audit (`OmO`):** Forces real-surface, isolated-sandbox QA without polluting git with screenshots/logs — enforced mechanically by `tracked-evidence-paths-audit.test.ts` and hermetic `$HOME` tests.
   - **Structured local verification receipts + `REVIEW.md` (`cmux`):** `verify-local.py --receipt -` + a living `REVIEW.md` of recurring review catches + `### Observed / Not run` PR disclosures close the gap between "CI is green (because jobs were skipped)" and real proof.

4. **Prompt shouting fails; crisp invariants win:**
   - Contrast `oh-my-openagent`'s **70.8 KB ALL-CAPS `AGENTS.md`** (already 3 months stale on its own generated header) with `slopus/happy`'s **40-line incident-cited `AGENTS.md`**, `cmux`'s **111-line router + `REVIEW.md`**, and `costrict`'s **6-line file** (which drove 92% English conventional commits).
