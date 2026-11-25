#!/usr/bin/env python3
"""
Zero-dependency static site generator for Agentic OSS Assessments.
Builds the complete GitHub Pages website into docs/ directly from:
  - data/chunk-01..06/*.json
  - chunks/chunk-01..06/*.md
  - synthesis/PLAYBOOK.md & synthesis/EXECUTIVE_BRIEF.md
  - distribution/x-article.md, distribution/upgrade-prompt.txt, distribution/assets/*.png
  - RUBRIC.md
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO_URL = "https://github.com/Ty-Robb/agentic-oss-assessments"
SITE_URL = "https://ty-robb.github.io/agentic-oss-assessments"
SNAPSHOT_DATE = "Nov 25, 2026"

# Complete ordered registry mapping every repo JSON -> assessment doc + curated metadata
REPO_REGISTRY: list[dict[str, Any]] = [
    # Baseline
    {
        "slug": "t3code",
        "repo": "pingdotgg/t3code",
        "chunk": "Base",
        "chunk_label": "Baseline",
        "data_path": "data/chunk-01/pingdotgg__t3code.json",
        "md_path": "RUBRIC.md",
        "status": "Active",
        "velocity": "50 / 7.0 hrs",
        "stack": "TS (226.7 MB, Effect, Vite+, Electron, RN)",
        "signature": "oxlint-plugin-t3code, VOUCHED.td, evals/, agent-context-budget",
    },
    # Chunk 1
    {
        "slug": "paradev",
        "repo": "ParadevAI/Paradev",
        "chunk": "C1",
        "chunk_label": "C1 · Rivals",
        "data_path": "data/chunk-01/ParadevAI__Paradev.json",
        "md_path": "chunks/chunk-01-direct-rivals/paradev.md",
        "status": "Active",
        "velocity": "50 / 3.2 days",
        "stack": "TS (35.2 MB, Bun, Turbo, Electron/Next/Expo, Drizzle) + TLA+",
        "signature": "Domain noRestrictedImports in Biome, paradev schema, 2-min test budget",
    },
    {
        "slug": "vibe-kanban",
        "repo": "BloopAI/vibe-kanban",
        "chunk": "C1",
        "chunk_label": "C1 · Rivals",
        "data_path": "data/chunk-01/BloopAI__vibe-kanban.json",
        "md_path": "chunks/chunk-01-direct-rivals/vibe-kanban.md",
        "status": "Sunsetting",
        "velocity": "50 / 7.5 mos",
        "stack": "30-crate Rust (axum/sqlx/ts-rs/tauri) + React",
        "signature": "ts-rs codegen check, sqlx offline check (warning: scope sprawl)",
    },
    {
        "slug": "emdash",
        "repo": "generalaction/emdash",
        "chunk": "C1",
        "chunk_label": "C1 · Rivals",
        "data_path": "data/chunk-01/generalaction__emdash.json",
        "md_path": "chunks/chunk-01-direct-rivals/emdash.md",
        "status": "Active",
        "velocity": "50 / 22 days",
        "stack": "TS (21.2 MB, pnpm, Nx, Electron, Drizzle, MobX)",
        "signature": "respectEslintDisableDirectives: false, self-pruning allowlists, sole-writer DB lint",
    },
    {
        "slug": "1code",
        "repo": "21st-dev/1code",
        "chunk": "C1",
        "chunk_label": "C1 · Rivals",
        "data_path": "data/chunk-01/21st-dev__1code.json",
        "md_path": "chunks/chunk-01-direct-rivals/1code.md",
        "status": "Archived",
        "velocity": "Archived Mar '26",
        "stack": "TS (5.1 MB, Electron, Bun, tRPC, Drizzle)",
        "signature": "Ephemeral NDJSON log server; anti-pattern on 0 CI / mirror / dual lockfiles",
    },
    # Chunk 2
    {
        "slug": "opencode",
        "repo": "anomalyco/opencode",
        "chunk": "C2",
        "chunk_label": "C2 · Harnesses",
        "data_path": "data/chunk-02/anomalyco__opencode.json",
        "md_path": "chunks/chunk-02-agent-harnesses/opencode.md",
        "status": "Active",
        "velocity": "50 / 12.3 hrs",
        "stack": "TS (Effect v4, Bun, Solid/OpenTUI) + Rust daemon",
        "signature": "anti-slop oxlint plugins, unit-tested ast-grep, Miri, 7 triage workflows",
    },
    {
        "slug": "pi",
        "repo": "earendil-works/pi",
        "chunk": "C2",
        "chunk_label": "C2 · Harnesses",
        "data_path": "data/chunk-02/earendil-works__pi.json",
        "md_path": "chunks/chunk-02-agent-harnesses/pi.md",
        "status": "Active",
        "velocity": "50 / 1.7 days",
        "stack": "TS (npm workspaces, erasable TS, Biome)",
        "signature": "Default-closed lgtmi/lgtm gate (307 issues), multi-agent Git safety, GritQL Biome",
    },
    {
        "slug": "codex",
        "repo": "openai/codex",
        "chunk": "C2",
        "chunk_label": "C2 · Harnesses",
        "data_path": "data/chunk-02/openai__codex.json",
        "md_path": "chunks/chunk-02-agent-harnesses/codex.md",
        "status": "Active",
        "velocity": "50 / 14.7 hrs",
        "stack": "Rust (90.7 MB, Bazel/Cargo) + pnpm SDKs",
        "signature": "7-day npm cooldown (minimumReleaseAge: 10080), CI required aggregator",
    },
    {
        "slug": "gemini-cli",
        "repo": "google-gemini/gemini-cli",
        "chunk": "C2",
        "chunk_label": "C2 · Harnesses",
        "data_path": "data/chunk-02/google-gemini__gemini-cli.json",
        "md_path": "chunks/chunk-02-agent-harnesses/gemini-cli.md",
        "status": "Active",
        "velocity": "50 / 18.1 days",
        "stack": "TS (npm workspaces, Ink, esbuild/SEA)",
        "signature": "47 behavioral evals/ + 2-stage eval-pr.yml, zero-checkout drift check",
    },
    # Chunk 3
    {
        "slug": "cline",
        "repo": "cline/cline",
        "chunk": "C3",
        "chunk_label": "C3 · Autonomous",
        "data_path": "data/chunk-03/cline__cline.json",
        "md_path": "chunks/chunk-03-autonomous-and-ide/cline.md",
        "status": "Active",
        "velocity": "50 / 19.5 days",
        "stack": "TS (Bun, SDK + CLI + VS Code gRPC + Tauri)",
        "signature": "34-line trap-only AGENTS.md, strip agent promo footers, fixture installer tests",
    },
    {
        "slug": "roo-code",
        "repo": "RooCodeInc/Roo-Code",
        "chunk": "C3",
        "chunk_label": "C3 · Autonomous",
        "data_path": "data/chunk-03/RooCodeInc__Roo-Code.json",
        "md_path": "chunks/chunk-03-autonomous-and-ide/roo-code.md",
        "status": "Archived",
        "velocity": "Archived May '26",
        "stack": "TS (pnpm, Turbo, VS Code ext + webview)",
        "signature": "5-line single-invariant AGENTS.md, .roomodes; warning on VS Code lock-in",
    },
    {
        "slug": "openhands",
        "repo": "OpenHands/OpenHands",
        "chunk": "C3",
        "chunk_label": "C3 · Autonomous",
        "data_path": "data/chunk-03/OpenHands__OpenHands.json",
        "md_path": "chunks/chunk-03-autonomous-and-ide/openhands.md",
        "status": "Active",
        "velocity": "50 / 2.0 days",
        "stack": "TS (React 19, Vite 8, Electron Agent Canvas)",
        "signature": "verify-skill-isolation.yml, Stryker diff mutation testing, HUMAN: PR check",
    },
    {
        "slug": "goose",
        "repo": "aaif-goose/goose",
        "chunk": "C3",
        "chunk_label": "C3 · Autonomous",
        "data_path": "data/chunk-03/aaif-goose__goose.json",
        "md_path": "chunks/chunk-03-autonomous-and-ide/goose.md",
        "status": "Active",
        "velocity": "50 / 5.0 days",
        "stack": "Rust (oi-kit + ACP + rmcp) + Electron",
        "signature": "Ready-board gate (512 issues), check-lean-size, wasm32, git cherry release check",
    },
    # Chunk 4
    {
        "slug": "openclaw",
        "repo": "openclaw/openclaw",
        "chunk": "C4",
        "chunk_label": "C4 · Orchestration",
        "data_path": "data/chunk-04/openclaw__openclaw.json",
        "md_path": "chunks/chunk-04-agent-native-orchestration/openclaw.md",
        "status": "Active",
        "velocity": "50 / 2.3 hrs",
        "stack": "TS (474.7 MB) + Swift/Kotlin/Rust, Kysely",
        "signature": "<20 KB AGENTS.md ('cite an incident'), all-error oxlint, prefix-stability test",
    },
    {
        "slug": "paperclip",
        "repo": "paperclipai/paperclip",
        "chunk": "C4",
        "chunk_label": "C4 · Orchestration",
        "data_path": "data/chunk-04/paperclipai__paperclip.json",
        "md_path": "chunks/chunk-04-agent-native-orchestration/paperclip.md",
        "status": "Active",
        "velocity": "50 / 14.5 hrs",
        "stack": "TS (157.8 MB, Express/React/Drizzle/PG) + Rust",
        "signature": "grep-indexed rules/*.mdc, pnpm verify (exit 2), real PG pg_dump/restore CI",
    },
    {
        "slug": "symphony",
        "repo": "openai/symphony",
        "chunk": "C4",
        "chunk_label": "C4 · Orchestration",
        "data_path": "data/chunk-04/openai__symphony.json",
        "md_path": "chunks/chunk-04-agent-native-orchestration/symphony.md",
        "status": "Active",
        "velocity": "47 / 6.0 mos",
        "stack": "SPEC.md + 914 KB Elixir/OTP + Burrito",
        "signature": "Spec-as-product ('implement SPEC.md in your language'), mix pr_body.check",
    },
    {
        "slug": "beads",
        "repo": "gastownhall/beads",
        "chunk": "C4",
        "chunk_label": "C4 · Orchestration",
        "data_path": "data/chunk-04/gastownhall__beads.json",
        "md_path": "chunks/chunk-04-agent-native-orchestration/beads.md",
        "status": "Active",
        "velocity": "50 / 8.0 days",
        "stack": "Go (51.4 MB) + Bazel + Dolt",
        "signature": "gascity-eddie[bot] (41/50 commits), NOT_ENOUGH_INFO, 'verify test actually ran'",
    },
    # Chunk 5
    {
        "slug": "paseo",
        "repo": "getpaseo/paseo",
        "chunk": "C5",
        "chunk_label": "C5 · Specialists",
        "data_path": "data/chunk-05/getpaseo__paseo.json",
        "md_path": "chunks/chunk-05-specialists/paseo.md",
        "status": "Active",
        "velocity": "50 / 2.4 days",
        "stack": "TS (51.2 MB, Expo/Electron, Noise NK relay)",
        "signature": "Anti-slop Doc voice, per-file/API no-sync-io allowlist, 'PRs closed by default'",
    },
    {
        "slug": "happy",
        "repo": "slopus/happy",
        "chunk": "C5",
        "chunk_label": "C5 · Specialists",
        "data_path": "data/chunk-05/slopus__happy.json",
        "md_path": "chunks/chunk-05-specialists/happy.md",
        "status": "Active",
        "velocity": "50 / 8.4 days",
        "stack": "Native Swift (22.3 MB) + Kotlin (14.6 MB) + TS",
        "signature": "Incident-cited main == origin/main release rule, CI-cost ban, env:up/seed CLI",
    },
    {
        "slug": "cmux",
        "repo": "manaflow-ai/cmux",
        "chunk": "C5",
        "chunk_label": "C5 · Specialists",
        "data_path": "data/chunk-05/manaflow-ai__cmux.json",
        "md_path": "chunks/chunk-05-specialists/cmux.md",
        "status": "Active",
        "velocity": "50 / 9.7 hrs",
        "stack": "Swift (115.2 MB) + Py/Rust/TS + Ghostty",
        "signature": "REVIEW.md, verify-local.py --receipt - (warning: 231 workflows CI factory tax)",
    },
    {
        "slug": "claude-squad",
        "repo": "smtg-ai/claude-squad",
        "chunk": "C5",
        "chunk_label": "C5 · Specialists",
        "data_path": "data/chunk-05/smtg-ai__claude-squad.json",
        "md_path": "chunks/chunk-05-specialists/claude-squad.md",
        "status": "Active",
        "velocity": "50 / 17 mos",
        "stack": "263 KB Go (Bubble Tea) + tmux + worktrees",
        "signature": "Unix composition over reinvention, golangci-lint --only-new-issues",
    },
    {
        "slug": "bolt-diy",
        "repo": "stackblitz-labs/bolt.diy",
        "chunk": "C5",
        "chunk_label": "C5 · Specialists",
        "data_path": "data/chunk-05/stackblitz-labs__bolt.diy.json",
        "md_path": "chunks/chunk-05-specialists/bolt-diy.md",
        "status": "Active",
        "velocity": "50 / 5.3 days",
        "stack": "TS (3.4 MB, React Router, WebContainers, AI SDK)",
        "signature": "Prod Docker curl smoke test in CI, .performance-budgets.json, Lighthouse CI",
    },
    {
        "slug": "oh-my-openagent",
        "repo": "code-yeongyu/oh-my-openagent",
        "chunk": "C5",
        "chunk_label": "C5 · Specialists",
        "data_path": "data/chunk-05/code-yeongyu__oh-my-openagent.json",
        "md_path": "chunks/chunk-05-specialists/oh-my-openagent.md",
        "status": "Active",
        "velocity": "50 / 19.2 hrs",
        "stack": "TS (58.0 MB) + Rust (5.3 MB), 45 pkgs, Bun",
        "signature": "Local .omo/evidence/ + sha256sum proof + anti-commit test, hermetic $HOME tests",
    },
    {
        "slug": "costrict",
        "repo": "zgsm-ai/costrict",
        "chunk": "C5",
        "chunk_label": "C5 · Specialists",
        "data_path": "data/chunk-05/zgsm-ai__costrict.json",
        "md_path": "chunks/chunk-05-specialists/costrict.md",
        "status": "Slowing",
        "velocity": "50 / 3.6 mos",
        "stack": "TS (15.1 MB, Roo Code enterprise fork, pnpm)",
        "signature": "1-line English commit rule (92% conv), 40+ CVE overrides, workspace-trust MCP gate",
    },
    # Chunk 6
    {
        "slug": "mattpocock-skills",
        "repo": "mattpocock/skills",
        "chunk": "C6",
        "chunk_label": "C6 · Skill Stacks",
        "data_path": "data/chunk-06/mattpocock__skills.json",
        "md_path": "chunks/chunk-06-skill-stacks/mattpocock-skills.md",
        "status": "Active",
        "velocity": "50 / 7.1 wks",
        "stack": "Markdown skills + 20 KB Shell/JS, Changesets",
        "signature": "5-bucket lifecycle, fresh-context subagents, Codex openai.yaml parity, YAML check",
    },
    {
        "slug": "mattpocock-sandcastle",
        "repo": "mattpocock/sandcastle",
        "chunk": "C6",
        "chunk_label": "C6 · Skill Stacks",
        "data_path": "data/chunk-06/mattpocock__sandcastle.json",
        "md_path": "chunks/chunk-06-skill-stacks/mattpocock-sandcastle.md",
        "status": "Active",
        "velocity": "50 / 6.0 days",
        "stack": "TS (2.6 MB, TS 7, Effect, oxlint-tsgolint)",
        "signature": "All-5-cat oxlint straitjacket + lint-shrink.yml PR bot, real bwrap CI, docs-guide test",
    },
    {
        "slug": "superpowers",
        "repo": "obra/superpowers",
        "chunk": "C6",
        "chunk_label": "C6 · Skill Stacks",
        "data_path": "data/chunk-06/obra__superpowers.json",
        "md_path": "chunks/chunk-06-skill-stacks/superpowers.md",
        "status": "Active",
        "velocity": "50 / 4.0 mos",
        "stack": "Markdown skills + 520 KB Shell/JS, 15+ harnesses",
        "signature": "94% PR rejection rate stated on line 1, external Quorum eval lab, bootstrap test",
    },
    {
        "slug": "spec-kit",
        "repo": "github/spec-kit",
        "chunk": "C6",
        "chunk_label": "C6 · Skill Stacks",
        "data_path": "data/chunk-06/github__spec-kit.json",
        "md_path": "chunks/chunk-06-skill-stacks/spec-kit.md",
        "status": "Active",
        "velocity": "50 / 7.0 days",
        "stack": "Python (11.9 MB, uv, Typer, MCP SDK)",
        "signature": "Firewall-sandboxed gh-aw agentic workflows, Evidence Gate, Ruff S602-S605",
    },
    {
        "slug": "gstack",
        "repo": "garrytan/gstack",
        "chunk": "C6",
        "chunk_label": "C6 · Skill Stacks",
        "data_path": "data/chunk-06/garrytan__gstack.json",
        "md_path": "chunks/chunk-06-skill-stacks/gstack.md",
        "status": "Active",
        "velocity": "50 / 1.8 days",
        "stack": "TS (45.1 MB), Bun, Playwright/Aside CLIs",
        "signature": "Honest 58 vs 61/99 self-eval, egress-receipt-wiring, token-budget ratchets, $150/wk cap",
    },
    {
        "slug": "openspec",
        "repo": "Fission-AI/OpenSpec",
        "chunk": "C6",
        "chunk_label": "C6 · Skill Stacks",
        "data_path": "data/chunk-06/Fission-AI__OpenSpec.json",
        "md_path": "chunks/chunk-06-skill-stacks/openspec.md",
        "status": "Active",
        "velocity": "50 / 25 days",
        "stack": "TS (5.8 MB, Node 22+, pnpm 10, Vitest 5)",
        "signature": "startup-modules.test.ts CLI cold-start guard, GHSA-annotated overrides, 2-PR features",
    },
    {
        "slug": "get-shit-done",
        "repo": "gsd-build/get-shit-done",
        "chunk": "C6",
        "chunk_label": "C6 · Skill Stacks",
        "data_path": "data/chunk-06/gsd-build__get-shit-done.json",
        "md_path": "chunks/chunk-06-skill-stacks/get-shit-done.md",
        "status": "Archived",
        "velocity": "Archived May '26",
        "stack": "7.3 MB CJS + 2.6 MB TS SDK, node:test",
        "signature": "prompt-injection-scan.sh, ADRs; archived after compromise warning -> open-gsd",
    },
    {
        "slug": "bmad-method",
        "repo": "bmad-code-org/BMAD-METHOD",
        "chunk": "C6",
        "chunk_label": "C6 · Skill Stacks",
        "data_path": "data/chunk-06/bmad-code-org__BMAD-METHOD.json",
        "md_path": "chunks/chunk-06-skill-stacks/bmad-method.md",
        "status": "Active",
        "velocity": "50 / 27 days",
        "stack": "Python (1.8 MB, uv, Jinja2, Ruff) + Astro",
        "signature": "'Prefer deleting an instruction to hedging it', PEP 723 skill scripts, ready_for_review AI",
    },
    {
        "slug": "backnotprop-pstack",
        "repo": "backnotprop/pstack",
        "chunk": "C6",
        "chunk_label": "C6 · Skill Stacks",
        "data_path": "data/chunk-06/backnotprop__pstack.json",
        "md_path": "chunks/chunk-06-skill-stacks/pstack.md",
        "status": "Active",
        "velocity": "7 / 3 wks",
        "stack": "Agent Skills + TLA+ (48.8 KB) + Lean (52 KB)",
        "signature": "Port of Lauren Tan's Cursor pstack: /create-formal-verification-skill (TLA+/Lean)",
    },
    {
        "slug": "pstack-claude",
        "repo": "michael-denyer/pstack-claude",
        "chunk": "C6",
        "chunk_label": "C6 · Skill Stacks",
        "data_path": "data/chunk-06/michael-denyer__pstack-claude.json",
        "md_path": "chunks/chunk-06-skill-stacks/pstack.md",
        "status": "Active",
        "velocity": "50 / 6.5 days",
        "stack": "1.8 MB TS/JS multi-harness pstack port + TLA+/Lean",
        "signature": "tools/forks.json CI check, --check-rules, watch-pr prompt-injection hardening",
    },
]

CHUNK_SUMMARIES = [
    ("chunk-01", "Chunk 1 · Direct T3 Code Rivals", "chunks/chunk-01-direct-rivals/SUMMARY.md"),
    ("chunk-02", "Chunk 2 · Flagship Agent Harnesses", "chunks/chunk-02-agent-harnesses/SUMMARY.md"),
    ("chunk-03", "Chunk 3 · Autonomous & IDE Heavyweights", "chunks/chunk-03-autonomous-and-ide/SUMMARY.md"),
    ("chunk-04", "Chunk 4 · Agent-Native Orchestration", "chunks/chunk-04-agent-native-orchestration/SUMMARY.md"),
    ("chunk-05", "Chunk 5 · Mobile, Terminal & Specialists", "chunks/chunk-05-specialists/SUMMARY.md"),
    ("chunk-06", "Chunk 6 · Agent Skill & Workflow Stacks", "chunks/chunk-06-skill-stacks/SUMMARY.md"),
]

# Build map from relative repo markdown paths to site URLs for link rewriting
MD_PATH_TO_SITE: dict[str, str] = {
    "RUBRIC.md": "repos/t3code.html",
    "README.md": "index.html",
    "synthesis/PLAYBOOK.md": "playbook.html",
    "synthesis/EXECUTIVE_BRIEF.md": "brief.html",
    "distribution/x-article.md": "article.html",
}
for _r in REPO_REGISTRY:
    if _r["md_path"] != "RUBRIC.md" and _r["md_path"] not in MD_PATH_TO_SITE:
        MD_PATH_TO_SITE[_r["md_path"]] = f"repos/{_r['slug']}.html"
for _cid, _, _mpath in CHUNK_SUMMARIES:
    MD_PATH_TO_SITE[_mpath] = f"chunks/{_cid}.html"


def fmt_stars(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)


def fmt_int(n: int) -> str:
    return f"{n:,}"


def rewrite_href(href: str, source_md_rel: str, page_depth: int) -> str:
    """Rewrite relative markdown links to site HTML routes or GitHub blob URLs."""
    if href.startswith(("http://", "https://", "#", "mailto:")):
        return href
    prefix = "../" * page_depth
    # Check if image asset reference
    if href.endswith((".png", ".jpg", ".svg")):
        return f"{prefix}assets/{Path(href).name}"
    # Resolve relative to source markdown path
    clean_href, anchor = (href.split("#", 1) + [""])[:2]
    resolved = os.path.normpath(os.path.join(os.path.dirname(source_md_rel), clean_href))
    resolved = resolved.replace("\\", "/")
    if resolved in MD_PATH_TO_SITE:
        target = prefix + MD_PATH_TO_SITE[resolved]
        return f"{target}#{anchor}" if anchor else target
    # Fallback: link directly to GitHub blob/tree
    if resolved.startswith("data/") or resolved.startswith("scripts/") or resolved.endswith(".json"):
        return f"{REPO_URL}/blob/main/{resolved}"
    return f"{REPO_URL}/blob/main/{resolved}"


def render_inline(text: str, source_md_rel: str, page_depth: int) -> str:
    """Render inline markdown (code, links, bold, italic) safely."""
    placeholders: list[str] = []

    def stash(html_str: str) -> str:
        idx = len(placeholders)
        placeholders.append(html_str)
        return f"\x00PH{idx}\x00"

    # Inline code first so nothing inside gets mangled
    def repl_code(m: re.Match[str]) -> str:
        return stash(f"<code>{html.escape(m.group(1))}</code>")

    s = re.sub(r"`([^`]+)`", repl_code, text)

    # Images ![alt](url)
    def repl_img(m: re.Match[str]) -> str:
        alt = html.escape(m.group(1))
        url = html.escape(rewrite_href(m.group(2), source_md_rel, page_depth))
        return stash(f'<figure class="md-figure"><img src="{url}" alt="{alt}" loading="lazy"></figure>')

    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl_img, s)

    # Links [label](url) — label may contain bold or inline code placeholders
    def repl_link(m: re.Match[str]) -> str:
        label_raw = m.group(1)
        url = rewrite_href(m.group(2), source_md_rel, page_depth)
        ext = ' target="_blank" rel="noopener noreferrer"' if url.startswith("http") else ""
        label_html = render_inline_emph(html.escape(label_raw))
        return stash(f'<a href="{html.escape(url)}"{ext}>{label_html}</a>')

    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_link, s)

    s = html.escape(s)
    s = render_inline_emph(s)

    for idx in range(len(placeholders) - 1, -1, -1):
        s = s.replace(f"\x00PH{idx}\x00", placeholders[idx])
    return s


def render_inline_emph(escaped: str) -> str:
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def slugify_heading(text: str) -> str:
    clean = re.sub(r"`|\*\*|\*|\[([^\]]+)\]\([^)]+\)", r"\1", text)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", clean.lower()).strip("-")
    return slug or "section"


def markdown_to_html(md: str, source_md_rel: str, page_depth: int = 0) -> str:
    """Clean zero-dependency GFM -> HTML renderer."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Blank line
        if not stripped:
            i += 1
            continue

        # Special inline image embed marker in x-article.md: *[Embed Image: `01-open-issue-stress-test.png`]*
        embed_m = re.match(r"^\*\[Embed Image:\s*`([^`]+)`\]\*$", stripped)
        if embed_m:
            img_name = embed_m.group(1)
            prefix = "../" * page_depth
            out.append(
                f'<figure class="md-figure article-chart">'
                f'<img src="{prefix}assets/{html.escape(img_name)}" alt="{html.escape(img_name)}" loading="lazy">'
                f"</figure>"
            )
            i += 1
            continue

        # Fenced code block
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            code_lines: list[str] = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            cls = f' class="lang-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(code_lines))}</code></pre>")
            continue

        # Horizontal rule
        if re.match(r"^([-*_])\1{2,}$", stripped):
            out.append("<hr>")
            i += 1
            continue

        # Heading
        hm = re.match(r"^(#{1,6})\s+(.*)$", line)
        if hm:
            lvl = len(hm.group(1))
            raw = hm.group(2).strip()
            hid = slugify_heading(raw)
            out.append(f'<h{lvl} id="{hid}">{render_inline(raw, source_md_rel, page_depth)}</h{lvl}>')
            i += 1
            continue

        # Blockquote
        if stripped.startswith(">"):
            bq_lines: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                bq_lines.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            bq_html = "<br>".join(render_inline(l, source_md_rel, page_depth) for l in bq_lines if l)
            out.append(f"<blockquote><p>{bq_html}</p></blockquote>")
            continue

        # Table (header + separator row)
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]):
            def split_row(r: str) -> list[str]:
                r = r.strip()
                if r.startswith("|"):
                    r = r[1:]
                if r.endswith("|"):
                    r = r[:-1]
                return [c.strip() for c in r.split("|")]

            headers = split_row(line)
            aligns_raw = split_row(lines[i + 1])
            aligns: list[str] = []
            for a in aligns_raw:
                if a.startswith(":") and a.endswith(":"):
                    aligns.append("center")
                elif a.endswith(":"):
                    aligns.append("right")
                else:
                    aligns.append("left")
            i += 2
            rows: list[list[str]] = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1

            tbl = ['<div class="table-wrap"><table class="md-table"><thead><tr>']
            for idx, hcell in enumerate(headers):
                al = aligns[idx] if idx < len(aligns) else "left"
                tbl.append(f'<th style="text-align:{al}">{render_inline(hcell, source_md_rel, page_depth)}</th>')
            tbl.append("</tr></thead><tbody>")
            for row in rows:
                tbl.append("<tr>")
                for idx, cell in enumerate(row):
                    al = aligns[idx] if idx < len(aligns) else "left"
                    tbl.append(f'<td style="text-align:{al}">{render_inline(cell, source_md_rel, page_depth)}</td>')
                tbl.append("</tr>")
            tbl.append("</tbody></table></div>")
            out.append("".join(tbl))
            continue

        # Unordered or ordered list (with 1-level nesting support)
        if re.match(r"^\s*([-*+]|\d+\.)\s+", line):
            ordered = bool(re.match(r"^\s*\d+\.\s+", line))
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            while i < n and (re.match(r"^\s*([-*+]|\d+\.)\s+", lines[i]) or (lines[i].startswith("  ") and lines[i].strip())):
                cur = lines[i]
                lm = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", cur)
                if lm:
                    indent = len(lm.group(1))
                    content = render_inline(lm.group(3).strip(), source_md_rel, page_depth)
                    if indent >= 2 and items:
                        # Append nested bullet inside previous li
                        items[-1] += f'<div class="sub-item">• {content}</div>'
                    else:
                        items.append(content)
                elif items:
                    items[-1] += " " + render_inline(cur.strip(), source_md_rel, page_depth)
                i += 1
            li_html = "".join(f"<li>{it}</li>" for it in items)
            out.append(f"<{tag}>{li_html}</{tag}>")
            continue

        # Paragraph
        para_lines = [stripped]
        i += 1
        while (
            i < n
            and lines[i].strip()
            and not lines[i].strip().startswith(("#", ">", "```", "- ", "* ", "---", "***"))
            and not re.match(r"^\s*\d+\.\s+", lines[i])
            and not ("|" in lines[i] and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]))
        ):
            para_lines.append(lines[i].strip())
            i += 1
        out.append(f"<p>{render_inline(' '.join(para_lines), source_md_rel, page_depth)}</p>")

    return "\n".join(out)


