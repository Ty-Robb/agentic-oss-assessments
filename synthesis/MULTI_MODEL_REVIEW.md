# Multi-Model Collective Review & Corrections Log

*Audit date: **2026-11-26** · Study scope: **35 public repositories** (`3,040,947` combined GitHub stars as of `2026-11-25`).*

To avoid single-model blind spots, after assembling the 35-repo dataset and initial synthesis (authored with Gemini 4 Neon), we ran three independent, read-only review delegates across three distinct frontier providers:

| Reviewer | Provider / Model | Mandate |
| --- | --- | --- |
| **Fact & Primary-Source Auditor** | Codex (`gpt-6.2-astra`, `reasoningEffort: high`) | Programmatically verify every star count, workflow count, commit span, quote, and path against all 35 raw JSON snapshots under `data/`. |
| **Adversarial & Blind-Spot Red-Teamer** | Claude (`claude-opus-5-5`, `effort: high`) | Stress-test the 6 Laws for survivorship bias, confounders, internal contradictions, and missing high-signal OSS comparisons. |
| **Prompt & Distribution Critic** | Grok (`grok-4.7`, `reasoningEffort: high`) | Audit `upgrade-prompt.txt`, Week 1–3 adoption ergonomics, and the X launch kit for agent failure modes, rule conflicts, and writing clichés. |

---

## Concrete Corrections Applied From the Review Panel

### 1. Factual & Quantitative Fixes (Codex `gpt-6.2-astra`)
- **Fixed 5 inflated workflow counts:** `collect_chunk.py` previously counted all files in `.github/workflows/`, including non-YAML `.ts`/`.md`/`.disabled` helpers (`952` of `973` entries across 35 repos are YAML). Updated collector + matrix + article:
  - `openai/codex`: `31` → **`28`**
  - `code-yeongyu/oh-my-openagent`: `48` → **`43`**
  - `zgsm-ai/costrict`: `11` → **`9`**
  - `github/spec-kit`: `29` → **`19`** (excluding 10 `gh-aw` `.md` sources)
  - `Fission-AI/OpenSpec`: `5` → **`4`**
- **Fixed 4 commit spans & 1 star subtotal:** `goose` (`4.8 days`), `symphony` (`195 days` across 47 commits), `sandcastle` (`5.9 days`), `backnotprop/pstack` (`27.9 days`) vs. `pstack-claude` (`6.5 days`); Chunk 1's 5 rivals sum to **`195,170` (`195.2k`, not `195.1k`)**.
- **Fixed 4 technical details & quotes:**
  - `google-gemini/gemini-cli`: `evals/` contains **47 entries (`38` `*.eval.ts` files)**, and `eval-pr.yml` uses a GitHub **`eval-gate` environment** approval (not a PR label).
  - `OpenHands/OpenHands`: protected verification skill path is **`.agents/skills/verify-*/`** (not `*-qa/`).
  - `slopus/happy`: stale-worktree OTA rollback affected **preview phones**, not every production user's phone.
  - `bmad-code-org/BMAD-METHOD`: added ellipsis (`...`) between the two separate quoted bullets.
- **Scoped "open source" accurately:** Changed cohort label to **"35 public repositories"** because `oh-my-openagent` is source-available (SUL-1.0) and `cmux` has BSL-licensed server directories.
- **Eliminated all stale `24` / `34` / `2.90M` references** across `README.md`, `PLAYBOOK.md`, `EXECUTIVE_BRIEF.md`, `x-article.md`, and `x-launch-posts.md`.

