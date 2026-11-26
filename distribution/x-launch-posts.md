# X Launch Kit (X Premium — Research Note 2-Card + X Article Format)

## Why This Format Wins on X
- **Main Post = 2 side-by-side 4:5 light-mode Research Note cards** (stands out hard against X's dark timeline, drives zoom-in dwell time + bookmarks):
  - **Image 1 (`assets/x-card-1-prompt.png`):** Stack-aware Week 1 `<prompt>` anyone can drop into T3 Code / Claude Code / Codex / OpenCode right now.
  - **Image 2 (`assets/x-card-2-infographic.png`):** Full visual breakdown of the 35-repo audit (`3,040,947` stars, `stablyai/orca`, `mattpocock/sandcastle`, `gstack`, `superpowers`, `pi`, `codex`, `cmux`).
- **Reply #1:** Link to the X Article + live interactive explorer (`https://agentic-oss-site.vercel.app`) + public MIT data repo (`https://github.com/Ty-Robb/agentic-oss-assessments`).
- **Reply #2:** Plain-text copy of [`upgrade-prompt.txt`](upgrade-prompt.txt) so readers can copy-paste without OCR.

---

## Main Post (Attach `x-card-1-prompt.png` + `x-card-2-infographic.png`)

> The fastest-moving desktop agent repo in our 35-repo audit (3.04M combined stars) tells its agents to stop writing tests.
>
> `stablyai/orca` (137.8k★) landed 50 commits in 3.2 hours. Line 1 of its repo rules: "Tests are the exception." Prove the change by running it. Commit a test only where a silent regression is expensive.
>
> Meanwhile:
> - `openai/codex` has 28,619 open issues + PRs. `earendil-works/pi` has 307 (auto-closed by default).
> - `garrytan/gstack` benchmarked itself on 100 tasks: 58% solved with the skill stack vs. 61.6% without it.
> - `mattpocock/sandcastle` runs a bot (`lint-shrink.yml`) that tightens lint/typecheck baselines after every merge to `main`.
>
> The prompt on the left card is the Week 1 patch (cross-checked by Codex, Claude Opus, and Grok). Paste it into your coding agent to audit your repo and add the gates without bloating your test suite:

*(Attach `assets/x-card-1-prompt.png` first, `assets/x-card-2-infographic.png` second. Do NOT put an outbound URL in Post 1.)*

---

## Reply #1 (Post Right Below Main Post — X Article + Live Site + Public Repo)

> Full 35-repo teardown in my X Article (every config snippet, workflow count, and what stalled `1code`, `vibe-kanban`, `Roo-Code`, and `get-shit-done`):
>
> [Paste X Article link here]
>
> Interactive 35-repo explorer + all 35 primary-source audits:
> https://agentic-oss-site.vercel.app
>
> Raw GitHub API JSONs, playbook & 3-model red-team log (MIT):
> https://github.com/Ty-Robb/agentic-oss-assessments

---

## Reply #2 (Plain-Text Prompt)

> Plain-text Week 1 prompt to copy-paste straight into T3 Code, Claude Code, Codex, or OpenCode 👇

*(Paste [`upgrade-prompt.txt`](upgrade-prompt.txt))*

---

## X Article Publishing Checklist

1. **Title:** `Stop Lecturing Agents in AGENTS.md. Make the Linter Reject Them. (35-Repo Audit · 3.04M Stars)`
2. **Cover image:** `assets/x-article-cover-light.png` (or `assets/00-cover-hero.png` for dark mode)
3. **Body:** [`x-article.md`](x-article.md)
4. **Inline charts:**
   - Section 3: `assets/01-open-issue-stress-test.png`
   - Section 5: `assets/02-ci-goldilocks-zone.png`
   - Section 8: `assets/03-six-changes-this-week.png`
