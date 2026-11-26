#!/usr/bin/env python3
"""Path-scoped variant of scripts/collect_chunk.py.

collect_chunk.py takes owner/repo and attributes repo-wide stars, workflows,
languages, contributors, and commits to that repo. That is misleading for a
plugin that lives in a monorepo path such as cursor/plugins/pstack.

Usage:
  python3 scripts/collect_path.py <out_dir> <owner/repo> <path>
  python3 scripts/collect_path.py data/chunk-06 cursor/plugins pstack

Use this instead of collect_chunk.py when the subject is a subdirectory of a
monorepo (for example cursor/plugins/pstack). collect_chunk.py attributes
repo-wide stars, forks, issues, languages, workflows, and unfiltered commits
to the whole repository, which is misleading for a single plugin path.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Reuse helpers from collect_chunk.py in this directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect_chunk import (  # type: ignore
    AI_COAUTHOR_RE,
    CONVENTIONAL_RE,
    FIX_REVERT_RE,
    fetch_file,
    gh_api,
    list_dir,
)


def commits_for_path(repo: str, path: str, per_page: int = 50) -> list[dict]:
    data = gh_api(f"repos/{repo}/commits?path={path}&per_page={per_page}") or []
    return data if isinstance(data, list) else []


def collect_path(repo: str, path: str) -> dict:
    meta = gh_api(f"repos/{repo}") or {}
    canonical = meta.get("full_name", repo)
    default_branch = meta.get("default_branch", "main")
    prefix = path.strip("/")

    top_tree = list_dir(canonical, prefix)
    plugin = fetch_file(canonical, f"{prefix}/plugin.json", max_chars=4000)
    readme = fetch_file(canonical, f"{prefix}/README.md", max_chars=8000)
    license_f = fetch_file(canonical, f"{prefix}/LICENSE", max_chars=2000)
    skills = [s.rstrip("/") for s in list_dir(canonical, f"{prefix}/skills")]

    tree = gh_api(f"repos/{canonical}/git/trees/{default_branch}?recursive=1") or {}
    blobs = [
        t
        for t in (tree.get("tree") or [])
        if t.get("type") == "blob" and str(t.get("path", "")).startswith(prefix + "/")
    ]
    ext_bytes: dict[str, int] = {}
    ext_count: dict[str, int] = {}
    for t in blobs:
        name = str(t.get("path", "")).rsplit("/", 1)[-1]
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else "(noext)"
        size = int(t.get("size") or 0)
        ext_bytes[ext] = ext_bytes.get(ext, 0) + size
        ext_count[ext] = ext_count.get(ext, 0) + 1

    commits_raw = commits_for_path(canonical, prefix, 50)
    commits = []
    ai = fix = conv = 0
    authors: dict[str, int] = {}
    for c in commits_raw:
        msg = (c.get("commit") or {}).get("message", "")
        first = msg.splitlines()[0] if msg else ""
        author = ((c.get("author") or {}) or {}).get("login") or (
            ((c.get("commit") or {}).get("author") or {}).get("name", "unknown")
        )
        date = (((c.get("commit") or {}).get("author") or {}).get("date", ""))
        has_ai = bool(AI_COAUTHOR_RE.search(msg))
        if has_ai:
            ai += 1
        if FIX_REVERT_RE.search(first):
            fix += 1
        if CONVENTIONAL_RE.search(first):
            conv += 1
        authors[author] = authors.get(author, 0) + 1
        commits.append(
            {
                "sha": (c.get("sha") or "")[:8],
                "date": date,
                "author": author,
                "subject": first[:140],
                "ai_signal": has_ai,
            }
        )

    n = len(commits)
    return {
        "repo": canonical,
        "path": prefix,
        "canonical_url": f"https://github.com/{canonical}/tree/{default_branch}/{prefix}",
        "collected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "caveats": [
            "Stars, forks, open_issues, languages, workflows, contributors, and releases in monorepo_meta are for the entire host repo, not this path.",
            "Commit stats below are filtered to path= and are comparable to other assessments' last-50 windows.",
        ],
        "monorepo_meta": {
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
        "plugin_meta": json.loads(plugin["excerpt"]) if plugin and plugin.get("excerpt") else None,
        "structure": {
            "root": top_tree,
            "skills": skills,
            "skill_count": len(skills),
            "file_count": len(blobs),
            "byte_count": sum(int(t.get("size") or 0) for t in blobs),
            "ext_counts": ext_count,
            "ext_bytes": ext_bytes,
        },
        "key_files": {
            k: v
            for k, v in {
                "plugin.json": plugin,
                "README.md": readme,
                "LICENSE": license_f,
            }.items()
            if v
        },
        "commit_stats_last_50_path": {
            "count": n,
            "date_span": {
                "newest": commits[0]["date"] if commits else None,
                "oldest": commits[-1]["date"] if commits else None,
            },
            "conventional_pct": round(100 * conv / n, 1) if n else 0,
            "fix_revert_pct": round(100 * fix / n, 1) if n else 0,
            "ai_coauthor_pct": round(100 * ai / n, 1) if n else 0,
            "top_recent_authors": sorted(authors.items(), key=lambda kv: -kv[1])[:8],
            "sample_commits": commits[:20],
        },
    }


def main() -> None:
    if len(sys.argv) < 4:
        print("Usage: collect_path.py <output_dir> <owner/repo> <path>", file=sys.stderr)
        sys.exit(1)
    out_dir = Path(sys.argv[1])
    repo, path = sys.argv[2], sys.argv[3]
    out_dir.mkdir(parents=True, exist_ok=True)
    data = collect_path(repo, path)
    slug = f"{data['repo'].replace('/', '__')}__{path.replace('/', '_')}"
    dest = out_dir / f"{slug}.json"
    dest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    cs = data["commit_stats_last_50_path"]
    print(f"Wrote {dest} path-commits={cs['count']} conv={cs['conventional_pct']}%")


if __name__ == "__main__":
    main()
