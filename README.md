# Agentic OSS Assessments

> **Live Website:** **[https://ty-robb.github.io/agentic-oss-assessments/](https://ty-robb.github.io/agentic-oss-assessments/)** — Interactive 34-repo explorer, charts, one-click Repo Upgrade Prompt, Playbook, Executive Brief, and individual audit pages.

Structured, primary-source engineering and agent-workflow assessments of **T3 Code rivals**, **flagship AI coding harnesses**, **orchestration platforms**, and **agent skill/workflow stacks** (**34 repositories** — 33 assessed across 6 chunks + `pingdotgg/t3code` as baseline; **2.90M combined GitHub stars** as of **2026-11-25**).

Every assessment inspects the real repository via GitHub API (file trees, `AGENTS.md`/`CLAUDE.md`, CI workflows, lint/type/eval gates, commit history, contributor distribution, and architectural boundaries) — not marketing copy.

## Start Here

- **[`synthesis/EXECUTIVE_BRIEF.md`](synthesis/EXECUTIVE_BRIEF.md)** — 5-minute distilled briefing covering everything learned across all 34 repos.
- **[`synthesis/PLAYBOOK.md`](synthesis/PLAYBOOK.md)** — Master 34-repo comparison matrix, 6 empirical laws of agentic OSS, tiered **Steal Immediately / Steal as You Scale / Anti-Patterns** playbook, and a concrete Week 1–3 rollout plan for TypeScript monorepos.
- **[`distribution/x-article.md`](distribution/x-article.md)** & **[`distribution/x-launch-posts.md`](distribution/x-launch-posts.md)** — Ready-to-publish X Article, 2-card light-mode Research Note launch kit, copy-paste prompt (`upgrade-prompt.txt`), and retina PNG visuals under `distribution/assets/`.
- **[`RUBRIC.md`](RUBRIC.md)** — Standardized 5-axis evaluation rubric and `pingdotgg/t3code` reference baseline.

## Assessment Coverage

| Chunk | Theme | Repositories | Combined Stars | Status | Summary |
| --- | --- | --- | ---: | --- | --- |
| Baseline | Reference Control Plane | `pingdotgg/t3code` | 78.8k | Reference | [RUBRIC.md](RUBRIC.md) |
| **Chunk 1** | Direct T3 Code Rivals (Worktree GUIs) | `ParadevAI/Paradev`, `BloopAI/vibe-kanban`, `generalaction/emdash`, `21st-dev/1code` | 57.3k | Done | [Chunk 1 Summary](chunks/chunk-01-direct-rivals/SUMMARY.md) |
| **Chunk 2** | Flagship Open-Source Agent Harnesses | `anomalyco/opencode`, `earendil-works/pi`, `openai/codex`, `google-gemini/gemini-cli` | 598.4k | Done | [Chunk 2 Summary](chunks/chunk-02-agent-harnesses/SUMMARY.md) |
| **Chunk 3** | Mature Autonomous & IDE-Native Heavyweights | `cline/cline`, `RooCodeInc/Roo-Code`, `OpenHands/OpenHands`, `aaif-goose/goose` | 247.4k | Done | [Chunk 3 Summary](chunks/chunk-03-autonomous-and-ide/SUMMARY.md) |
| **Chunk 4** | Agent-Native Orchestration & Memory | `openclaw/openclaw`, `paperclipai/paperclip`, `openai/symphony`, `gastownhall/beads` | 569.3k | Done | [Chunk 4 Summary](chunks/chunk-04-agent-native-orchestration/SUMMARY.md) |
| **Chunk 5** | Mobile, Terminal & Guardrail Specialists | `getpaseo/paseo`, `slopus/happy`, `manaflow-ai/cmux`, `smtg-ai/claude-squad`, `stackblitz-labs/bolt.diy`, `code-yeongyu/oh-my-openagent`, `zgsm-ai/costrict` | 183.6k | Done | [Chunk 5 Summary](chunks/chunk-05-specialists/SUMMARY.md) |
| **Chunk 6** | Agent Skill, Spec & Workflow Stacks | `mattpocock/skills`, `mattpocock/sandcastle`, `obra/superpowers`, `github/spec-kit`, `garrytan/gstack`, `Fission-AI/OpenSpec`, `gsd-build/get-shit-done`, `bmad-code-org/BMAD-METHOD`, `backnotprop/pstack`, `michael-denyer/pstack-claude` | 1,168.2k | Done | [Chunk 6 Summary](chunks/chunk-06-skill-stacks/SUMMARY.md) |

## Headline Findings

1. **Custom lint rules > prose rules:** Surviving high-velocity repos (`t3code`, `Paradev`, `emdash`, `opencode`, `openclaw`, `paseo`) encode domain invariants into `oxlint`/Biome plugins with per-file debt ratchets and unit tests for the lint rules themselves.
2. **Contributor gating decides issue-tracker survival:** Default-closed `lgtmi`/`lgtm` (`pi`: 307 open issues at 123.8k★) outperforms open trackers (`codex`: 28,619 open issues at 136.4k★) by **93×**.
3. **Verification must be independent and anti-vacuous:** `OpenHands` blocks implementor PRs from editing verification skills (`verify-skill-isolation.yml`) and runs diff-scoped Stryker mutation testing; `oh-my-openagent` enforces uncommitted local `.omo/evidence/` + `sha256sum` PR proofs; `beads` and `cmux` guard against silently skipped tests.
4. **Watch the CI Goldilocks zone:** Zero CI (`1code`) ended in archival in 7 weeks, while 231 workflows (`cmux`) led to ~80% of sampled `main` commits being spent maintaining CI/runner machinery itself. The sweet spot across the healthiest repos is **12–30 focused workflows**.
5. **Keep `AGENTS.md` lean, incident-cited, and anti-slop:** Pair `openclaw`'s *"A new rule cites an incident"* + *"Choose good compromises"*, `paseo`'s `Doc voice` LLM cliché ban, `cmux`'s `REVIEW.md`, `BMAD`'s *"prefer deleting an instruction to hedging it"*, and `paperclip`'s `grep`-indexed `rules/*.mdc`.
6. **Skill stacks organize workflow, not raw model fix rate:** `garrytan/gstack`'s own 100-bug benchmark shows **58/100 solved with `gstack` vs. 61/99 without it**. The enduring wins in Chunk 6 are mechanical: `mattpocock/sandcastle`'s automated shrink-only `lint-shrink.yml` ratchet bot + all-5-category type-aware `oxlint`, `mattpocock/skills`'s fresh-context subagent rule + frontmatter YAML validation, `obra/superpowers`'s upfront 94% PR rejection policy + external CLI eval lab, `pstack`'s project-local TLA+/Lean formal verification skills, and `gsd-build/get-shit-done`'s compromise postmortem showing why supply-chain hygiene matters as much for prompt stacks as code repos.

## Repository Layout

```text
├── README.md
├── RUBRIC.md
├── scripts/
│   ├── collect_chunk.py         # Reproducible GitHub API primary-source collector
│   └── build_site.py            # Zero-dependency GitHub Pages site generator -> docs/
├── docs/                        # Published GitHub Pages site (https://ty-robb.github.io/agentic-oss-assessments/)
├── data/                        # Raw JSON snapshots collected per chunk (git-tracked for auditability)
│   ├── chunk-01/
│   ├── chunk-02/
│   ├── chunk-03/
│   ├── chunk-04/
│   ├── chunk-05/
│   └── chunk-06/
├── chunks/
│   ├── chunk-01-direct-rivals/
│   ├── chunk-02-agent-harnesses/
│   ├── chunk-03-autonomous-and-ide/
│   ├── chunk-04-agent-native-orchestration/
│   ├── chunk-05-specialists/
│   └── chunk-06-skill-stacks/
├── synthesis/
│   ├── EXECUTIVE_BRIEF.md
│   └── PLAYBOOK.md
└── distribution/
    ├── x-article.md
    ├── x-launch-posts.md
    ├── upgrade-prompt.txt
    └── assets/
```
