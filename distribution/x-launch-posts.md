# X Launch Kit (X Premium)

## Publishing Checklist

1. **Publish the X Article first** using [`x-article.md`](x-article.md).
   - **Title:** `I Audited 24 Open-Source AI Coding Repos (1.73M Stars). Here's What Actually Works.`
   - **Cover image:** `assets/00-cover-hero.png` (16:9 dark editorial summary card)
   - **Inline images (3):**
     - Section 3: `assets/01-open-issue-stress-test.png`
     - Section 5: `assets/02-ci-goldilocks-zone.png`
     - Section 7: `assets/03-six-changes-this-week.png`
2. **Post the Hook Post below** quoting/attaching the X Article (do **not** put a GitHub URL in Post 1).
3. **Post Reply #1 immediately** underneath the hook post. *(Note: `Ty-Robb/agentic-oss-assessments` is currently **private** — flip it to public before posting the repo link, or omit the link if keeping it private.)*

---

## Hook Post (Attach or Quote the X Article)

> I audited 24 open-source AI coding repos (1.73M combined stars) via the GitHub API — not their marketing pages.
>
> Real `AGENTS.md` files, linter plugins, CI workflows, dependency locks, and recent commit histories.
>
> A few receipts that surprised me:
>
> • `pi` has 307 open issues at 124k★. `codex` has 28,619 at 136k★ (93× gap).
> • `1code` shipped with 0 CI workflows and archived in 7 weeks.
> • `cmux` built 231 workflows — now ~80% of its recent `main` commits are just fixing CI.
> • `OpenHands` blocks PRs from editing both app code and verification skills, and runs diff-scoped mutation testing.
> • `emdash` sets `respectEslintDisableDirectives: false` so agents can't silence lint errors.
>
> Full breakdown + the 6 things worth stealing for your own repo this week:

*(Attach `assets/00-cover-hero.png` or the native X Article card.)*

---

## Reply #1 (Post Right Below Hook Post)

### If you flip the repo public:
> Full dataset, raw GitHub API snapshots, per-repo teardowns across all 24 projects, and the Week 1–3 TypeScript rollout playbook are open here:
>
> https://github.com/Ty-Robb/agentic-oss-assessments

### If you keep the repo private:
> The 6 fastest wins to ship on your own repo this week (no new infra required):
>
> 1. Cap `AGENTS.md` at <180 lines ("a new rule cites an incident") + symlink `CLAUDE.md`
> 2. Add a 1-page `REVIEW.md` of recurring PR review catches
> 3. Add `minimumReleaseAge: 10080` (7-day npm cooldown) to `pnpm-workspace.yaml`
> 4. Turn your top 3–5 recurring review comments into hard lint errors (ban silent `eslint-disable`)
> 5. Add one diff-scoped local check (`check:changed`) + `knip` + single `CI required` job
> 6. Require `### Observed / Not run` in PR bodies + fail CI on committed scratch/evidence files
