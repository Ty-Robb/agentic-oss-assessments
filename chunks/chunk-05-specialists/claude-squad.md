# Claude Squad (`smtg-ai/claude-squad`)

- **Snapshot:** `8,866★` · `641` forks · **`54` open issues** · `AGPL-3.0` · Stable / low-churn maintenance (created Mar 9, 2025; pushed 2026-11-13)
- **Primary Stack:** **263 KB Go** (`go 1.23` / toolchain `1.25.8`), Bubble Tea (`bubbletea` + `bubbles` + `lipgloss`), Cobra CLI, `creack/pty`, wrapping `tmux` + `git worktree` + `gh`; 12 KB Shell, 8.7 KB TS docs site; GoReleaser + Homebrew.
- **Data source:** [`data/chunk-05/smtg-ai__claude-squad.json`](../../data/chunk-05/smtg-ai__claude-squad.json)

## 1. Agent Instruction & Docs Hygiene
- **Zero agent instruction files:** No `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.cursor/`, or `docs/` directory.
- **Minimal human docs:** A clean 162-line `README.md` documenting keybindings, `~/.claude-squad/config.json` profiles, and the 3-bullet architecture (*tmux + git worktrees + TUI*), plus a boilerplate 29-line `CONTRIBUTING.md`.
- **Why it still works here:** At **263 KB of Go** across 8 shallow top-level packages (`app/`, `cmd/`, `config/`, `daemon/`, `keys/`, `log/`, `session/`, `ui/`), an agent or human can read the entire relevant subsystem in seconds — proving that tiny codebases don't need elaborate instruction scaffolding to stay legible.

## 2. Mechanical Gates & Quality Control
- **Lean 5-workflow CI:** `build.yml`, `lint.yml`, `release.yml`, `cla.yml`, `deploy-pages.yml`.
- **Pragmatic diff-only Go linting (`lint.yml`):** Runs `golangci-lint` (`v1.60.1`) with `--fast` and **`only-new-issues: true`** plus a strict `gofmt -l .` check, scoped to Go file path filters (`**.go`, `go.mod`, `go.sum`).
- **Automated binary distribution:** `.goreleaser.yaml` + `release.yml` + `install.sh` + Homebrew (`brew install claude-squad`).
- **Gaps:** No race detector / integration harness visible in the sampled lint workflow, and `golangci-lint` is pinned to an older `v1.60.1`.

## 3. Architectural Bets & Craft
- **Unix-philosophy composition over reinvention:** Instead of building a custom terminal emulator (`cmux`), custom Electron/WebSocket server (`t3code`, `1code`), or custom agent harness (`opencode`), Claude Squad delegates terminal multiplexing to **`tmux`**, workspace isolation to **`git worktree`**, PR shipping to **`gh`**, and agent execution to **any CLI command** (`claude`, `codex`, `gemini`, `aider`, `opencode`, custom profiles).
- **Minimal dependency footprint:** Only 13 direct Go dependencies in `go.mod`; recently even **removed `go-git`** (`#302`) to eliminate a transitive security advisory and stick to native `git`.
- **Real operational polish in small commits:** Recent fixes directly target the exact pain points of TUI worktree wrappers — recovering instances after tmux server death (`#322`), moving expensive ops off the UI event loop (`#253`), computing full diffs only for the selected instance (`#279`), and orphaned worktree cleanup (`#294`).

## 4. Commit, PR & Maintenance Reality
- **Calm, low-churn maturity:** **50 commits over 17 months** (`2025-06-13` to `2026-11-13`, `v1.0.16` → `v1.0.20`), **82% conventional commits**, **36% fix/revert**, **16% AI signal** (mostly external contributors submitting focused bugfix PRs like `#344`, `#322`, `#315`, `#279`).
- **Tiny team, tiny backlog:** Two authors (`mufeez-amjad` 116 total / 28 of last 50; `jayshrivastava` 87 total / 4 of last 50) maintain an 8.9k★ tool with only **`54` open issues** — the cleanest issue-to-star maintenance ratio among active standalone tools in Chunk 5.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Radical scope discipline (compose `tmux` + `git worktree` + `gh` instead of rebuilding them):** 263 KB of Go achieves ~70% of the local multi-agent workflow with almost zero maintenance drag.
  2. **`golangci-lint` with `only-new-issues: true`:** Zero-friction lint ratchet for small repos adopting stricter checks incrementally.
  3. **Deleting heavy libraries in favor of native CLIs** (removing `go-git` to shed CVEs and complexity) and computing diffs lazily only for the active selection.
- **Avoid:**
  1. **AGPL-3.0 + CLA friction** if you want wide enterprise adoption or frictionless community patches.
  2. **Relying on `tmux` screen-scraping / prompt-matching** (e.g., `#263` *"Update claude trust prompt handling"*) for structured agent control — brittle whenever upstream CLIs change their TUI output.
