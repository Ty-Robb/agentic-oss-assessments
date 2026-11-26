# Stop Lecturing Agents in `AGENTS.md`. Make the Linter Reject Them.

*Primary-source engineering teardown of **35 public AI coding, harness, orchestration, and skill-stack repositories** (**3,040,947 / ~3.04M combined stars**, snapshot **2026-11-25**), cross-checked by Codex (`gpt-6.2-astra`), Claude (`claude-opus-5-5`), and Grok (`grok-4.7`).*

*Cohort: `t3code`, `stablyai/orca`, `openclaw`, `opencode`, `pi`, `codex`, `gemini-cli`, `OpenHands`, `cline`, `goose`, `paperclip`, `paseo`, `happy`, `cmux`, `Paradev`, `emdash`, `oh-my-openagent`, `beads`, `symphony`, `bolt.diy`, `claude-squad`, `costrict`, `1code`, `vibe-kanban`, `Roo-Code`, `mattpocock/skills`, `mattpocock/sandcastle`, `obra/superpowers`, `github/spec-kit`, `garrytan/gstack`, `Fission-AI/OpenSpec`, `gsd-build/get-shit-done`, `bmad-code-org/BMAD-METHOD`, `backnotprop/pstack`, and `michael-denyer/pstack-claude`.*

---

Most advice on running AI coding agents comes from toy demos or vendor blogs.

I pulled primary-source GitHub API snapshots across **35 public agentic coding, orchestration, and skill-stack repositories** (**3.04M combined stars** — 33 OSI open-source, plus source-available `oh-my-openagent` and BSL-hybrid `cmux`). I inspected their actual `AGENTS.md` and `CLAUDE.md` files, custom lint plugins, YAML CI workflows, `pnpm-workspace.yaml` locks, PR templates, and commit histories.

