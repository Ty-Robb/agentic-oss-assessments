# BMAD-METHOD (`bmad-code-org/BMAD-METHOD`)

- **Snapshot:** `55,740★` · `6,212` forks · **`116` open issues** · `MIT` (GitHub meta `NOASSERTION`) · Active (created Apr 13, 2025; pushed 2026-11-25)
- **Primary Stack:** **1.8 MB Python** tooling (`uv`, Jinja2, PyYAML, `ruamel.yaml`, Ruff, `rumdl`, `yamlfix`, pytest-xdist) + modular Markdown skills + Astro docs site (`docs-site/`); ships v6.12 (stable npm) and v7 preview alpha (`npx skills add`).
- **Data source:** [`data/chunk-06/bmad-code-org__BMAD-METHOD.json`](../../data/chunk-06/bmad-code-org__BMAD-METHOD.json)

## 1. Agent Instruction & Docs Hygiene
- **One of the sharpest 35-line `AGENTS.md` files (2.2 KB) in the entire 34-repo study:**
  - **Self-verifying managed block:** Opens with `<!-- Verified 2026-10-04 against 3cae711e. Managed by bmad-project-context; ... Keep anything you want preserved outside the markers. -->` so freshness is auditable against a real commit SHA.
  - **Best prompt-economics rule in Chunk 6:**
    > *"Skills, workflows, tasks, and agent definitions are prompt text an agent reads in full on every run. Length and ambiguity are paid on every run; a corner case is paid only when it occurs. So do not add instructions for exotic cases — the model usually handles them from context, and the reviewing human can correct it when it does not."*
  - **Three more gems:**
    - *"Prefer deleting an instruction to hedging it."*
    - *"Automated tests assert outcomes produced by deterministic code. Do not write automated tests for LLM output or for static source text."*
    - *"No tool or model attribution, anywhere."*
- **Pragmatic PR governance (`CONTRIBUTING.md`):** PRs must target `dev` (auto-retargeted by `retarget-pr.yaml`), ideal PR size 200–400 lines (hard cap **800 lines**), PR description under **200 words**, and *"Using AI to write code is normal here; using AI as a substitute for thinking is not."*

## 2. Mechanical Gates & Quality Control
- **Lean 5-workflow CI:** `quality.yaml`, `coderabbit-review.yaml` (triggers `@coderabbitai review` only on `ready_for_review` — avoiding wasted reviews on drafts!), `retarget-pr.yaml` (auto-retargets `main` PRs to `dev`), `docs.yaml`, `discord.yaml`.
- **Clean Python & skill validation (`pyproject.toml`):**
  - `uv run tools/validate_skills.py --strict` validates `SKILL.md` frontmatter with real **PyYAML** (explicitly migrated away from hand-rolled frontmatter parsers in `#3169` and `#3182`!).
  - **PEP 723 inline script dependencies:** Every shipped Python script under `skills/<module>/<skill>/scripts/` declares its own inline dependencies + Python `>=3.11` floor (verified by `test_python_floor.py`), so `uv run` executes any skill script with zero project install!
  - Ruff + `rumdl` (curated 5 markdown rules) + `yamlfix` (`whitelines = 1` so embedded workflow shell scripts keep blank lines) + `pytest -n auto`.

## 3. Architectural Bets & Craft
- **Right-sized Agile AI-Driven Development (v7 modularization):** Moved away from a monolithic npm installer (frozen on `V6.12`) toward modular `npx skills add` packs (`core-tools`, `method`, `toolsmith`, `founder`) with a dedicated `bmad-eval` measurement skill and explicit human-in-the-loop philosophy (*"Human Amplification, Not Replacement"*).
- **Clean Jinja2 template discipline:** Mandates block-level `{% if %}` on their own lines (never inline inside sentences) and keeps runtime LLM choices in prose rather than over-templating them.

## 4. Commit, PR & Maintenance Reality
- **High-craft, low-noise velocity:** **50 commits in 27 days** (`2026-10-16` to `2026-11-12`), **92% conventional commits**, **46% fix/revert**, **6% AI signal** (attribution trailers explicitly banned in `AGENTS.md`).
- Tight core pair (`bmadcode` 29/50 recent / 272 all-time; `alexeyv` 13/50 recent / 706 all-time) maintaining 55.7k★ with only **`116` open issues**.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Prompt-economics invariant:** *"Length and ambiguity are paid on every run; a corner case is paid only when it occurs. Prefer deleting an instruction to hedging it."*
  2. **PEP 723 inline script metadata** for shipped Python skill scripts so `uv run` executes them with zero virtual-env setup.
  3. **Triggering AI PR reviewers (`@coderabbitai review`) only on `ready_for_review`** (`coderabbit-review.yaml`) instead of burning noise on every draft push.
  4. **Auto-retargeting `main` PRs to `dev` (`retarget-pr.yaml`)** + **800-line PR cap** + **<200-word PR summary cap**.
  5. **SHA-stamped `AGENTS.md` freshness header** (`Verified YYYY-MM-DD against <sha>`).
- **Avoid:**
  1. **Heavy multi-persona Agile roleplay (Mary, John, Nadia, epics, shards)** on small, clear code changes — even BMAD v7 had to add a *"small changes go straight to build"* bypass to combat process drag.
