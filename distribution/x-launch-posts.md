# X Launch Kit (X Premium — Research Note 2-Card + X Article Format)

## Why This Format Wins on X
- **Main Post = 2 side-by-side 4:5 light-mode Research Note cards** (stands out hard against X's dark timeline, drives massive zoom-in dwell time + bookmarks):
  - **Image 1 (`assets/x-card-1-prompt.png`):** Copy-pasteable `<prompt>` anyone can drop into T3 Code / Claude Code / Codex / OpenCode right now.
  - **Image 2 (`assets/x-card-2-infographic.png`):** Full visual breakdown of the 24-repo audit (hygiene, lint gates, Open-Issue Stress Test, CI Goldilocks Zone, 5-KPI footer).
- **Reply #1:** Plain-text copy of [`upgrade-prompt.txt`](upgrade-prompt.txt) (so readers can copy-paste without OCR) + link to your X Article.
- **X Article:** Publish [`x-article.md`](x-article.md) with `assets/x-article-cover-light.png` as the cover image and the 3 detailed dark/light charts inline.

---

## Main Post (Attach `x-card-1-prompt.png` + `x-card-2-infographic.png`)

> I audited 24 open-source AI coding repos (1.73M combined stars) via the GitHub API — real `AGENTS.md` files, linter plugins, CI workflows, dependency locks, and recent commits.
>
> 3 already archived or sunset. The ones shipping 50 commits/day all converged on the same 6 mechanical guardrails.
>
> Send this prompt and infographic to your coding agent to audit and upgrade your own repo:

*(Attach `assets/x-card-1-prompt.png` first, `assets/x-card-2-infographic.png` second. Do NOT put an outbound GitHub URL in Post 1.)*

---

## Reply #1 (Post Right Below Main Post — Plain-Text Prompt + X Article)

> Full breakdown in my X Article (with all 24 repo receipts, exact config snippets, and what killed `1code`, `vibe-kanban`, and `Roo-Code`):
>
> [Paste X Article link here]
>
> And here's the plain-text prompt if you want to copy-paste it directly into your agent 👇

*(Then paste the contents of [`upgrade-prompt.txt`](upgrade-prompt.txt) in Reply #2, or link `https://github.com/Ty-Robb/agentic-oss-assessments` once you flip the repo public.)*

---

## X Article Publishing Checklist

1. **Title:** `I Audited 24 Open-Source AI Coding Repos (1.73M Stars). Here's What Actually Works.`
2. **Cover image:** `assets/x-article-cover-light.png` (or `assets/00-cover-hero.png` if you prefer dark mode)
3. **Body:** [`x-article.md`](x-article.md)
4. **Inline charts:**
   - Section 3: `assets/01-open-issue-stress-test.png`
   - Section 5: `assets/02-ci-goldilocks-zone.png`
   - Section 7: `assets/03-six-changes-this-week.png`