Four of the 35 have archived or begun sunsetting. Meanwhile, repos like `openclaw` (50 commits in 2.3 hrs), `stablyai/orca` (50 commits in 3.2 hrs), and `t3code` (50 commits in 7.0 hrs) are moving at extreme commit volume — and dealing with the real maintenance trade-offs that come with it (`orca`'s last 50 commits are 70% fix/revert with 9,918 open items).

Here are the patterns that held up under primary-source inspection — along with the counter-examples and caveats.

---

## 1. Four Repos Archived or Sunset — For Four Distinct Reasons

Launch stars did not insulate a single one of them:

- **`21st-dev/1code` (5.6k★ — archived; 7 weeks creation-to-last-push):** Operated as a one-way public mirror (`sync-to-public.sh`) with zero public CI workflows, zero linter, zero tests, dual lockfiles (`bun.lock` + `bun.lockb`), and a `CLAUDE.md` still listing shipped features as "Planned WIP."
- **`BloopAI/vibe-kanban` (28.8k★ — sunsetting per README):** Genuine systems craft (`ts-rs` codegen checks, `sqlx` offline verification, `clippy -D warnings`), carrying 30 Rust crates, ElectricSQL, a WebRTC relay, Tauri, and Rust nightly on a small core team.
- **`RooCodeInc/Roo-Code` (24.2k★ — archived May 2026):** Stayed coupled to a VS Code extension while surviving peers (`Cline`, `OpenHands`, `Goose`) decoupled into standalone SDKs and multi-surface ACP control planes.
- **`gsd-build/get-shit-done` (64.1k★ — archived May 2026):** A security and governance event, not feature sprawl — commit `126b6b9e` warned the repository *"appears compromised"* and README redirected users to `open-gsd/gsd-core`. Prompt and skill repos carry the exact same supply-chain blast radius as code packages.

---

## 2. Keep `AGENTS.md` Short and Incident-Cited — Move Repeated Bugs Into the Linter

Large instruction files don't automatically stall a team (`oh-my-openagent` has a 70.8 KB `AGENTS.md` with a 3-month-stale header and still landed 50 commits in 19.2 hrs; `gstack` splits 54 KB across `AGENTS.md` and `CLAUDE.md`), and Rust-first `codex` ships with no root `AGENTS.md` at all.

Still, the cleanest TypeScript codebases treat `AGENTS.md` as a **check command, trap list, and router**:

- **`openclaw/openclaw` (395.2k★):** Hard-caps `AGENTS.md` under **20,000 characters** with one strict governance rule: ***"A new rule cites an incident."*** Adds *"Choose good compromises"* (prefer an idempotency key, one check, and retry over speculative machinery).
- **`bmad-code-org/BMAD-METHOD` (55.7k★):** Keeps a crisp 35-line `AGENTS.md`: ***"Length and ambiguity are paid on every run... Prefer deleting an instruction to hedging it."***
- **`getpaseo/paseo` (25.3k★):** Enforces a **`Doc voice`** rule banning LLM prose clichés (`"It's not X, it's Y"`, `"robust"`, `"seamless"`, `"and that matters"`) and requiring agents to integrate doc edits rather than appending paragraphs.
- **`manaflow-ai/cmux` (29.0k★) & `paperclipai/paperclip` (116.9k★):** `cmux` keeps a compact **`REVIEW.md`** of real recurring PR catches; `paperclip` stores domain rules in `grep`-indexed `rules/*.mdc`; `orca` puts deep reference docs under `docs/agents-md-refs/`.
- **Single source of truth:** Put a **1-line `@AGENTS.md` include** in `CLAUDE.md` (`t3code`, `Paradev`, `emdash`, `beads`). It avoids symlink breakage on Windows and stops copy-pasted duplicates from drifting.

Once an agent makes the same mistake twice, the strongest teams **turn it into a hard lint error with baselines:**

- **`mattpocock/sandcastle` (9.3k★, 2.6 MB TS):** Enables 5 `oxlint` categories (`correctness`, `suspicious`, `pedantic`, `perf`, `style` = `"error"`, leaving `restriction`/`nursery` off) with type-aware `oxlint-tsgolint`, bans `Effect.run*` outside entry points, tests `GLOSSARY.md` ↔ `docs/guide/` ↔ `README.md` in Vitest (`tests/docs-guide.test.ts`), and runs an **automated shrink-only ratchet PR bot (`lint-shrink.yml`)** on every push to `main` that lowers lint/typecheck baselines automatically.
- **`stablyai/orca` (137.8k★, 143.7 MB TS):** Ships 5 surgical `oxlint` plugins (`quadratic-buffer-concat.mjs`, `ime-enter-guard.mjs`, `app-store-performance.mjs`, `anti-slop-prefilter.mjs`, `renderer-scrollbar-style.mjs`), bans eager value-imports of `@linear/sdk` (~2.6 MB CJS), and runs `main-blocking-work.yml` to ratchet Electron main-process sync spawns.
- **`anomalyco/opencode` (229.1k★):** Custom `anti-slop` `oxlint` plugins + unit-tested `ast-grep` rules (`no-widen-then-assert`, `no-module-mocking`).
- **`Paradev` / `emdash` / `paseo`:** Domain `noRestrictedImports` (banning sync subprocesses and cross-tenant queries), `respectEslintDisableDirectives: false` (no silent `eslint-disable` escapes), sole-writer DB table bans, and per-file, per-API allowlists (`paseo/no-sync-io`).

---

## 3. The Open-Issue Stress Test (And Its Caveats)

When anyone can prompt an agent to open a PR in 90 seconds, open-by-default trackers accumulate massive backlogs. Note two important caveats on the numbers below: GitHub's `open_issues_count` combines **open issues and open PRs**, and company backing/user base varies hugely across these projects:

*[Embed Image: `01-open-issue-stress-test.png`]*

- **`openai/codex`** (136.4k★, open tracker + large paid user base): **28,619** open issues + PRs
- **`manaflow-ai/cmux`** (29.0k★, autonomous agent factory): **11,218**
- **`stablyai/orca`** (137.8k★, `Fixes #` gate for outsiders): **9,918**
- **`openclaw/openclaw`** (395.2k★, 20-PR author cap + bot sweepers): **9,182**
- **`pingdotgg/t3code`** (78.8k★, `VOUCHED.td` + PR limits): **3,681**
- **`aaif-goose/goose`** (57.0k★, `Ready`-board gate): **512**
- **`obra/superpowers`** (326.5k★, maintainer-reported *"94% PR rejection rate"* near the top of `AGENTS.md`, line 7): **372**
- **`earendil-works/pi`** (123.8k★, default-closed `lgtmi`/`lgtm` auto-close): **307**

`codex` had **93.2×** as many open items as `pi` at collection — though `pi`'s 307 is partly true by construction because unapproved items are auto-closed on arrival (which trades away public bug discoverability). Counter-example inside our own cohort: `paseo` (`25.3k★`, `2,203` open) runs *"PRs closed by default"* yet carries more open items per star than open-tracker `opencode`.

Still, `paseo`'s `CONTRIBUTING.md` nails the modern maintainer constraint:

> *"I can prompt an agent to write code just as you can. The bottlenecks are choosing what to build, shaping it, verifying its behavior, and taking responsibility for its maintenance."*

---

## 4. The Fastest Desktop Agent Repo Tells Agents to Stop Writing Tests

Left alone, coding agents fail verification in two opposite ways: they pad PRs with brittle mock/UI unit tests, or they weaken assertions and treat skipped CI jobs as green coverage.

Combining four repos resolves both:

1. **Test selectively (`stablyai/orca`):** Opens `AGENTS.md` with **`"Tests are the exception."`** Prove behavior by running the real app/CLI; commit an automated test *only* where a silent regression is expensive (parsers/codecs, security boundaries, persistence/migrations, concurrency/state machines, cross-platform paths), and delete low-value UI/mock tests you touch. Backed by a zero-checkout **`pr-test-loc.yml`** workflow on free `ubuntu-slim` runners (fetching trusted scripts from `default_branch`) posting a test-vs-prod LoC table on every PR, a mandatory **`## Performance`** PR check (`"None, because ..."` allowed), and shadow-mode diff test selection (`unit-selection-evidence.yml`) against its 24-shard suite.
2. **Keep grading independent (`OpenHands`):** `verify-skill-isolation.yml` fails CI if a PR modifies both production code and `.agents/skills/verify-*/` in the same PR; `stryker-diff.mjs` runs diff-scoped mutation testing on critical paths.
3. **Treat self-run QA as disclosure, not proof (`cmux`, `oh-my-openagent`, `beads`):** Require **`### Observed / Not run`** in PR bodies, keep local QA captures gitignored (`.omo/evidence/` + `sha256sum` + CI audit failing if tracked), verify filtered tests ran >0 subtests, and answer `NOT_ENOUGH_INFO` when evidence runs out.
4. **Ban fragile source-grep tests (`gstack`, `gsd`):** `gstack`'s `test-value-bar` and `gsd`'s `lint-no-source-grep.cjs` reject tests that merely regex source strings instead of executing behavior.

---

## 5. Match CI Workflow Count to Team Size

Across the 35 repos (counting exact `.yml`/`.yaml` files in `.github/workflows/`), most lean high-velocity teams cluster around **8–30 workflows**:

*[Embed Image: `02-ci-goldilocks-zone.png`]*

- **Under-gated (`0–1` YAML workflows):** `1code` (`0`, one-way mirror) went quiet after 7 weeks. `slopus/happy` (`1`) bans extra Actions to control cost and works only because a tight 2-person core ships directly to `main`. `superpowers` (`0`) relies on an external CLI eval lab.
- **Lean high-signal range (`8–30` YAML workflows):** `sandcastle` (8), `paseo` (12), `pi` (16), `spec-kit` (19), `opencode` (21), `Paradev` (22), `OpenHands` (25), `codex` (28), `t3code` (29); `emdash` runs 6.
- **Heavy CI stacks (`38–231` YAML workflows):** Larger backed teams sustain more (`gstack` 38, `gemini-cli` 47, `orca` 67 with 6 cache-warmup/runner workflows, `openclaw` 133). At the extreme, `cmux` carries **231** YAML workflows — and **17 of its 20 stored Nov 25 commits** (~85%, by a single author on one day) touched CI, runners, or release automation.

The winning CI formula for a small/mid team:
- **Path-filtered jobs** paired with **one `if: always()` `CI required` aggregator** (`codex`, `t3code`) that fails on `failure`/`cancelled` and treats `skipped` as pass *only* when path filters caused it.
- **One cached diff-scoped local check** (`pnpm check:changed` / `pnpm verify`) paired with `orca`'s rule: *"A pass is cached, so don't rerun it 'to be sure', and don't also run `pnpm tc`, `pnpm lint`, or the full suite."*

---

## 6. What 10 Agent Skill & Workflow Stacks Taught Us

Auditing the 10 largest skill, spec, and sandbox repos (**1.17M stars**) turned up the most candid self-evaluation in the study.

**`garrytan/gstack` (142.6k★, 45.1 MB TS, 38 YAML workflows)** ran a 100-task GitHub bug/feature benchmark in its own `README.md` on Opus 5.5:
- **58% (58/100) solved with `gstack`** vs. **61.6% (61/99, one unscored) without it** (and **29/60 in each arm** on security fixes).
- Its own conclusion: ***"Use gstack for the workflow, the reviews, the shipping steps and the safety guards, not for a higher fix rate."***

That is one model and one vendor's benchmark — not proof for every skill stack — but the durable takeaways from Chunk 6 are mechanical:

- **`mattpocock/skills` (332.8k★):** Explicitly critiques heavy process-owning stacks (GSD, BMAD, Spec-Kit), organizes composable skills in a 5-bucket lifecycle, validates every `SKILL.md` with the installer's exact YAML parser, enforces **fresh context windows for subagent-dispatching skills** (Codex forks parent context by default), and sets **both** `disable-model-invocation: true` (Claude) and `agents/openai.yaml` `allow_implicit_invocation: false` (Codex).
- **`gstack` (142.6k★):** `.tmpl` → `SKILL.md` codegen, **`catalog-budget.test.ts` (`2,292`-token cap)**, **`test/egress-receipt-wiring.test.ts`** (mandatory local receipt before outbound fetch), and `$150/wk`-capped pre-registered eval sweeps.
- **`pstack` (Lauren Tan / `poteto` at Cursor; ports `backnotprop/pstack` & `michael-denyer/pstack-claude`):** `/create-formal-verification-skill` generating project-local TLA+ and Lean verification skills, plus `tools/forks.json` declared-fork tracking and prompt-injection hardening in `watch-pr`.
- **`github/spec-kit` (151.4k★, 19 YAML workflows):** Pioneers firewall-sandboxed **GitHub Agentic Workflows (`gh-aw`)** compiled `.md` → `.lock.yml`.
- **`Fission-AI/OpenSpec` (75.7k★, 4 YAML workflows):** Enforces CLI cold-start module budgets (`startup-modules.test.ts`) and npm OIDC trusted publishing.

---

## 7. Small Config Wins That Pay Off Immediately

1. **Supply-chain cooldown + dated sweeper (`codex`, `openclaw`, `orca`, `OpenSpec`, `paseo`):**
   ```yaml
   # pnpm-workspace.yaml
   minimumReleaseAge: 4320       # 3d (orca) or 10080 for 7d (codex/openclaw)
   minimumReleaseAgeStrict: true
   blockExoticSubdeps: true
   allowBuilds:
     esbuild: true               # comment every single true/false entry
   ```
   Pair with dated expiry comments + a sweeper workflow (`openclaw`), `lockfile-lint` (`paseo`), GHSA overrides in `pnpm-workspace.yaml` (`OpenSpec`), and `ignoredOptionalDependencies` if your dependencies bundle unused ~95 MB/platform CLIs (`orca`).
2. **Shrink-only lint/typecheck ratchet bot (`mattpocock/sandcastle`):** `lint-shrink.yml` tightens committed lint/typecheck baselines on `main` automatically — keep it off coverage floors so it never fights deleting low-value tests.
3. **Trigger-gated infra proofs:** `lock_timeout = '5s'` migrations (`Paradev`), real Postgres CI `pg_dump`/restore (`paperclip`), prod Docker `curl` smoke test (`bolt.diy`), real `bwrap` sandbox CI (`sandcastle`), `prefix-stability.test.ts` (`openclaw`), and `eval-gate` environment-approved behavioral evals (`gemini-cli`: 38 `*.eval.ts` files).
4. **Multi-agent machine safety (`pi`, `paseo`, `orca`, `oh-my-openagent`, `happy`):** Ban `git add -A`/`stash`/`reset --hard`, isolate checkout `.dev/` homes, run hidden-window Electron CDP (`ORCA_BACKGROUND_LAUNCH=1`), guard `$HOME` in meta-tests, and release only from clean `main == origin/main` (`happy` learned this after a stale-worktree preview OTA rolled back 4 fixes on preview phones).

---

## 8. The Week 1 Patch (Harmonized So Gates Never Fight Each Other)

*[Embed Image: `03-six-changes-this-week.png`]*

1. **Open `AGENTS.md` with one cached diff-scoped check command**, add a 1-line `@AGENTS.md` include in `CLAUDE.md`, and include `Doc voice`, *"Choose good compromises"*, multi-agent Git safety, and `orca`'s **`"Tests are the exception"`** rule.
2. **Tell agents not to re-run the full suite** once the cached diff-scoped check passes.
3. **Add `### Observed / Not run` + `## Performance` (`"None, because ..."` allowed)** to your PR template, plus a CI guard rejecting tracked QA/scratch files.
4. **Seed `REVIEW.md` from real PR history** (skip if you don't have history yet).
5. **In Week 2, commit baselines first**, turn 3–5 real review catches into hard lint errors with per-file allowlists, add a lint/typecheck-only shrink bot, and wire one explicit `if: always()` `CI required` aggregator + zero-checkout `pr-test-loc`.
6. **Keep Week 3 strictly trigger-gated:** add dependency cooldowns, DB dump/restore, `prefix-stability`, `verify-skill-isolation` (`.agents/skills/verify-*/`), or dual Claude+Codex skill checks only when your repo actually triggers them.

---

*Not covered in this 35-repo wave (candidates for Chunk 7): Aider, Zed (originator of ACP), Kilo Code, Continue, SWE-bench/SWE-agent, and non-agent AI-governance pioneers (Ghostty, curl). All 35 raw JSON snapshots, assessments, and the 3-model review log live in `Ty-Robb/agentic-oss-assessments` (MIT) and at `https://agentic-oss-site.vercel.app`.*
