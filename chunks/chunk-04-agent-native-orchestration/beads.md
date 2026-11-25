# Beads (`gastownhall/beads`, formerly `steveyegge/beads`)

- **Snapshot:** `29,048★` · `1,960` forks · `1,828` open issues · `MIT` · Active (created Oct 2025; pushed 2026-11-24)
- **Primary Stack:** Go + **Bazel** (51.4 MB Go, 740 KB Starlark, CGO + embedded/server **Dolt** version-controlled SQL database, `nogo` lint + `.golangci.yml`, Cobra + Charmbracelet TUI, OpenTelemetry, `testcontainers-go`, Nix flake, GoReleaser, npm/PyPI wrappers).
- **Data source:** [`data/chunk-04/gastownhall__beads.json`](../../data/chunk-04/gastownhall__beads.json)

## 1. Agent Instruction & Docs Hygiene
- **Exceptionally thoughtful 245-line `AGENTS.md` (13.6 KB)** with symlinked `CLAUDE.md` (zero drift) and a 15-row routing table to `engdocs/` (`PROJECT_CHARTER.md`, `TESTING.md`, `LINTING.md`, `AGENT_SIGNING.md`, `UI_PHILOSOPHY.md`) and `.claude/skills/beads-docs/SKILL.md`.
- **Anti-hallucination verification rules every Go/Bazel team should copy:**
  - Explicitly warns about the **Go silent-skip trap**: *"A target also passes when the test never ran (a filter that matches nothing, a skip, a file the configuration does not compile)... Go prints `--- PASS` for a test whose every subtest skipped. Count a run only when its log shows `--- PASS: TestName` and no `--- SKIP`."*
  - Requires `NOT_ENOUGH_INFO` in issue/PR form fields when evidence runs out (prevents agents from fabricating reproduction details!).
  - Requires running `scripts/pr-preflight.sh` before implementing/opening/closing any PR and `scripts/gh-body-lint <body-file>` before posting with `gh ... --body-file`.
- **Contributor-first anti-steamrolling policy:** Explicitly instructs agents to search open PRs first, build on an external contributor's branch, preserve their tests and `Co-authored-by:`, and *never* silently supersede a contributor PR.
- **Non-interactive shell safety list:** Documents exact non-interactive flags (`cp -f`, `rm -f`, `ssh -o BatchMode=yes`, `HOMEBREW_NO_AUTO_UPDATE=1 brew`, never `bd edit`) and forbids emoji-style CLI icons in favor of crisp Unicode status glyphs (`○ ◐ ● ✓ ❄`).

## 2. Mechanical Gates & Quality Control
- **Full Bazel + `nogo` + RBE (`rbe-west`) CI architecture (23 workflows):**
  - Contributors get an **anonymous read-only remote build cache (`--config=fork-cache`)** so local builds hit CI cache instantly without credentials!
  - `bazel-autofix.yml` automatically repairs out-of-sync `BUILD.bazel` files on same-repo PRs and posts apply recipes on fork PRs.
  - `make check-docs` runs Bazel docsync + doc freshness + CLI flag verification so docs can't drift from Cobra flags.
- **Brilliant merge-queue + post-merge alerting (`pr.yml`, `pr-risk.yml`, `main-ci-alert.yml`):**
  - Merge groups run the fast Linux/Bazel subset (`ci-scope.sh`), while pushes to `main` run the heavy cross-OS (Windows/macOS/Nix) and Dolt-tier complement.
  - **`main-ci-alert.yml`:** Whenever a post-merge `main` push turns red, automatically opens (or updates) a single `ci/main-red` issue listing every candidate PR in the merged batch, comments on each candidate PR, and **auto-closes the issue** once every tracked workflow turns green again — using `concurrency: { group: main-ci-alert, queue: max }` to avoid duplicate issues!
  - Even its CI bash/workflow policies are unit-tested in Go (`scripts/main_ci_alert_test.go`, `scripts/ci_merge_queue_test.go`).
- **Race-safe label automation (`remove-needs-triage.yml`):** Explicitly handles concurrent `labeled` webhook 404 races so benign concurrent label removals don't paint a red X on PR checks.

## 3. Architectural Bets & Craft
- **Git-native structured agent memory (Dolt + hash IDs):** Replaces flat markdown TODO lists with a dependency-aware issue graph (`bd ready`, `bd update --claim`, `bd remember`, `bd prime`, semantic compaction) using hash-based IDs (`bd-a1b2`) to prevent multi-branch/multi-agent merge collisions, plus `--stealth` and `--contributor` modes so personal agent planning stays out of upstream PRs.
- **Strict layering & scope charter (`Schema → issueops → cmd/bd`):** Enforces a hard storage-driver boundary against Dolt (`dolthub/driver`), preferring metadata over schema bloat and leaving orchestration policy to external orchestrators.
- **Heavy root clutter trade-off:** 51.4 MB of Go + Bazel + Dolt CGO + 90 KB `pr.yml` (1,735 lines!) + multiple root `PROPOSAL-*.md` and `*_test.go` files reflect intense rapid evolution from lightweight JSONL CLI to full Dolt-backed distributed graph DB.

## 4. Commit, PR & Maintenance Reality
- **Most agent-operated repository in the entire study:**
  - **41 of the last 50 commits (82%) are authored by `gascity-eddie[bot]`!**
  - **100% conventional commits**, **100% AI-signed (`Agent-Signature:` trailer)**, **82% `fix:`** over 8 days (2026-11-12 to 2026-11-20), driven by an automated PR pipeline (`status/needs-review-auto` → `status/reviewing` → `status/merge-ready` → `status/merge-queued`).
  - Notice how many bot commits include `(supersedes #7304)` / `(GH#4135)` — actively burning down community backlog and edge-case bugs at high throughput while crediting original PRs/issues.
  - All-time top contributor remains founder `steveyegge` (4,805 commits), followed by `maphew` (776), `julianknutsen` (699), `coffeegoddd` (616), and `gascity-eddie[bot]` (156).

## 5. Steal vs. Avoid
- **Steal:**
  1. **The "Check That the Test Actually Ran" rule** (verifying `--- PASS` and zero `--- SKIP`, never trusting a vacuous filtered pass) — applies to Vitest/Jest/Pytest too (`--passWithNoTests` traps!).
  2. **`NOT_ENOUGH_INFO` evidence rule + `scripts/gh-body-lint`** to stop agents from hallucinating issue repros or mangling GitHub markdown.
  3. **`main-ci-alert.yml` + Go-tested CI policy scripts** — closes the observability gap when using fast merge queues + heavier post-merge CI.
  4. **Anonymous read-only remote build cache (`--config=fork-cache`)** and **explicit non-interactive shell flags** in `AGENTS.md`.
  5. **Contributor-protection checklist** before letting autonomous bots rewrite or close external PRs.
- **Avoid:**
  1. **1,735-line `pr.yml` + 25+ root `.md` proposal/guide files** — hard for humans and agents to navigate without a map.
  2. **Heavy CGO + embedded Dolt + Bazel toolchain** unless you genuinely need cell-level SQL branching/merging.