### 2. Epistemic & Methodological Tightening (Claude `claude-opus-5-5`)
- **Renamed "6 Empirical Laws" → "6 Observed Patterns (With Counter-Examples & Caveats)"** and cut the unsourced `"10-to-1"` claim everywhere.
- **Fixed `oh-my-openagent` dual-role contradiction** in Pattern 1 (removed it from the "stopped lecturing" list).
- **Clarified the Open-Issue Stress Test:** Explicitly noted that GitHub's `open_issues_count` combines open issues + open PRs; noted `pi`'s 307 is a closing policy (auto-closing unapproved intake on arrival) rather than proven review-load reduction; footnoted `bolt.diy` (`stale.yml`), `symphony` (reference spec with no community intake), `codex` (large paid user base), and counter-example `paseo` (`11` stars/open issue despite "PRs closed by default").
- **Scoped `cmux`'s CI churn accurately:** Clarified that ~17 of 20 stored Nov 25 commit subjects (`~85%`) were CI/runner/release maintenance by a single author (`teamleaderleo`) on one day — a vivid operational snapshot rather than a multi-month org average — and listed high-workflow survivors (`openclaw` 133, `orca` 67, `gemini-cli` 47, `gstack` 38) alongside `8–30` guidance.
- **Reclassified `gsd-build/get-shit-done` as a security/governance event** (`126b6b9e` *"appears compromised"* warning + README redirect to `open-gsd/gsd-core`) rather than scope sprawl, and noted `1code`'s 7-week span is creation-to-last-push on a one-way mirror.
- **Resolved the `orca` vs. `OpenHands` verification tension** into one coherent rule: commit tests only for costly silent regressions (`orca`), keep their verification harness independent (`OpenHands`), and treat self-run CDP screenshots as transparent disclosure (`Observed / Not run`), not independent proof.
- **Dropped `ai_coauthor_pct` as a quality/evaluative signal** because commit-trailer regexes undercount teams that strip co-author trailers (`orca`, `codex`, `Paradev` = `0%`).
- **Scoped `gstack`'s self-benchmark:** Stated as **58% (58/100) vs. 61.6% (61/99)** on Opus 5.5, self-reported by `gstack` — does not generalize across all models/stacks.
- **Added a Methodology, Confounders & Not-Covered section** to `PLAYBOOK.md` disclosing `pingdotgg/t3code` as the reference baseline and explicitly noting high-signal repos outside this 35-repo wave (**Aider**, **Zed / ACP**, **Kilo Code**, **Continue**, and **Ghostty / curl** AI-contribution policies).

### 3. Prompt & Distribution Ergonomics (Grok `grok-4.7`)
- **Rebuilt `distribution/upgrade-prompt.txt` into a surgical Week 1 patch prompt:**
  - Deleted the marketing essay, unsourced `"10-to-1"`, and 35-repo roster from the agent payload.
  - Added strict guardrails so agents **inspect first, stop before editing, skip controls that don't fit the repo's stack, and never fabricate review incidents** without git/PR history.
  - Defaulted `CLAUDE.md` to a **1-line `@AGENTS.md` include** (safe on Windows, never overwrites an existing file silently).
  - Integrated Orca's 3 portable rules (**`"Tests are the exception"`** for costly silent regressions, **PR test-vs-prod LoC check**, and **`## Performance`** with `"None, because ..."` allowed) plus the **cached `check:changed`** rule ("do not also re-run the full suite").
  - Specified exact `if: always()` CI aggregator semantics (fail on `failure`/`cancelled`; treat `skipped` as pass only when caused by path filters).
  - Cut `knip`, TLA+/Lean, Docker smoke, dump/restore, and rising coverage floors from the default Week 1 prompt (so coverage floors never fight deleting low-value tests).
  - Made skill-hygiene checks conditional on existing `SKILL.md` files and required **both** `disable-model-invocation: true` (Claude) and `agents/openai.yaml` `allow_implicit_invocation: false` (Codex).
- **Harmonized Week 1–3 in `PLAYBOOK.md`:** Week 1 = lean instructions + test-exception policy + cached diff-scoped check + `Observed / Not run`; Week 2 = debt baselines → 3 real review-catch lint rules → lint/typecheck-only shrink bot; Week 3 = strictly trigger-gated (public fork PRs, SQL migrations, prompt caching, or existing skill catalogs).
- **Sharpened X Launch Kit (`x-launch-posts.md` & `x-article.md`):** Replaced generic template phrasing with Orca's `"Tests are the exception"` lead hook, aligned every count to `35` repos / `3,040,947` stars, and tightened the article title to *"Stop Lecturing Agents in `AGENTS.md`. Make the Linter Reject Them."*
