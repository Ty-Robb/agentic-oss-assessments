# Agentic OSS Assessments

Structured, primary-source engineering and agent-workflow assessments of **T3 Code rivals** and **high-signal open-source AI coding / orchestration tools** (23 repositories across 5 chunks + `pingdotgg/t3code` as baseline).

Every assessment inspects the real repository via GitHub API (file trees, `AGENTS.md`/`CLAUDE.md`, CI workflows, lint/type/eval gates, commit history, contributor distribution, and architectural boundaries) — not marketing copy.

## Progress

| Chunk | Theme | Repositories | Status | Summary |
| --- | --- | --- | --- | --- |
| Baseline | Reference Control Plane | `pingdotgg/t3code` | Reference | [RUBRIC.md](RUBRIC.md) |
| **Chunk 1** | Direct T3 Code Rivals (Worktree GUIs) | `ParadevAI/Paradev`, `BloopAI/vibe-kanban`, `generalaction/emdash`, `21st-dev/1code` | In Progress | [Chunk 1 Summary](chunks/chunk-01-direct-rivals/SUMMARY.md) |
| **Chunk 2** | Flagship Open-Source Agent Harnesses | `anomalyco/opencode`, `earendil-works/pi`, `openai/codex`, `google-gemini/gemini-cli` | Pending | [Chunk 2 Summary](chunks/chunk-02-agent-harnesses/SUMMARY.md) |
| **Chunk 3** | Mature Autonomous & IDE-Native Heavyweights | `cline/cline`, `RooCodeInc/Roo-Code`, `OpenHands/OpenHands`, `aaif-goose/goose` | Pending | [Chunk 3 Summary](chunks/chunk-03-autonomous-and-ide/SUMMARY.md) |
| **Chunk 4** | Agent-Native Orchestration & Memory | `openclaw/openclaw`, `paperclipai/paperclip`, `openai/symphony`, `gastownhall/beads` | Pending | [Chunk 4 Summary](chunks/chunk-04-agent-native-orchestration/SUMMARY.md) |
| **Chunk 5** | Mobile, Terminal & Guardrail Specialists | `getpaseo/paseo`, `slopus/happy`, `manaflow-ai/cmux`, `smtg-ai/claude-squad`, `stackblitz-labs/bolt.diy`, `code-yeongyu/oh-my-openagent`, `zgsm-ai/costrict` | Pending | [Chunk 5 Summary](chunks/chunk-05-specialists/SUMMARY.md) |

## Cross-Repo Synthesis

- [synthesis/PLAYBOOK.md](synthesis/PLAYBOOK.md) — Rolling, ranked engineering & agentic-workflow playbook ("what to steal vs. what to avoid"), updated after every chunk.

## Repository Layout

```text
├── README.md
├── RUBRIC.md
├── scripts/
│   └── collect_chunk.py         # Reproducible GitHub API primary-source collector
├── data/                        # Raw JSON snapshots collected per chunk (git-tracked for auditability)
├── chunks/
│   ├── chunk-01-direct-rivals/
│   ├── chunk-02-agent-harnesses/
│   ├── chunk-03-autonomous-and-ide/
│   ├── chunk-04-agent-native-orchestration/
│   └── chunk-05-specialists/
└── synthesis/
    └── PLAYBOOK.md
```
