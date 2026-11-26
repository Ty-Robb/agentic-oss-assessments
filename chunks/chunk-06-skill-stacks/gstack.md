# gstack (`garrytan/gstack`)

- **Snapshot:** `142,644★` · `21,048` forks · **`45` open issues** · `MIT` · Hyper-active (created Mar 11, 2026; pushed 2026-11-25)
- **Primary Stack:** **45.1 MB TypeScript** + 2.1 MB Shell + 1.5 MB Go Template + 484 KB JS + Swift/C; Bun `1.4.2+`, TypeScript 7 (`7.0.2`), Playwright + Aside browser integration, compiled standalone CLIs (`browse`, `make-pdf`), Chrome extension, Docker CSO security scanners.
- **Data source:** [`data/chunk-06/garrytan__gstack.json`](../../data/chunk-06/garrytan__gstack.json)

## 1. Agent Instruction & Docs Hygiene
- **The most honest empirical self-eval in the entire 36-repo study (`README.md`):**
  > *"What it doesn't do: make your agent fix more bugs. In a November 2026 test on 100 everyday GitHub bugs and features, Claude Opus 5.5 fixed 58 with gstack installed and 61 of 99 without it (one task didn't score). So gstack gave no gain, and the test rules out a gain bigger than about 2 points on those tasks. On 60 security fixes, both fixed 29. Use gstack for the workflow, the reviews, the shipping steps and the safety guards, not for a higher fix rate."*
- **Heavy, deeply battle-scarred agent instructions:** Separate `AGENTS.md` (**18.6 KB / 275 lines** listing 60+ skills + a massive 9-point `Validation discipline`) AND `CLAUDE.md` (**35.5 KB / 631 lines**!) plus an 84.7 KB `CONTRIBUTING.md` and **82 `docs/`** — powerful operational rigor, but heavy token weight and split across two large root instruction files.
- **Template-generated `SKILL.md` discipline:** `SKILL.md` files are compiled from `.tmpl` sources (`bun run gen:skill-docs`), never edited directly; merge conflicts must be resolved on `.tmpl` and regenerated.
- **Built-in operational self-learning:** Sessions log failures/quirks to `~/.gstack/projects/{slug}/learnings.jsonl` and surface them automatically (`/learn`).

## 2. Mechanical Gates & Quality Control
- **38 GitHub Actions workflows** — far heavier than a "just Markdown" repo because gstack is actually a 45 MB TypeScript browser/PDF/CSO/eval platform:
  1. **Strict prompt & catalog token budgets:** `test/catalog-budget.test.ts` caps the always-loaded skill catalog at `2,292` token-equivalents; `test/context-budget-ratchet.test.ts` pins per-skill token ceilings against `test/fixtures/context-budget.json`.
  2. **Egress receipts enforced in CI (`test/egress-receipt-wiring.test.ts`):** Every off-machine send (`curl`, `git`, TS network calls) must write a local receipt *before* sending — CI fails on any unreceipted new network sink!
  3. **Scientific paid-eval discipline (`eval-sweep.yml`, `evals.yml`, `evals-periodic.yml`):**
     - Pre-registered trial counts before running (`rule`: 1 trial; `behavior`: 3-trial panel, pass ≥2/3; `judge`: 3-sample median) — *"Never add trials, samples or dispatches after seeing a result."*
     - Hard **$150/week USD spend cap** shared across 7 days of sweeps, digest-pinned GHCR CI images, diff-selected paid PR probes (`touchfiles.ts`), and detached SIGTERM-proof runners (`eval:bg:pr`).
  4. **Strict security & hygiene checks:** `typecheck:test` shrink-only ratchet, `test/spawnsync-timeout-tripwire.test.ts`, `bun run slop:diff`, digest-pinned `actionlint` Docker image (no repointable tags), `osv-scanner.yml`, `dependency-review.yml`, `mutation-report.yml`, and fail-closed attested CSO runtime promotions (`cso-runtime-promote.yml`).
  5. **Test-value bar (`docs/test-value-bar.md`):** Explicitly bans brittle prose-pinning tests on skill wording unless software parses the exact bytes or a recorded eval proves the wording matters.

## 3. Architectural Bets & Craft
- **Role-based startup factory + real browser/PDF binaries:** Pairs 60+ specialist slash commands (`/office-hours`, `/plan-ceo-review`, `/plan-eng-review`, `/review`, `/qa`, `/cso`, `/gstack-ship`, `/careful`, `/freeze`, `/guard`) with real compiled Bun binaries (`browse`, `make-pdf`), Aside browser automation with bundled headless fallback, and a Chrome extension.
- **Release channels (`stable` vs. `main`):** Defaults new installs to tagged `stable` releases (Mon/Thu) rather than raw `main`, while contributors and crew follow `main`.
- **Platform-agnostic project discovery:** Skills forbid hardcoding framework commands; they read project `CLAUDE.md`, ask once if missing, and persist the answer.

## 4. Commit, PR & Maintenance Reality
- **High-intensity solo-founder + AI factory:** **50 commits in 43.8 hours (~1.8 days)** (`2026-11-23` to `2026-11-25`, PR `#4,836`), **0% conventional** (plain descriptive sentences enforced by `plain-title.yml`), **100% AI signal**, and **`garrytan` authored 50 of the last 50 commits** (1,444 all-time; next highest contributor has 17).
- Remarkably clean tracker: only **`45` open issues** at **142.6k★** (3,170 stars per open issue!).

## 5. Steal vs. Avoid
- **Steal:**
  1. **Radical benchmark honesty** — testing your own skill pack head-to-head against bare models and publishing when fix rate shows zero lift (58 vs. 61/99).
  2. **Prompt & catalog token-budget ratchets** (`catalog-budget.test.ts` + `context-budget-ratchet.test.ts`) so skills don't silently bloat context windows.
  3. **Pre-registered eval statistics + hard weekly USD spend caps** (`$150/wk`, 3-trial behavioral panels, median-of-3 judges, no p-hacking retries).
  4. **Mandatory egress receipts (`egress-receipt-wiring.test.ts`)** for any tool/agent making outbound network calls.
  5. **Digest-pinned third-party Docker images in CI** (`actionlint@sha256:...`) and **`test-value-bar`** banning fragile prose-pinning tests.
- **Avoid:**
  1. **Splitting 54 KB of instructions across separate `AGENTS.md` (18.6 KB) and `CLAUDE.md` (35.5 KB)** — consolidate into one lean router + focused reference docs.
  2. **Assuming 60+ skills improve raw coding accuracy** — use skills for review, QA, safety guards, and shipping workflows, not as a substitute for model capability or repo lint/test gates.