SHARED_CSS = r"""
:root {
  --bg: #ffffff;
  --bg-subtle: #f8fafc;
  --bg-card: #ffffff;
  --bg-code: #f1f5f9;
  --ink: #0f172a;
  --body: #334155;
  --muted: #64748b;
  --faint: #94a3b8;
  --border: #e2e8f0;
  --border-strong: #cbd5e1;
  --emerald: #059669;
  --emerald-bg: #ecfdf5;
  --emerald-border: #a7f3d0;
  --sky: #0284c7;
  --sky-bg: #f0f9ff;
  --violet: #7c3aed;
  --violet-bg: #f5f3ff;
  --amber: #d97706;
  --amber-bg: #fffbeb;
  --coral: #dc2626;
  --coral-bg: #fef2f2;
  --shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 8px 24px rgba(15, 23, 42, 0.04);
  --font-sans: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}

[data-theme="dark"] {
  --bg: #0b0f17;
  --bg-subtle: #111827;
  --bg-card: #131926;
  --bg-code: #0f1623;
  --ink: #f3f6fc;
  --body: #cbd5e1;
  --muted: #94a3b8;
  --faint: #64748b;
  --border: #232d3f;
  --border-strong: #334155;
  --emerald: #10b981;
  --emerald-bg: rgba(16, 185, 129, 0.14);
  --emerald-border: rgba(16, 185, 129, 0.35);
  --sky: #38bdf8;
  --sky-bg: rgba(56, 189, 248, 0.14);
  --violet: #a78bfa;
  --violet-bg: rgba(167, 139, 250, 0.14);
  --amber: #f59e0b;
  --amber-bg: rgba(245, 158, 11, 0.14);
  --coral: #f87171;
  --coral-bg: rgba(248, 113, 113, 0.14);
  --shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 15.5px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}

a { color: var(--sky); text-decoration: none; }
a:hover { text-decoration: underline; }

.container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px;
}

.container-narrow {
  max-width: 860px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Navbar */
.nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}
.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  min-height: 60px;
  flex-wrap: wrap;
  padding: 8px 0;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--ink);
  font-weight: 700;
  font-size: 15.5px;
  letter-spacing: -0.01em;
}
.brand:hover { text-decoration: none; }
.brand-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: var(--ink);
  color: var(--bg);
  font-family: var(--font-mono);
  font-weight: 800;
  font-size: 13px;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.nav-links a {
  color: var(--muted);
  font-size: 13.5px;
  font-weight: 500;
  padding: 6px 10px;
  border-radius: 8px;
  transition: background 0.15s, color 0.15s;
}
.nav-links a:hover, .nav-links a.active {
  color: var(--ink);
  background: var(--bg-subtle);
  text-decoration: none;
}
.nav-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
.icon-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 11px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-subtle);
  color: var(--body);
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  font-family: var(--font-sans);
}
.icon-btn:hover { border-color: var(--border-strong); color: var(--ink); text-decoration: none; }

/* Hero */
.hero {
  padding: 56px 0 36px;
  border-bottom: 1px solid var(--border);
  background: radial-gradient(circle at 85% 15%, var(--emerald-bg), transparent 45%);
}
.eyebrow {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--emerald);
  text-transform: uppercase;
  margin-bottom: 14px;
}
.hero h1 {
  font-size: clamp(32px, 5vw, 52px);
  line-height: 1.08;
  letter-spacing: -0.03em;
  margin: 0 0 18px;
  max-width: 900px;
}
.hero-sub {
  font-size: 18px;
  color: var(--body);
  max-width: 760px;
  margin: 0 0 28px;
}
.cta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 36px;
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 18px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14.5px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: transform 0.1s, border-color 0.15s, background 0.15s;
}
.btn:hover { text-decoration: none; }
.btn-primary {
  background: var(--ink);
  color: var(--bg);
}
.btn-primary:hover { opacity: 0.92; }
.btn-secondary {
  background: var(--bg-card);
  color: var(--ink);
  border-color: var(--border-strong);
}
.btn-secondary:hover { background: var(--bg-subtle); }
.btn-emerald {
  background: var(--emerald-bg);
  color: var(--emerald);
  border-color: var(--emerald-border);
}

/* KPI Strip */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
}
.kpi {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  box-shadow: var(--shadow);
}
.kpi-val {
  font-family: var(--font-mono);
  font-size: 28px;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.02em;
}
.kpi-label {
  font-size: 13px;
  font-weight: 700;
  color: var(--emerald);
  margin-top: 6px;
}
.kpi-sub {
  font-size: 12px;
  color: var(--muted);
  margin-top: 2px;
}

/* Sections */
.section {
  padding: 52px 0;
  border-bottom: 1px solid var(--border);
}
.section-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}
.section-num {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.section h2 {
  font-size: clamp(22px, 3vw, 30px);
  letter-spacing: -0.02em;
  margin: 4px 0 0;
}
.section-desc {
  color: var(--muted);
  margin: 6px 0 0;
  max-width: 720px;
}

/* Explorer controls */
.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-bottom: 16px;
}
.search-input {
  flex: 1 1 260px;
  padding: 10px 14px;
  border-radius: 10px;
  border: 1px solid var(--border-strong);
  background: var(--bg-card);
  color: var(--ink);
  font-size: 14px;
  font-family: var(--font-sans);
}
.search-input:focus { outline: 2px solid var(--emerald); outline-offset: 1px; }
.pill-group {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.pill {
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--bg-subtle);
  color: var(--body);
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  font-family: var(--font-sans);
}
.pill.active {
  background: var(--ink);
  color: var(--bg);
  border-color: var(--ink);
}
.count-note {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--muted);
  margin-left: auto;
}

/* Explorer Table */
.table-wrap {
  width: 100%;
  overflow-x: auto;
  border: 1px solid var(--border);
  border-radius: 14px;
  background: var(--bg-card);
  box-shadow: var(--shadow);
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.4px;
}
th, td {
  padding: 10px 10px;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}
tbody tr:last-child td { border-bottom: none; }
thead th {
  background: var(--bg-subtle);
  color: var(--muted);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  white-space: nowrap;
  text-align: left;
}
th.sortable { cursor: pointer; user-select: none; }
th.sortable:hover { color: var(--ink); }
tbody tr:hover { background: var(--bg-subtle); }
.repo-cell { font-family: var(--font-mono); font-weight: 700; white-space: nowrap; }
.repo-cell a { color: var(--ink); }
.repo-cell a:hover { color: var(--emerald); }
.num { font-family: var(--font-mono); text-align: right; white-space: nowrap; }
.sig { color: var(--body); font-size: 12.8px; line-height: 1.45; }
.tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}
.tag-active { background: var(--emerald-bg); color: var(--emerald); border: 1px solid var(--emerald-border); }
.tag-archived { background: var(--coral-bg); color: var(--coral); border: 1px solid color-mix(in srgb, var(--coral) 30%, transparent); }
.tag-sunsetting { background: var(--amber-bg); color: var(--amber); border: 1px solid color-mix(in srgb, var(--amber) 30%, transparent); }
.tag-chunk { background: var(--bg-subtle); color: var(--muted); border: 1px solid var(--border); }

/* Cards & Grids */
.grid-3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
  box-shadow: var(--shadow);
}
.card-tag {
  display: inline-block;
  padding: 3px 9px;
  border-radius: 6px;
  font-family: var(--font-mono);
  font-size: 11.5px;
  font-weight: 700;
  margin-bottom: 10px;
}
.card h3 { margin: 0 0 8px; font-size: 17px; letter-spacing: -0.01em; }
.card p { margin: 0; color: var(--body); font-size: 14px; }

/* Bar Chart */
.chart-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 22px;
  box-shadow: var(--shadow);
}
.bar-row {
  display: grid;
  grid-template-columns: 185px 210px 1fr 110px;
  gap: 12px;
  align-items: center;
  padding: 9px 10px;
  border-radius: 10px;
}
.bar-row.highlight {
  background: var(--emerald-bg);
  border: 1px solid var(--emerald-border);
}
.bar-repo { font-family: var(--font-mono); font-weight: 700; font-size: 13.5px; }
.bar-meta { font-size: 12.5px; color: var(--muted); }
.bar-track {
  height: 16px;
  background: var(--bg-subtle);
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid var(--border);
}
.bar-fill { height: 100%; border-radius: 5px; }
.bar-val { font-family: var(--font-mono); font-weight: 800; font-size: 14px; text-align: right; }

/* Band items */
.band {
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: 14px;
  padding: 14px;
  border-radius: 11px;
  margin-top: 10px;
  border: 1px solid var(--border);
}
.band-num { font-family: var(--font-mono); font-size: 19px; font-weight: 800; align-self: center; }
.band-title { font-weight: 700; font-size: 13.5px; }
.band-desc { font-size: 13px; color: var(--body); margin-top: 3px; }

/* Prompt Box */
.prompt-wrap {
  background: var(--bg-card);
  border: 1px solid var(--border-strong);
  border-radius: 14px;
  overflow: hidden;
  box-shadow: var(--shadow);
}
.prompt-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 18px;
  background: var(--bg-subtle);
  border-bottom: 1px solid var(--border);
}
.prompt-pre {
  margin: 0;
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.6;
  overflow-x: auto;
  background: var(--bg-code);
  color: var(--ink);
  white-space: pre-wrap;
  word-break: break-word;
}

/* Assets Gallery */
.gallery {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 24px;
}
.gallery-item {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
}
.gallery-item img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  object-position: top;
  display: block;
  border-bottom: 1px solid var(--border);
}
.gallery-cap {
  padding: 12px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
}

/* Markdown Prose Pages */
.doc-header {
  padding: 36px 0 24px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 28px;
}
.breadcrumbs {
  font-family: var(--font-mono);
  font-size: 12.5px;
  color: var(--muted);
  margin-bottom: 12px;
}
.meta-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 16px;
}
.meta-chip {
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 11px;
  font-family: var(--font-mono);
  font-size: 12.5px;
  color: var(--body);
}
.meta-chip strong { color: var(--ink); }

.prose {
  padding-bottom: 64px;
}
.prose h1 { font-size: 32px; letter-spacing: -0.025em; margin: 0 0 16px; line-height: 1.15; }
.prose h2 { font-size: 23px; letter-spacing: -0.015em; margin: 36px 0 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
.prose h3 { font-size: 18px; margin: 26px 0 8px; }
.prose p { margin: 0 0 14px; color: var(--body); }
.prose ul, .prose ol { margin: 0 0 16px; padding-left: 22px; color: var(--body); }
.prose li { margin-bottom: 6px; }
.prose .sub-item { margin: 4px 0 0 12px; font-size: 14px; }
.prose code {
  font-family: var(--font-mono);
  font-size: 0.88em;
  background: var(--bg-code);
  padding: 2px 6px;
  border-radius: 5px;
  border: 1px solid var(--border);
  color: var(--ink);
}
.prose pre {
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  overflow-x: auto;
  margin: 0 0 18px;
}
.prose pre code {
  background: none;
  border: none;
  padding: 0;
  font-size: 13px;
  line-height: 1.55;
}
.prose blockquote {
  margin: 0 0 18px;
  padding: 12px 18px;
  border-left: 3px solid var(--emerald);
  background: var(--bg-subtle);
  border-radius: 0 10px 10px 0;
}
.prose blockquote p { margin: 0; color: var(--ink); }
.prose hr { border: none; border-top: 1px solid var(--border); margin: 28px 0; }
.prose .md-figure { margin: 22px 0; }
.prose .md-figure img {
  width: 100%;
  border-radius: 12px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}
.prose .table-wrap { margin: 18px 0 24px; }

/* Footer */
.footer {
  padding: 36px 0 48px;
  color: var(--muted);
  font-size: 13.5px;
}
.footer-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

@media (max-width: 960px) {
  .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .grid-3, .gallery { grid-template-columns: 1fr; }
  .grid-2 { grid-template-columns: 1fr; }
  .bar-row { grid-template-columns: 1fr; gap: 6px; }
  .bar-val { text-align: left; }
}
"""

