#!/usr/bin/env python3
"""Collect primary-source GitHub metadata, key agent/CI/lint files, and recent commits for a chunk of repos."""

from __future__ import annotations

import base64
import concurrent.futures
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

KEY_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "README.md",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "mix.exs",
    "pyproject.toml",
    "biome.json",
    "biome.jsonc",
    ".oxlintrc.json",
    "oxlint.json",
    "knip.json",
    "knip.jsonc",
    "turbo.json",
    "pnpm-workspace.yaml",
    "WORKFLOW.md",
    "SOUL.md",
]

AI_COAUTHOR_RE = re.compile(
    r"(co-authored-by:.*(claude|anthropic|codex|openai|cursor|copilot|gemini|devin|aider|amp|factory|droid|bot|\[bot\]))|"
    r"(generated with.*claude|🤖)",
    re.IGNORECASE,
)
FIX_REVERT_RE = re.compile(r"^(fix|revert|hotfix)(\(|:|\s)", re.IGNORECASE)
CONVENTIONAL_RE = re.compile(
    r"^(feat|fix|chore|docs|refactor|test|ci|build|perf|style|revert)(\([^)]+\))?!?: "
)


def gh_api(endpoint: str) -> Any:
    proc = subprocess.run(
        ["gh", "api", endpoint],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def fetch_file(repo: str, path: str, max_chars: int = 12000) -> dict[str, Any] | None:
    data = gh_api(f"repos/{repo}/contents/{path}")
    if not isinstance(data, dict) or data.get("type") != "file":
        return None
    raw_b64 = data.get("content", "")
    try:
        text = base64.b64decode(raw_b64).decode("utf-8", errors="replace")
    except Exception:
        text = ""
    lines = text.splitlines()
    return {
        "path": path,
        "size_bytes": data.get("size", len(text.encode("utf-8"))),
        "line_count": len(lines),
        "truncated": len(text) > max_chars,
        "excerpt": text[:max_chars],
    }


def list_dir(repo: str, path: str) -> list[str]:
    data = gh_api(f"repos/{repo}/contents/{path}")
    if not isinstance(data, list):
        return []
    return sorted(
        f"{item['name']}/" if item.get("type") == "dir" else item["name"]
        for item in data
        if isinstance(item, dict) and "name" in item
    )


def collect_repo(repo: str) -> dict[str, Any]:
    meta = gh_api(f"repos/{repo}") or {}
    canonical = meta.get("full_name", repo)
    default_branch = meta.get("default_branch", "main")

    languages = gh_api(f"repos/{canonical}/languages") or {}
    top_tree = list_dir(canonical, "")
    workflows = [
        w for w in list_dir(canonical, ".github/workflows") if w.endswith((".yml", ".yaml"))
    ]
    docs_dir = list_dir(canonical, "docs")
    agents_dir = list_dir(canonical, ".agents")
    agents_skills = list_dir(canonical, ".agents/skills")
    claude_dir = list_dir(canonical, ".claude")
    cursor_dir = list_dir(canonical, ".cursor")
    evals_dir = list_dir(canonical, "evals")

    # Fetch existing key files found in root (plus README/AGENTS/CLAUDE)
    root_names = {entry.rstrip("/") for entry in top_tree}
    files_to_fetch = [f for f in KEY_FILES if f in root_names]
    key_files: dict[str, Any] = {}
    for f in files_to_fetch:
        limit = 16000 if f in ("AGENTS.md", "CLAUDE.md", "WORKFLOW.md") else 6000
        info = fetch_file(canonical, f, max_chars=limit)
        if info:
            key_files[f] = info

    # Also grab up to 3 interesting CI workflows (ci, test, lint, pr, review)
    workflow_samples: dict[str, Any] = {}
    priority_wf = [
        w for w in workflows
        if any(k in w.lower() for k in ("ci", "test", "lint", "check", "pr", "review", "eval", "triage"))
    ][:4]
    for wf in priority_wf:
        info = fetch_file(canonical, f".github/workflows/{wf}", max_chars=4500)
        if info:
            workflow_samples[wf] = info

    # Recent 50 commits on default branch
    commits_raw = gh_api(f"repos/{canonical}/commits?sha={default_branch}&per_page=50") or []
    commits: list[dict[str, Any]] = []
    ai_coauthor_count = 0
    fix_revert_count = 0
    conventional_count = 0
    author_counts: dict[str, int] = {}
    for c in commits_raw if isinstance(commits_raw, list) else []:
        msg = (c.get("commit", {}) or {}).get("message", "")
        first_line = msg.splitlines()[0] if msg else ""
        author = ((c.get("author") or {}).get("login")) or ((c.get("commit", {}) or {}).get("author", {}) or {}).get("name", "unknown")
        date = ((c.get("commit", {}) or {}).get("author", {}) or {}).get("date", "")
        has_ai = bool(AI_COAUTHOR_RE.search(msg))
        if has_ai:
            ai_coauthor_count += 1
        if FIX_REVERT_RE.search(first_line):
            fix_revert_count += 1
        if CONVENTIONAL_RE.search(first_line):
            conventional_count += 1
        author_counts[author] = author_counts.get(author, 0) + 1
        commits.append({
            "sha": (c.get("sha") or "")[:8],
            "date": date,
            "author": author,
            "subject": first_line[:140],
            "ai_signal": has_ai,
        })

    # Top contributors
    contributors_raw = gh_api(f"repos/{canonical}/contributors?per_page=10") or []
    top_contributors = [
        {"login": x.get("login"), "contributions": x.get("contributions")}
        for x in (contributors_raw if isinstance(contributors_raw, list) else [])
        if isinstance(x, dict)
    ]

    # Recent releases (up to 5)
    releases_raw = gh_api(f"repos/{canonical}/releases?per_page=5") or []
    recent_releases = [
        {"tag": r.get("tag_name"), "published_at": r.get("published_at"), "name": r.get("name")}
        for r in (releases_raw if isinstance(releases_raw, list) else [])
        if isinstance(r, dict)
    ]

    return {
        "repo": canonical,
        "meta": {
            "description": meta.get("description"),
            "homepage": meta.get("homepage"),
            "license": (meta.get("license") or {}).get("spdx_id"),
            "stars": meta.get("stargazers_count"),
            "forks": meta.get("forks_count"),
            "open_issues": meta.get("open_issues_count"),
            "archived": meta.get("archived"),
            "created_at": meta.get("created_at"),
            "pushed_at": meta.get("pushed_at"),
            "default_branch": default_branch,
            "topics": meta.get("topics", []),
        },
        "languages": languages,
        "structure": {
            "root": top_tree,
            "workflows": workflows,
            "docs": docs_dir[:50],
            "docs_count": len(docs_dir),
            "agents_dir": agents_dir,
            "agents_skills": agents_skills,
            "claude_dir": claude_dir,
            "cursor_dir": cursor_dir,
            "evals_dir": evals_dir,
        },
        "key_files": key_files,
        "workflow_samples": workflow_samples,
        "commit_stats_last_50": {
            "count": len(commits),
            "date_span": {
                "newest": commits[0]["date"] if commits else None,
                "oldest": commits[-1]["date"] if commits else None,
            },
            "conventional_pct": round(100 * conventional_count / len(commits), 1) if commits else 0,
            "fix_revert_pct": round(100 * fix_revert_count / len(commits), 1) if commits else 0,
            "ai_coauthor_pct": round(100 * ai_coauthor_count / len(commits), 1) if commits else 0,
            "top_recent_authors": sorted(author_counts.items(), key=lambda kv: -kv[1])[:8],
            "sample_commits": commits[:20],
        },
        "top_contributors": top_contributors,
        "recent_releases": recent_releases,
    }


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: collect_chunk.py <output_dir> <owner/repo> [owner/repo ...]", file=sys.stderr)
        sys.exit(1)
    out_dir = Path(sys.argv[1])
    repos = sys.argv[2:]
    out_dir.mkdir(parents=True, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(collect_repo, r): r for r in repos}
        for fut in concurrent.futures.as_completed(futures):
            r = futures[fut]
            data = fut.result()
            slug = data["repo"].replace("/", "__")
            out_path = out_dir / f"{slug}.json"
            out_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            m = data["meta"]
            cs = data["commit_stats_last_50"]
            print(
                f"Collected {data['repo']}: ★{m['stars']} | archived={m['archived']} | "
                f"workflows={len(data['structure']['workflows'])} | "
                f"key_files={list(data['key_files'].keys())} | "
                f"last50: conv={cs['conventional_pct']}% fix={cs['fix_revert_pct']}% ai={cs['ai_coauthor_pct']}%"
            )


if __name__ == "__main__":
    main()
