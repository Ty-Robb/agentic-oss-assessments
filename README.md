# Agentic OSS Assessments

> **Live Website:** **[https://agentic-oss-site.vercel.app](https://agentic-oss-site.vercel.app)** — Interactive 36-repo explorer, charts, one-click Week 1 Upgrade Prompt, Playbook, Executive Brief, and individual audit pages.

Structured, primary-source engineering and agent-workflow assessments of **T3 Code rivals**, **flagship AI coding harnesses**, **orchestration platforms**, and **agent skill/workflow stacks** (**36 public repositories** — 34 standalone assessments across 6 chunks + `pingdotgg/t3code` as reference baseline + path-scoped `cursor/plugins/pstack` as #36; **3,040,947 / ~3.04M combined GitHub stars** as of **2026-11-25** from the 35 standalone repos; #36 is excluded from the star sum because host monorepo stars are not pstack-only; MIT-licensed research data).

Every assessment inspects the real repository via GitHub API (file trees, `AGENTS.md`/`CLAUDE.md`, YAML CI workflows, lint/type/eval gates, commit history, contributor distribution, and architectural boundaries) — and the synthesis has been independently fact-checked and red-teamed by a **3-model cross-provider review panel** ([`synthesis/MULTI_MODEL_REVIEW.md`](synthesis/MULTI_MODEL_REVIEW.md)).

## Start Here

- **[`synthesis/EXECUTIVE_BRIEF.md`](synthesis/EXECUTIVE_BRIEF.md)** — 5-minute distilled briefing covering all 36 public repositories.
- **[`synthesis/PLAYBOOK.md`](synthesis/PLAYBOOK.md)** — Master 36-repo comparison matrix, 6 observed patterns (with counter-examples & confounders), tiered **Steal Immediately / Steal as You Scale / Anti-Patterns** playbook, and a harmonized Week 1–3 rollout blueprint.
- **[`synthesis/MULTI_MODEL_REVIEW.md`](synthesis/MULTI_MODEL_REVIEW.md)** — Adversarial review log from **Codex (`gpt-6.2-astra`)**, **Claude (`claude-opus-5-5`)**, and **Grok (`grok-4.7`)** and every correction made before publication.
- **[`distribution/x-article.md`](distribution/x-article.md)** & **[`distribution/x-launch-posts.md`](distribution/x-launch-posts.md)** — Ready-to-publish long-form teardown, 2-card light-mode Research Note launch kit, stack-aware Week 1 prompt ([`upgrade-prompt.txt`](distribution/upgrade-prompt.txt)), and retina PNG visuals under `distribution/assets/`.
- **[`RUBRIC.md`](RUBRIC.md)** — Standardized 5-axis evaluation rubric and `pingdotgg/t3code` reference baseline.

## Assessment Coverage

| Chunk | Theme | Repositories | Combined Stars | Status | Summary |
| --- | --- | --- | ---: | --- | --- |
| Baseline | Reference Control Plane | `pingdotgg/t3code` | 78.8k | Reference | [RUBRIC.md](RUBRIC.md) |
| **Chunk 1** | Direct T3 Code Rivals (Worktree GUIs) | `stablyai/orca`, `ParadevAI/Paradev`, `BloopAI/vibe-kanban`, `generalaction/emdash`, `21st-dev/1code` | 195.2k | Done | [Chunk 1 Summary](chunks/chunk-01-direct-rivals/SUMMARY.md) |
| **Chunk 2** | Flagship Open-Source Agent Harnesses | `anomalyco/opencode`, `earendil-works/pi`, `openai/codex`, `google-gemini/gemini-cli` | 598.4k | Done | [Chunk 2 Summary](chunks/chunk-02-agent-harnesses/SUMMARY.md) |
| **Chunk 3** | Mature Autonomous & IDE-Native Heavyweights | `cline/cline`, `RooCodeInc/Roo-Code`, `OpenHands/OpenHands`, `aaif-goose/goose` | 247.4k | Done | [Chunk 3 Summary](chunks/chunk-03-autonomous-and-ide/SUMMARY.md) |
| **Chunk 4** | Agent-Native Orchestration & Memory | `openclaw/openclaw`, `paperclipai/paperclip`, `openai/symphony`, `gastownhall/beads` | 569.3k | Done | [Chunk 4 Summary](chunks/chunk-04-agent-native-orchestration/SUMMARY.md) |
| **Chunk 5** | Mobile, Terminal & Guardrail Specialists | `getpaseo/paseo`, `slopus/happy`, `manaflow-ai/cmux`, `smtg-ai/claude-squad`, `stackblitz-labs/bolt.diy`, `code-yeongyu/oh-my-openagent`, `zgsm-ai/costrict` | 183.6k | Done | [Chunk 5 Summary](chunks/chunk-05-specialists/SUMMARY.md) |
| **Chunk 6** | Agent Skill, Spec & Workflow Stacks | `mattpocock/skills`, `mattpocock/sandcastle`, `obra/superpowers`, `github/spec-kit`, `garrytan/gstack`, `Fission-AI/OpenSpec`, `gsd-build/get-shit-done`, `bmad-code-org/BMAD-METHOD`, `cursor/plugins/pstack` (path-scoped #36, stars excluded), `backnotprop/pstack`, `michael-denyer/pstack-claude` | 1,168.2k | Done | [Chunk 6 Summary](chunks/chunk-06-skill-stacks/SUMMARY.md) |

*Note on licenses: 34 of 36 repos are OSI open-source (`cursor/plugins/pstack` ships MIT in `pstack/LICENSE`); `code-yeongyu/oh-my-openagent` is source-available (SUL-1.0) and `manaflow-ai/cmux` has BSL-licensed server directories. All 36 are public GitHub repositories (or a public path in one). Combined stars still exclude #36.*

## Headline Findings

1. **High-throughput TypeScript repos encode recurring bugs in lint rules & static ratchets:** Teams (`t3code`, `orca`, `Paradev`, `emdash`, `opencode`, `openclaw`, `paseo`, `sandcastle`) encode recurring review catches directly into `oxlint`/Biome plugins with debt baselines and unit tests for the lint rules themselves.
2. **Contributor gating decides open backlog size (with important caveats):** GitHub's `open_issues_count` combines open issues and PRs. Open trackers accumulate massive backlogs (`codex`: 28,619; `orca`: 9,918), while default-closed gates (`pi`: 307 — auto-closing unapproved intake on arrival; `superpowers`: 372 with a maintainer-reported 94% PR rejection rate) keep queues tiny at the trade-off of public discoverability.
3. **Commit tests only for costly invariants, and verify them independently:** Combine `orca`'s `"Tests are the exception"` + zero-checkout `pr-test-loc.yml`, `OpenHands`'s `verify-skill-isolation.yml` (protecting `.agents/skills/verify-*/`), `oh-my-openagent`'s uncommitted `.omo/evidence/` + `sha256sum`, and `cmux`'s `### Observed / Not run` disclosure.
4. **Watch CI sprawl vs. team size:** Most small/mid-size repos sit cleanly around **8–30 YAML workflows**, whereas `1code` had `0` and `cmux` carries `231` (17 of its 20 stored Nov 25 commits by one maintainer touched CI/release automation). Large backed teams (`openclaw` 133, `orca` 67, `gemini-cli` 47) sustain more only with dedicated runner/cache engineering.
5. **Keep `AGENTS.md` lean, incident-cited, and anti-slop:** Pair `openclaw`'s *"A new rule cites an incident"* + *"Choose good compromises"*, `paseo`'s `Doc voice` cliché ban, `cmux`'s `REVIEW.md`, `BMAD`'s *"Prefer deleting an instruction to hedging it"*, and `paperclip`'s `grep`-indexed `rules/*.mdc`.
6. **Skill stacks organize workflow, not raw bug-fix rate:** `garrytan/gstack`'s own self-reported 100-task benchmark on Opus 5.5 found **58% (58/100) solved with `gstack` vs. 61.6% (61/99) without it**. The durable mechanical wins in Chunk 6 are `mattpocock/sandcastle`'s all-5-category `oxlint` + `lint-shrink.yml` bot, `mattpocock/skills`'s frontmatter YAML check + Codex/Claude invocation parity, `gstack`'s token-budget & egress-receipt tests, and `OpenSpec`'s CLI cold-start module guard.

## Repository Layout

```text
├── LICENSE                      # MIT License
├── README.md
├── RUBRIC.md
├── scripts/
│   ├── collect_chunk.py         # Reproducible GitHub API primary-source collector (whole repos)
│   └── collect_path.py          # Path-scoped collector for monorepo subdirectories (e.g. cursor/plugins/pstack)
├── data/                        # Raw JSON snapshots collected per chunk (36 JSONs; #36 is path-scoped)
│   ├── chunk-01/
│   ├── chunk-02/
│   ├── chunk-03/
│   ├── chunk-04/
│   ├── chunk-05/
│   └── chunk-06/
├── chunks/                      # 35 individual assessments + 6 chunk summaries (pstack family is 3 files)
│   ├── chunk-01-direct-rivals/
│   ├── chunk-02-agent-harnesses/
│   ├── chunk-03-autonomous-and-ide/
│   ├── chunk-04-agent-native-orchestration/
│   ├── chunk-05-specialists/
│   └── chunk-06-skill-stacks/
├── synthesis/
│   ├── EXECUTIVE_BRIEF.md
│   ├── MULTI_MODEL_REVIEW.md    # 3-model adversarial review & corrections log
│   └── PLAYBOOK.md
└── distribution/
    ├── x-article.md
    ├── x-launch-posts.md
    ├── upgrade-prompt.txt
    └── assets/
```