THEME_SCRIPT = r"""
(function () {
  var saved = localStorage.getItem('theme');
  if (saved === 'dark' || saved === 'light') {
    document.documentElement.setAttribute('data-theme', saved);
  }
  window.toggleTheme = function () {
    var cur = document.documentElement.getAttribute('data-theme');
    var next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    var btn = document.getElementById('themeBtn');
    if (btn) btn.textContent = next === 'dark' ? '☀ Light' : '☾ Dark';
  };
  document.addEventListener('DOMContentLoaded', function () {
    var cur = document.documentElement.getAttribute('data-theme');
    var btn = document.getElementById('themeBtn');
    if (btn) btn.textContent = cur === 'dark' ? '☀ Light' : '☾ Dark';
  });
})();
"""


def page_shell(
    *,
    title: str,
    description: str,
    body_html: str,
    active_nav: str = "",
    depth: int = 0,
    extra_js: str = "",
) -> str:
    prefix = "../" * depth
    og_image = f"{SITE_URL}/assets/x-article-cover-light.png"
    nav_items = [
        ("index", f"{prefix}index.html", "Overview"),
        ("explorer", f"{prefix}index.html#explorer", "34 Repos"),
        ("playbook", f"{prefix}playbook.html", "Playbook"),
        ("brief", f"{prefix}brief.html", "Executive Brief"),
        ("article", f"{prefix}article.html", "Article"),
        ("prompt", f"{prefix}index.html#prompt", "Upgrade Prompt"),
    ]
    nav_html = "".join(
        f'<a href="{href}" class="{"active" if active_nav == key else ""}">{label}</a>'
        for key, href, label in nav_items
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="{og_image}">
  <link rel="stylesheet" href="{prefix}styles.css">
  <script>{THEME_SCRIPT}</script>
</head>
<body>
  <header class="nav">
    <div class="container nav-inner">
      <a class="brand" href="{prefix}index.html">
        <span class="brand-badge">34</span>
        <span>Agentic OSS Assessments</span>
      </a>
      <nav class="nav-links">{nav_html}</nav>
      <div class="nav-actions">
        <button id="themeBtn" class="icon-btn" type="button" onclick="toggleTheme()">☾ Dark</button>
        <a class="icon-btn" href="{REPO_URL}" target="_blank" rel="noopener noreferrer">GitHub ↗</a>
      </div>
    </div>
  </header>

  {body_html}

  <footer class="footer">
    <div class="container footer-inner">
      <div>Primary-source GitHub API audit · 34 repositories · 2.90M combined stars · Snapshot {SNAPSHOT_DATE}</div>
      <div>
        <a href="{prefix}playbook.html">Playbook</a> ·
        <a href="{prefix}brief.html">Brief</a> ·
        <a href="{prefix}article.html">Article</a> ·
        <a href="{REPO_URL}" target="_blank" rel="noopener noreferrer">Source & Raw JSONs ↗</a>
      </div>
    </div>
  </footer>
  {extra_js}
</body>
</html>
"""


def load_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for item in REPO_REGISTRY:
        data_file = ROOT / item["data_path"]
        raw = json.loads(data_file.read_text(encoding="utf-8"))
        meta = raw.get("meta", {})
        struct = raw.get("structure", {})
        cstats = raw.get("commit_stats_last_50", {})
        langs = raw.get("languages", {})
        top_lang = max(langs.items(), key=lambda kv: kv[1])[0] if langs else "Markdown"

        rec = dict(item)
        rec.update(
            {
                "stars": int(meta.get("stars", 0)),
                "forks": int(meta.get("forks", 0)),
                "open_issues": int(meta.get("open_issues", 0)),
                "archived": bool(meta.get("archived", False)),
                "description": meta.get("description") or "",
                "license": meta.get("license") or "—",
                "workflows": len(struct.get("workflows", [])),
                "top_lang": top_lang,
                "ai_pct": float(cstats.get("ai_coauthor_pct", 0.0)),
                "conv_pct": float(cstats.get("conventional_pct", 0.0)),
                "github_url": f"https://github.com/{item['repo']}",
                "raw_json_url": f"{REPO_URL}/blob/main/{item['data_path']}",
                "page_url": f"repos/{item['slug']}.html",
            }
        )
        records.append(rec)
    return records


def build_index(records: list[dict[str, Any]], prompt_text: str) -> str:
    total_stars = sum(r["stars"] for r in records)
    stars_str = f"{total_stars / 1_000_000:.2f}M"

    # Build JSON payload for client-side explorer
    client_rows = [
        {
            "slug": r["slug"],
            "repo": r["repo"],
            "chunk": r["chunk"],
            "chunkLabel": r["chunk_label"],
            "stars": r["stars"],
            "openIssues": r["open_issues"],
            "status": r["status"],
            "workflows": r["workflows"],
            "velocity": r["velocity"],
            "stack": r["stack"],
            "signature": r["signature"],
            "aiPct": r["ai_pct"],
            "convPct": r["conv_pct"],
            "pageUrl": r["page_url"],
            "githubUrl": r["github_url"],
        }
        for r in records
    ]

    issue_bars = [
        ("openai/codex", "136.4k★ · open tracker + bots", 28619, "var(--coral)", False),
        ("manaflow-ai/cmux", "29.0k★ · autonomous agent factory", 11218, "#ea580c", False),
        ("openclaw/openclaw", "395.2k★ · 20-PR cap + sweepers", 9182, "var(--amber)", False),
        ("pingdotgg/t3code", "78.8k★ · VOUCHED.td + PR caps", 3681, "var(--sky)", False),
        ("obra/superpowers", "326.5k★ · 94% PR reject policy", 372, "var(--emerald)", False),
        ("earendil-works/pi", "123.8k★ · default-closed lgtmi/lgtm", 307, "var(--emerald)", True),
    ]
    bars_html = []
    for repo_name, meta_txt, count, color, hi in issue_bars:
        pct = max(1.6, (count / 28619.0) * 100.0)
        badge = ' <span class="tag tag-active">93× FEWER</span>' if hi else ""
        bars_html.append(
            f'<div class="bar-row{" highlight" if hi else ""}">'
            f'<div class="bar-repo">{repo_name}</div>'
            f'<div class="bar-meta">{meta_txt}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct:.2f}%;background:{color}"></div></div>'
            f'<div class="bar-val" style="color:{color}">{count:,}{badge}</div>'
            f"</div>"
        )

    chunk_links = "".join(
        f'<a class="pill" href="chunks/{cid}.html">{html.escape(label)} →</a>'
        for cid, label, _ in CHUNK_SUMMARIES
    )

    body = f"""
  <section class="hero">
    <div class="container">
      <div class="eyebrow">Primary-Source GitHub API Audit · {len(records)} Repos · {stars_str} Combined Stars · {SNAPSHOT_DATE}</div>
      <h1>How Top Agentic OSS Repos Stay Fast Without Melting Down.</h1>
      <p class="hero-sub">
        Real receipts from inspecting the actual <code>AGENTS.md</code> files, custom linter plugins, CI workflows, dependency locks, eval labs, and recent commits across <strong>{len(records)} open-source coding harnesses, orchestrators, and skill stacks</strong>.
      </p>
      <div class="cta-row">
        <a class="btn btn-primary" href="#prompt">Copy Repo Upgrade Prompt ↓</a>
        <a class="btn btn-secondary" href="#explorer">Explore All {len(records)} Repos</a>
        <a class="btn btn-emerald" href="playbook.html">Read Full Playbook →</a>
        <a class="btn btn-secondary" href="article.html">Read Long-Form Article</a>
      </div>

      <div class="kpi-grid">
        <div class="kpi">
          <div class="kpi-val">{len(records)}</div>
          <div class="kpi-label">repos audited</div>
          <div class="kpi-sub">6 chunks + t3code baseline</div>
        </div>
        <div class="kpi">
          <div class="kpi-val">{stars_str}</div>
          <div class="kpi-label">combined stars</div>
          <div class="kpi-sub">1.73M harnesses + 1.17M skills</div>
        </div>
        <div class="kpi">
          <div class="kpi-val">93×</div>
          <div class="kpi-label">open-issue gap</div>
          <div class="kpi-sub">pi (307) vs. codex (28,619)</div>
        </div>
        <div class="kpi">
          <div class="kpi-val">58 vs 61</div>
          <div class="kpi-label">gstack self-eval</div>
          <div class="kpi-sub">skills ≠ higher raw fix rate</div>
        </div>
        <div class="kpi">
          <div class="kpi-val">4 / 34</div>
          <div class="kpi-label">archived / sunset</div>
          <div class="kpi-sub">sprawl, weak gates & supply chain</div>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 1: INTERACTIVE 34-REPO EXPLORER -->
  <section class="section" id="explorer">
    <div class="container">
      <div class="section-head">
        <div>
          <div class="section-num">Section 01 · Interactive Dataset</div>
          <h2>Explore All {len(records)} Audited Repositories</h2>
          <p class="section-desc">Search by repo, stack, or engineering practice. Click column headers to sort. Open any row for the complete primary-source assessment.</p>
        </div>
      </div>

      <div class="controls">
        <input id="searchBox" class="search-input" type="search" placeholder="Filter by repo, stack, oxlint, TLA+, gh-aw, sandcastle, gstack...">
        <div class="pill-group" id="chunkFilters">
          <button class="pill active" data-chunk="ALL">All ({len(records)})</button>
          <button class="pill" data-chunk="Base">Base</button>
          <button class="pill" data-chunk="C1">C1 Rivals</button>
          <button class="pill" data-chunk="C2">C2 Harnesses</button>
          <button class="pill" data-chunk="C3">C3 Autonomous</button>
          <button class="pill" data-chunk="C4">C4 Orchestration</button>
          <button class="pill" data-chunk="C5">C5 Specialists</button>
          <button class="pill" data-chunk="C6">C6 Skill Stacks</button>
        </div>
        <div class="pill-group" id="statusFilters">
          <button class="pill active" data-status="ALL">Any Status</button>
          <button class="pill" data-status="Active">Active</button>
          <button class="pill" data-status="DEAD">Archived / Sunset</button>
        </div>
        <span class="count-note" id="rowCount">{len(records)} repos</span>
      </div>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Chunk</th>
              <th>Repository</th>
              <th class="sortable num" data-sort="stars">Stars ↕</th>
              <th class="sortable num" data-sort="openIssues">Open Issues ↕</th>
              <th>Status</th>
              <th class="sortable num" data-sort="workflows">Workflows ↕</th>
              <th class="sortable num" data-sort="aiPct">AI Signal ↕</th>
              <th>Signature Practice</th>
              <th>Audit</th>
            </tr>
          </thead>
          <tbody id="repoTbody"></tbody>
        </table>
      </div>

      <div style="margin-top:16px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;">
        <span style="font-size:12.5px;color:var(--muted);font-weight:600;">Chunk Summaries:</span>
        {chunk_links}
      </div>
    </div>
  </section>

  <!-- SECTION 2: SKILL STACKS VS MECHANICAL REALITY -->
  <section class="section" id="findings">
    <div class="container">
      <div class="section-head">
        <div>
          <div class="section-num">Section 02 · Chunk 6 Spotlight</div>
          <h2>Skill Stacks Organize Workflow — Mechanical Gates Drive Reliability</h2>
          <p class="section-desc">Auditing the 10 largest agent skill, spec, and sandbox repos (1.17M★) produced the clearest empirical reality check in the study.</p>
        </div>
      </div>

      <div class="grid-3">
        <div class="card">
          <span class="card-tag" style="background:var(--amber-bg);color:var(--amber)">gstack · 142.6k★ self-eval</span>
          <h3>58 vs. 61/99 bugs fixed</h3>
          <p>In its own README benchmark, Opus 5.5 solved 58 tasks with <code>gstack</code> vs. 61/99 without it (29 vs. 29 on security fixes). Use skill stacks for workflow, token budgets (<code>catalog-budget.test.ts</code>), and egress receipts — not raw fix rate. <a href="repos/gstack.html">Read audit →</a></p>
        </div>
        <div class="card">
          <span class="card-tag" style="background:var(--emerald-bg);color:var(--emerald)">mattpocock · skills & sandcastle</span>
          <h3>Fresh context + automated shrink bot</h3>
          <p><code>skills</code> (332.8k★) enforces fresh-context subagents and frontmatter YAML tests. <code>sandcastle</code> (9.3k★) is the cleanest small repo in the study: all-5-category type-aware <code>oxlint</code> + automated <code>lint-shrink.yml</code> ratchet PR bot + real <code>bwrap</code> CI. <a href="repos/mattpocock-sandcastle.html">Read audit →</a></p>
        </div>
        <div class="card">
          <span class="card-tag" style="background:var(--violet-bg);color:var(--violet)">superpowers & pstack · 336k★</span>
          <h3>94% PR reject · TLA+/Lean skills</h3>
          <p><code>obra/superpowers</code> states a <strong>94% PR rejection rate</strong> on line 1 of <code>AGENTS.md</code> and backs changes with a real-CLI eval lab. <code>pstack</code> ships <code>/create-formal-verification-skill</code> generating project-local TLA+ (49 KB) &amp; Lean (52 KB) skills. <a href="repos/pstack-claude.html">Read audit →</a></p>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 3: OPEN-ISSUE STRESS TEST -->
  <section class="section">
    <div class="container">
      <div class="section-head">
        <div>
          <div class="section-num">Section 03 · Governance</div>
          <h2>The Open-Issue Stress Test</h2>
          <p class="section-desc">When anyone can prompt an agent to open a PR in 90 seconds, open-by-default trackers drown. Default-closed contributor gating cuts backlog by 93×.</p>
        </div>
      </div>
      <div class="chart-card">
        {"".join(bars_html)}
      </div>
    </div>
  </section>

  <!-- SECTION 4: CI GOLDILOCKS ZONE & 4 POSTMORTEMS -->
  <section class="section">
    <div class="container">
      <div class="section-head">
        <div>
          <div class="section-num">Section 04 · Survival Mechanics</div>
          <h2>The CI Goldilocks Zone &amp; What Killed 4 Repos</h2>
          <p class="section-desc">Too few workflows invite rot; too many consume the engineering team. Scope sprawl and supply-chain gaps finish the job.</p>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="section-num" style="margin-bottom:8px">GitHub Actions Workflows vs. Reality</div>
          <div class="band" style="background:var(--coral-bg)">
            <div class="band-num" style="color:var(--coral)">0–1</div>
            <div>
              <div class="band-title">1code (0) · superpowers (0) · happy (1)</div>
              <div class="band-desc">Zero PR CI killed <code>1code</code> in 7 weeks; <code>superpowers</code> survives via 94% PR rejection + external eval lab; <code>happy</code> relies on a 2-person core.</div>
            </div>
          </div>
          <div class="band" style="background:var(--emerald-bg);border-color:var(--emerald-border)">
            <div class="band-num" style="color:var(--emerald)">8–30</div>
            <div>
              <div class="band-title">sandcastle (8) · paseo (12) · pi (16) · opencode (21) · OpenHands (25) · t3code (29)</div>
              <div class="band-desc">Sweet spot: path-filtered CI + one <code>if: always()</code> aggregator + fast local diff-scoped checker + 7-day npm cooldown.</div>
            </div>
          </div>
          <div class="band" style="background:var(--amber-bg)">
            <div class="band-num" style="color:var(--amber)">133–231</div>
            <div>
              <div class="band-title">openclaw (133) · cmux (231)</div>
              <div class="band-desc">CI factory tax: ~80% of <code>cmux</code>'s sampled <code>main</code> commits repair runner pools and autofixers while open issues hit 11,218.</div>
            </div>
          </div>
        </div>

        <div class="card" style="background:color-mix(in srgb, var(--coral-bg) 45%, var(--bg-card))">
          <div class="section-num" style="color:var(--coral);margin-bottom:10px">4 Repos Archived or Sunsetting</div>
          <div style="display:flex;flex-direction:column;gap:14px;">
            <div>
              <strong><a href="repos/1code.html">21st-dev/1code</a> (5.6k★ · Archived)</strong>
              <p>Zero CI, zero linter, zero tests, dual lockfiles, one-way mirror, stale WIP docs. Public life: 7 weeks.</p>
            </div>
            <div>
              <strong><a href="repos/vibe-kanban.html">BloopAI/vibe-kanban</a> (28.8k★ · Sunsetting)</strong>
              <p>Strong Rust craft crushed by 30 crates + ElectricSQL + WebRTC relay + Tauri + Rust nightly on a 4-person team.</p>
            </div>
            <div>
              <strong><a href="repos/roo-code.html">RooCodeInc/Roo-Code</a> (24.2k★ · Archived May '26)</strong>
              <p>Coupled to a VS Code extension while surviving peers decoupled into multi-surface SDKs and ACP control planes.</p>
            </div>
            <div>
              <strong><a href="repos/get-shit-done.html">gsd-build/get-shit-done</a> (64.1k★ · Archived May '26)</strong>
              <p>Hit a compromise warning right in git history (<code>126b6b9e</code>) and migrated to <code>open-gsd/gsd-core</code>. Prompt packages need supply-chain discipline too.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 5: COPY-PASTE REPO UPGRADE PROMPT + VISUAL CARDS -->
  <section class="section" id="prompt">
    <div class="container">
      <div class="section-head">
        <div>
          <div class="section-num">Section 05 · Actionable Prompt &amp; Shareable Cards</div>
          <h2>Drop This Prompt Into Your Coding Agent</h2>
          <p class="section-desc">Paste straight into T3 Code, Claude Code, Codex, OpenCode, or Pi to audit your repository and ship the highest-ROI Week 1 guardrails.</p>
        </div>
      </div>

      <div class="prompt-wrap">
        <div class="prompt-bar">
          <span style="font-family:var(--font-mono);font-size:12.5px;font-weight:700;color:var(--muted)">distribution/upgrade-prompt.txt · 34-repo playbook</span>
          <button id="copyPromptBtn" class="btn btn-primary" style="padding:7px 14px;font-size:13px" type="button" onclick="copyUpgradePrompt()">Copy Prompt</button>
        </div>
        <pre id="upgradePromptPre" class="prompt-pre">{html.escape(prompt_text)}</pre>
      </div>

      <div class="gallery">
        <a class="gallery-item" href="assets/x-card-1-prompt.png" target="_blank">
          <img src="assets/x-card-1-prompt.png" alt="Research Note Prompt Card" loading="lazy">
          <div class="gallery-cap"><span>Research Note · Prompt Card</span><span>Open PNG ↗</span></div>
        </a>
        <a class="gallery-item" href="assets/x-card-2-infographic.png" target="_blank">
          <img src="assets/x-card-2-infographic.png" alt="Research Note 34-Repo Infographic" loading="lazy">
          <div class="gallery-cap"><span>Research Note · 34-Repo Infographic</span><span>Open PNG ↗</span></div>
        </a>
        <a class="gallery-item" href="assets/x-article-cover-light.png" target="_blank">
          <img src="assets/x-article-cover-light.png" alt="X Article Light Cover" loading="lazy">
          <div class="gallery-cap"><span>Editorial Cover · 16:9 Light</span><span>Open PNG ↗</span></div>
        </a>
      </div>
    </div>
  </section>
"""

    extra_js = f"""
  <script>
    const REPOS = {json.dumps(client_rows)};
    let activeChunk = 'ALL';
    let activeStatus = 'ALL';
    let sortKey = 'stars';
    let sortDir = -1;

    function fmtStars(n) {{
      if (n >= 1000000) return (n / 1000000).toFixed(2) + 'M';
      if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
      return String(n);
    }}

    function statusTag(s) {{
      if (s === 'Active') return '<span class="tag tag-active">Active</span>';
      if (s === 'Archived') return '<span class="tag tag-archived">Archived</span>';
      return '<span class="tag tag-sunsetting">' + s + '</span>';
    }}

    function renderRows() {{
      const q = (document.getElementById('searchBox').value || '').toLowerCase().trim();
      const filtered = REPOS.filter(r => {{
        if (activeChunk !== 'ALL' && r.chunk !== activeChunk) return false;
        if (activeStatus === 'Active' && r.status !== 'Active') return false;
        if (activeStatus === 'DEAD' && r.status === 'Active') return false;
        if (q) {{
          const hay = (r.repo + ' ' + r.stack + ' ' + r.signature + ' ' + r.chunkLabel).toLowerCase();
          if (!hay.includes(q)) return false;
        }}
        return true;
      }});

      filtered.sort((a, b) => ((a[sortKey] || 0) - (b[sortKey] || 0)) * sortDir);

      const tbody = document.getElementById('repoTbody');
      tbody.innerHTML = filtered.map(r => `
        <tr>
          <td><span class="tag tag-chunk">${{r.chunk}}</span></td>
          <td class="repo-cell"><a href="${{r.pageUrl}}">${{r.repo}}</a></td>
          <td class="num"><strong>${{fmtStars(r.stars)}}</strong></td>
          <td class="num">${{r.openIssues.toLocaleString()}}</td>
          <td>${{statusTag(r.status)}}</td>
          <td class="num">${{r.workflows}}</td>
          <td class="num">${{Math.round(r.aiPct)}}%</td>
          <td class="sig">${{r.signature}}</td>
          <td style="white-space:nowrap"><a href="${{r.pageUrl}}">Read →</a></td>
        </tr>
      `).join('');

      document.getElementById('rowCount').textContent = filtered.length + ' of ' + REPOS.length + ' repos';
    }}

    document.getElementById('searchBox').addEventListener('input', renderRows);
    document.querySelectorAll('#chunkFilters .pill').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('#chunkFilters .pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeChunk = btn.dataset.chunk;
        renderRows();
      }});
    }});
    document.querySelectorAll('#statusFilters .pill').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('#statusFilters .pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeStatus = btn.dataset.status;
        renderRows();
      }});
    }});
    document.querySelectorAll('th.sortable').forEach(th => {{
      th.addEventListener('click', () => {{
        const key = th.dataset.sort;
        if (sortKey === key) sortDir *= -1;
        else {{ sortKey = key; sortDir = -1; }}
        renderRows();
      }});
    }});

    window.copyUpgradePrompt = function () {{
      const txt = document.getElementById('upgradePromptPre').textContent;
      navigator.clipboard.writeText(txt).then(() => {{
        const btn = document.getElementById('copyPromptBtn');
        btn.textContent = '✓ Copied to clipboard';
        setTimeout(() => {{ btn.textContent = 'Copy Prompt'; }}, 2200);
      }});
    }};

    renderRows();
  </script>
