# Chunk 6 Summary — Agent Skill, Spec & Workflow Stacks

*Snapshot date: 2026-11-25. Combined stars in this chunk: **1,168,180★** across 10 repositories (bringing the full 34-repo study to **2,903,100★ / ~2.90M combined stars**).*

## Side-by-Side Matrix

| Repo | Who Built It | Stars | Open Issues | Status | Primary Stack | `AGENTS.md` / Policy | Signature Mechanical Gate | Workflows | Last-50 Velocity & Hygiene |
| --- | --- | ---: | ---: | --- | --- | --- | --- | ---: | --- |
| **[`mattpocock/skills`](mattpocock-skills.md)** | **Matt Pocock** | 332.8k | 251 | Active | Markdown skills + 20 KB Shell/JS, Changesets | 33-line `AGENTS.md`, collaborators-only PRs, `SCOPE.md`, zero em-dashes, fresh-context subagents | Installer-parity YAML frontmatter CI (`check-frontmatter.mjs`), `disable-model-invocation` + `agents/openai.yaml` | 4 | 50 / **7.1 wks** · 16% conv · 6% fix · 66% AI |
| **[`mattpocock/sandcastle`](mattpocock-sandcastle.md)** | **Matt Pocock** | 9.3k | 137 | Active | 2.6 MB TS, TS 7, Effect, `oxlint-tsgolint`, Biome fmt | 41-line `AGENTS.md` + `GLOSSARY.md` | **All-5-category `oxlint` straitjacket + automated `lint-shrink.yml` bot**, real `bwrap`/Windows/macOS CI, `tests/docs-guide.test.ts`, `api-report/` | 8 | 50 / **6.0 days** · **98% conv** · 8% fix · 98% AI |
| **[`obra/superpowers`](superpowers.md)** | **Jesse Vincent** (`obra`) | 326.5k | 372 | Active | Markdown skills + 520 KB Shell/JS, 15+ harness plugins | 121-line `AGENTS.md` (**94% PR rejection rate**), human <200w summary, full model/plugin disclosure | External real-CLI eval lab (`superpowers-evals`: Quorum + Gauntlet QA), `"react todo list"` bootstrap acceptance test | **0** | 50 / **4.0 mos** · 78% conv · 12% fix · 14% AI |
| **[`github/spec-kit`](spec-kit.md)** | **GitHub** | 151.4k | 230 | Active | 11.9 MB Python (`uv`, Typer, MCP SDK, Hatchling) | 76-line `AGENTS.md` + **Evidence Gate** (`CONTRIBUTING.md`) | **GitHub Agentic Workflows (`gh-aw`)** in digest-pinned firewall containers + constrained `safe-outputs`, Ruff `S602`–`S605` | 29 | 50 / **7.0 days** · 78% conv · 60% fix · 34% AI |
| **[`garrytan/gstack`](gstack.md)** | **Garry Tan** (YC CEO) | 142.6k | **45** | Active | **45.1 MB TS** + Bun + Playwright/Aside + compiled CLIs | 18.6 KB `AGENTS.md` + 35.5 KB `CLAUDE.md` + honest **58 vs 61/99** benchmark admission | `catalog-budget` & `context-budget` ratchets, `egress-receipt-wiring.test.ts`, `$150/wk`-capped pre-registered eval sweeps | 38 | 50 / **1.8 days** · 0% conv (plain titles) · **100% AI** (`garrytan` = 50/50) |
| **[`Fission-AI/OpenSpec`](openspec.md)** | **Fission AI** (`TabishB`, `clay-good`) | 75.7k | 214 | Active | 5.8 MB TS, Node 22+, pnpm 10, Vitest 5, Nix | **0-byte empty `AGENTS.md`**, maintainers/invited-only PRs, 2-PR proposal→code flow | **`startup-modules.test.ts`** (CLI cold-start guard), GHSA-annotated `pnpm-workspace.yaml` overrides, npm OIDC | 5 | 50 / **25 days** · 86% conv · 40% fix · 98% AI |
| **[`gsd-build/get-shit-done`](get-shit-done.md)** | **TÂCHES / `trek-e`** | 64.1k | 0 | **Archived** (May '26) | 7.3 MB CJS + 2.6 MB TS SDK, `node:test` + `c8` | 41-line `AGENTS.md` + 791-line `CONTRIBUTING.md`; archived after compromise warning → `open-gsd/gsd-core` | `prompt-injection-scan.sh` + `base64-scan.sh`, `lint-no-source-grep.cjs`, `<issue#>-<slug>` ADRs, `auto-close-deprecated.yml` | 20 | Archived May 31, '26 · 80% conv · 40% fix · 72% AI |
| **[`bmad-code-org/BMAD-METHOD`](bmad-method.md)** | **BMAD** (`bmadcode`, `alexeyv`) | 55.7k | 116 | Active | 1.8 MB Python (`uv`, Jinja2, Ruff) + Astro docs | 35-line SHA-verified `AGENTS.md` (*"length is paid on every run; prefer deleting to hedging"*) | `validate_skills.py --strict` (PyYAML), PEP 723 inline-dep skill scripts, `ready_for_review`-only AI review, `retarget-pr.yaml` | 5 | 50 / **27 days** · 92% conv · 46% fix · 6% AI |
| **[`pstack`](pstack.md)** (`backnotprop/pstack` + `michael-denyer/pstack-claude`) | Orig. **Lauren Tan (`poteto`)** at Cursor; community ports | 5.2k / 4.9k | 2 / 16 | Active | Agent Skills + 1.8 MB TS/JS + **Lean (52 KB) + TLA+ (49 KB)** | Anti-slop manifesto (*"go deep first"*), `poteto-mode` router, formal verification skills | **`tools/forks.json` declared-fork CI check**, `--check-rules` dead-substitution guard, `hol-plugin-scanner.yml`, Windows hook CI | 0 / 6 | `pstack-claude`: 50 / **6.5 days** · 2% conv · 0% AI |

## Key Findings: Harness Engineering (Chunks 1–5) vs. Skill-Stack Engineering (Chunk 6)

1. **Skill stacks do NOT magically boost raw bug-fix rates — they enforce workflow, review, QA, and safety:**
   - `garrytan/gstack`'s own November 2026 head-to-head benchmark (published directly in its `README.md`) is the single most important empirical receipt in the study: on 100 real GitHub bugs/features, Opus 5.5 solved **58 with `gstack`** vs. **61 of 99 without it** (and 29 vs. 29 on 60 security fixes).
   - That validates our core finding from Chunks 1–5: **mechanical repo gates** (linters, tests, sandboxes, ratchets) fix code quality; **skills** shape human–agent alignment (`/grill-me`, `brainstorming`), structured review, formal verification (`pstack`'s TLA+/Lean), and shipping rituals.

2. **The biggest philosophical split in Chunk 6 — Composable Skills vs. Process-Owning SDLC Frameworks:**
   - **Composable / lightweight camp (`mattpocock/skills`, `pstack`, `OpenSpec`):** Small, opt-in skills (`/grill-me`, `unslop`, `how`/`why`, `GLOSSARY.md`) that keep the human engineer in control.
   - **Full-process SDLC camp (`gstack`, `superpowers`, `spec-kit`, `BMAD-METHOD`, `get-shit-done`):** End-to-end roleplay or spec pipelines. Notice that `get-shit-done` collapsed into a governance/compromise migration (`archived`), `BMAD` v7 had to add a *"small changes go straight to build"* escape hatch, and `gstack` swelled to **45.1 MB of TypeScript + 38 CI workflows** to keep its own skills from regressing!

3. **Five elite mechanical engineering inventions discovered in Chunk 6:**
   - **Automated shrink-only ratchet bot (`mattpocock/sandcastle` — `lint-shrink.yml`):** Combines an all-5-category `oxlint` straitjacket with a bot that automatically lowers lint/type/test baselines and raises the E2E coverage floor on every push to `main`.
   - **Prompt & catalog token-budget ratchets + mandatory egress receipts (`gstack`):** Caps always-loaded skill catalogs (`2,292` tokens), pins per-skill token ceilings, and fails CI on any off-machine `curl`/`git`/fetch call lacking an egress receipt.
   - **Firewall-sandboxed GitHub Agentic Workflows (`github/spec-kit` — `gh-aw`):** Digest-pinned firewall containers + domain allowlists + constrained `safe-outputs` (`allowed-files`, `draft: true`, `max: 1`).
   - **Prompt-economics & fresh-context rules (`BMAD` + `mattpocock/skills` + `pstack`):** *"Length and ambiguity are paid on every run; prefer deleting to hedging"*; always start subagents with a fresh context window (countering Codex's default fork); pair `disable-model-invocation: true` with `agents/openai.yaml` so Codex doesn't auto-load interactive skills.
   - **Declared fork registries & formal verification skills (`pstack-claude`) + CLI cold-start module tests (`OpenSpec` — `startup-modules.test.ts`) + `prompt-injection-scan.sh` (`GSD`).**

4. **Skill repos face an even worse AI-PR slop wave than runtime repos — and locked their doors even harder:**
   - `obra/superpowers` explicitly advertises a **94% PR rejection rate** (and keeps open issues at 372 for 326.5k★).
   - `mattpocock/skills` (251 open issues at 332.8k★) and `OpenSpec` (214 at 75.7k★) restrict PRs to **collaborators / invited contributors only**.
   - `garrytan/gstack` keeps open issues at **45** at 142.6k★.
