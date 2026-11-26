# GitHub Spec Kit (`github/spec-kit`)

- **Snapshot:** `151,365★` · `13,607` forks · `230` open issues · `MIT` · Active (created Aug 21, 2025; pushed 2026-11-25)
- **Primary Stack:** **11.9 MB Python** (`specify-cli`, Python 3.11+, `uv`, Typer, Pydantic, Lark, MCP SDK 2.x, Hatchling) + 142 KB Shell + 137 KB PowerShell; Ruff, pytest (`pytest-xdist`), DocFX, GitHub Agentic Workflows (`gh-aw`).
- **Data source:** [`data/chunk-06/github__spec-kit.json`](../../data/chunk-06/github__spec-kit.json)

## 1. Agent Instruction & Docs Hygiene
- **Crisp, architecture-routed 76-line `AGENTS.md` (3.7 KB):** Maps every subsystem (`design/shared.md`, `design/cli.md`, `design/mcp.md`, `design/integration.md`, `design/workflow-step.md`) cleanly without duplicating prose.
- **Concrete environment & portability traps:**
  - Enforces **Windows PowerShell 5.1** compatibility across all generated PS scripts (exact built-in Windows version, with required PS 5.1 validation evidence).
  - Warns against worktree virtualenv bleed: *"Run the suite inside this worktree's own virtualenv (`.venv/bin/python -m pytest`). A bare `uv run pytest` can pick up an editable install from another worktree."*
- **Strong Evidence Gate (`CONTRIBUTING.md` — 519 lines):** *"A contribution is evaluated on the evidence it carries, not on how plausible its reasoning sounds. The same bar applies to everyone — human and AI-assisted contributions are judged identically."* Caps active review priority at 3 open PRs per author, mandates splitting prerequisite core changes from integration PRs, and requires per-activity AI disclosure (commits, PRs, *and* review comments).

## 2. Mechanical Gates & Quality Control
- **19 YAML workflows (29 total entries in `.github/workflows/`, including 10 `gh-aw` `.md` sources) — first repo in the 36-repo study using GitHub Agentic Workflows (`gh-aw`) in production:**
  - Markdown-authored workflows (`add-community-preset.md`, `add-community-extension.md`, `add-community-bundle.md`, `bug-assess.md`, `bug-fix.md`, `bug-test.md`, `feature-assess.md`, `pr-assess.md`) compiled via `gh aw compile` into locked YAML (`.lock.yml`).
  - **Defense-in-depth agent sandboxing inside CI:**
    - Runs Copilot inside **SHA-256 digest-pinned firewall containers** (`ghcr.io/github/gh-aw-firewall/{agent,api-proxy,squid}:0.28.14@sha256:...`).
    - Explicit network domain allowlist (`github.com`, `raw.githubusercontent.com`) + read-only `contents`/`issues` permissions + **constrained `safe-outputs`** (`allowed-files: [presets/catalog.community.json]`, `draft: true`, `max: 1`, `threat-detection: continue-on-error: false`, `protected-files: policy: blocked`).
- **Subprocess security posture locked in Ruff (`pyproject.toml`):** Enables `S602`, `S604`, `S605` so any reintroduction of `shell=True` or `os.system` requires an explicit `# noqa` visible in review.

## 3. Architectural Bets & Craft
- **Enterprise-grade, air-gap-ready Spec-Driven Development platform:** Bundles core templates, extensions (`git`, `agent-context`, `assess`, `bug`, `github`), workflows (`speckit`, `bugfix`, `assess`), presets (`lean`, `constitution-sync`), and catalog snapshots right inside the Python wheel (`hatchling` `force-include`) so `specify init` works completely offline behind corporate firewalls.
- **Composable extensibility:** Separates Integrations (coding agents), Extensions (commands/hooks), Presets (org/regulatory standards), Workflow Overlays (modify without forking), and private self-hosted Catalogs.

## 4. Commit, PR & Maintenance Reality
- **Healthy multi-maintainer enterprise cadence:** **50 commits in 7.0 days** (`2026-11-18` to `2026-11-25`, `v1.4.1` → `v1.4.5`, PR `#5,576`), **78% conventional**, **60% fix/revert**, **34% AI signal** (including `[Copilot Dreaming]` automated fixes and `github-actions[bot]` catalog updates).
- Well-distributed human team (`mnriem` 478, `localden` 361, `jawwad-ali` 153, `Quratulain-bilal` 100, `adityajai119` 9/50 recent) keeping open issues to just **`230`** at **151.4k★**.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Firewall-sandboxed agent CI workflows (`gh-aw` pattern):** Digest-pinned containers + domain allowlists + constrained `safe-outputs` (`allowed-files`, `draft: true`, `max: 1`, `threat-detection`).
  2. **The Evidence Gate framing** (*"evaluated on the evidence it carries, not on how plausible its reasoning sounds"* + identical bar for human and AI PRs).
  3. **Ruff `S602`/`S604`/`S605`** locking out `shell=True` unless explicitly reviewed via `# noqa`.
  4. **Explicit per-worktree `.venv/bin/python -m pytest` rule** preventing editable-install cross-worktree bleed in Python repos.
- **Avoid:**
  1. **130 KB generated `.lock.yml` workflow files** unless you genuinely need `gh-aw`'s compiled firewall/safe-output sandbox — overkill for a small private team.
  2. **Adopting full SDD bureaucracy (constitution → spec → plan → tasks → overlays) on tiny greenfield or solo changes** where lightweight `/grill-me` + tests move faster.