"""

    return page_shell(
        title="Agentic OSS Assessments — 34 AI Coding Repos (2.90M Stars)",
        description="Primary-source GitHub API audit of 34 open-source AI coding harnesses, orchestrators, and skill stacks (2.90M combined stars).",
        body_html=body,
        active_nav="index",
        depth=0,
        extra_js=extra_js,
    )


def build_doc_page(
    *,
    md_rel: str,
    title: str,
    eyebrow: str,
    active_nav: str,
    depth: int = 0,
    extra_meta_html: str = "",
) -> str:
    md_text = (ROOT / md_rel).read_text(encoding="utf-8")
    content_html = markdown_to_html(md_text, md_rel, page_depth=depth)
    prefix = "../" * depth
    body = f"""
  <main class="container-narrow">
    <div class="doc-header">
      <div class="breadcrumbs"><a href="{prefix}index.html">← All 34 Repos</a> · {html.escape(eyebrow)}</div>
      {extra_meta_html}
    </div>
    <article class="prose">
      {content_html}
    </article>
  </main>
"""
    return page_shell(
        title=f"{title} — Agentic OSS Assessments",
        description=f"Primary-source engineering assessment: {title}",
        body_html=body,
        active_nav=active_nav,
        depth=depth,
    )


def build_repo_page(r: dict[str, Any]) -> str:
    status_cls = "tag-active" if r["status"] == "Active" else ("tag-archived" if r["status"] == "Archived" else "tag-sunsetting")
    meta_html = f"""
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
        <div>
          <span class="tag tag-chunk">{html.escape(r['chunk_label'])}</span>
          <span class="tag {status_cls}" style="margin-left:6px">{html.escape(r['status'])}</span>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <a class="icon-btn" href="{r['github_url']}" target="_blank" rel="noopener noreferrer">GitHub Repo ↗</a>
          <a class="icon-btn" href="{r['raw_json_url']}" target="_blank" rel="noopener noreferrer">Raw JSON Snapshot ↗</a>
        </div>
      </div>
      <div class="meta-strip">
        <span class="meta-chip">Stars: <strong>{fmt_stars(r['stars'])}</strong> ({fmt_int(r['stars'])})</span>
        <span class="meta-chip">Open Issues: <strong>{fmt_int(r['open_issues'])}</strong></span>
        <span class="meta-chip">Workflows: <strong>{r['workflows']}</strong></span>
        <span class="meta-chip">AI Signal: <strong>{r['ai_pct']:.0f}%</strong></span>
        <span class="meta-chip">Conv. Commits: <strong>{r['conv_pct']:.0f}%</strong></span>
        <span class="meta-chip">Velocity: <strong>{html.escape(r['velocity'])}</strong></span>
      </div>
