# X Launch Kit (X Premium — Research Note 2-Card + X Article Format)

## Why This Format Wins on X
- **Main Post = 2 side-by-side 4:5 light-mode Research Note cards** (stands out hard against X's dark timeline, drives massive zoom-in dwell time + bookmarks):
  - **Image 1 (`assets/x-card-1-prompt.png`):** Copy-pasteable `<prompt>` anyone can drop into T3 Code / Claude Code / Codex / OpenCode right now.
  - **Image 2 (`assets/x-card-2-infographic.png`):** Full visual breakdown of the 34-repo audit (hygiene, lint gates + `sandcastle` ratchet bot, `gstack`/`Pocock`/`superpowers`/`pstack` skill-stack receipts, Open-Issue Stress Test, CI Goldilocks Zone, 5-KPI footer).
- **Reply #1:** Link to your X Article + plain-text copy of [`upgrade-prompt.txt`](upgrade-prompt.txt) (so readers can copy-paste without OCR).
- **X Article:** Publish [`x-article.md`](x-article.md) with `assets/x-article-cover-light.png` as the cover image and the 3 detailed charts inline.

---

## Main Post (Attach `x-card-1-prompt.png` + `x-card-2-infographic.png`)

> I audited 34 open-source AI coding repos (2.90M combined stars) via the GitHub API — harnesses, orchestrators, and top skill stacks (`t3code`, `openclaw`, `opencode`, `pi`, `mattpocock/skills`, `sandcastle`, `gstack`, `pstack`, `superpowers`, `spec-kit`).
>
> 4 already archived or sunset. `gstack`'s own benchmark showed 58/100 bugs fixed vs. 61/99 without it — because mechanical gates beat prompt stacks 10-to-1.
>
> Send this prompt and infographic to your coding agent to audit and upgrade your own repo:

*(Attach `assets/x-card-1-prompt.png` first, `assets/x-card-2-infographic.png` second. Do NOT put an outbound GitHub URL in Post 1.)*

---

## Reply #1 (Post Right Below Main Post — X Article + Plain-Text Prompt)

> Full breakdown in my X Article (all 34 repo receipts, exact config snippets, what killed `1code`, `vibe-kanban`, `Roo-Code`, and `get-shit-done`, plus why Matt Pocock's `sandcastle` has the cleanest small-repo setup in the study):
>
> [Paste X Article link here]
>
> And here's the plain-text prompt if you want to copy-paste it directly into your agent 👇

*(Then paste the contents of [`upgrade-prompt.txt`](upgrade-prompt.txt) in Reply #2, or link `https://github.com/Ty-Robb/agentic-oss-assessments` once you flip the repo public.)*

---

## X Article Publishing Checklist

1. **Title:** `I Audited 34 Open-Source AI Coding Repos (2.90M Stars). Here's What Actually Works.`
2. **Cover image:** `assets/x-article-cover-light.png` (or `assets/00-cover-hero.png` if you prefer dark mode)
3. **Body:** [`x-article.md`](x-article.md)
4. **Inline charts:**
   - Section 3: `assets/01-open-issue-stress-test.png`
   - Section 5: `assets/02-ci-goldilocks-zone.png`
   - Section 8: `assets/03-six-changes-this-week.png`