"""
    return build_doc_page(
        md_rel=r["md_path"],
        title=r["repo"],
        eyebrow=f"{r['chunk_label']} · {r['repo']}",
        active_nav="explorer",
        depth=1,
        extra_meta_html=meta_html,
    )


def main() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    (DOCS / "repos").mkdir(parents=True)
    (DOCS / "chunks").mkdir(parents=True)
    (DOCS / "assets").mkdir(parents=True)

    # .nojekyll so GitHub Pages serves static HTML cleanly
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    (DOCS / "styles.css").write_text(SHARED_CSS.strip() + "\n", encoding="utf-8")

    # Copy distribution PNG assets
    for png in sorted((ROOT / "distribution" / "assets").glob("*.png")):
        shutil.copy2(png, DOCS / "assets" / png.name)

    records = load_records()
    prompt_text = (ROOT / "distribution" / "upgrade-prompt.txt").read_text(encoding="utf-8").strip()

    # Main landing page
    (DOCS / "index.html").write_text(build_index(records, prompt_text), encoding="utf-8")

    # Core synthesis & article pages
    (DOCS / "playbook.html").write_text(
        build_doc_page(
            md_rel="synthesis/PLAYBOOK.md",
            title="Agentic OSS Engineering Playbook",
            eyebrow="Synthesis · Master Playbook",
            active_nav="playbook",
            depth=0,
        ),
        encoding="utf-8",
    )
    (DOCS / "brief.html").write_text(
        build_doc_page(
            md_rel="synthesis/EXECUTIVE_BRIEF.md",
            title="Executive Brief (34 Repos)",
            eyebrow="Synthesis · 5-Minute Executive Brief",
            active_nav="brief",
            depth=0,
        ),
        encoding="utf-8",
    )
    (DOCS / "article.html").write_text(
        build_doc_page(
            md_rel="distribution/x-article.md",
            title="I Audited 34 Open-Source AI Coding Repos (2.90M Stars)",
            eyebrow="Long-Form Article",
            active_nav="article",
            depth=0,
        ),
        encoding="utf-8",
    )

    # Chunk summaries
    for cid, label, md_rel in CHUNK_SUMMARIES:
        (DOCS / "chunks" / f"{cid}.html").write_text(
            build_doc_page(
                md_rel=md_rel,
                title=label,
                eyebrow=label,
                active_nav="explorer",
                depth=1,
            ),
            encoding="utf-8",
        )

    # All 34 individual repository pages
    for r in records:
        (DOCS / "repos" / f"{r['slug']}.html").write_text(build_repo_page(r), encoding="utf-8")

    print(f"Built static site in {DOCS} ({len(records)} repo pages + 6 chunk summaries + 4 core pages)")


if __name__ == "__main__":
    main()
