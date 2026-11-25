# Chunk 2 Summary — Flagship Open-Source Agent Harnesses

*Snapshot date: 2026-11-25. Combined stars in this chunk: **598,420★**.*

## Side-by-Side Matrix

| Repo | Stars | Open Issues | Primary Stack | `AGENTS.md` / Docs | Signature Mechanical Gate | CI Workflows | Last-50 Velocity & Hygiene |
| --- | ---: | ---: | --- | --- | --- | ---: | --- |
| **[`anomalyco/opencode`](opencode.md)** | 229.1k | 4,172 | TS (Effect v4, Bun, Solid/OpenTUI) + Rust daemon | 221 lines `AGENTS.md` + `.opencode/skills/` | Custom `anti-slop` + `anti-slop-effect` `oxlint` plugins, tested `ast-grep` rules, Rust Miri, `check-bot-scope`, 7 triage workflows | 21 | 50 commits / **12.3 hrs** · 100% conv · 60% fix · `opencode-agent[bot]` #3 contributor (2,766 commits) |
| **[`earendil-works/pi`](pi.md)** | 123.8k | **307** | TS (plain npm workspaces, Node erasable TS, Biome) | 160 lines `AGENTS.md` + `.pi/skills/` | Default-closed `lgtmi`/`lgtm` contributor gate, exact dep/install-lock gates, GritQL Biome plugin, multi-agent Git safety rules | 16 | 50 commits / **1.7 days** · 90% conv · 60% fix · 2% AI |
| **[`openai/codex`](codex.md)** | 136.4k | 28,619 | Rust (90.7 MB) + Bazel/Cargo + pnpm SDKs | No root `AGENTS.md`; 15 crisp `docs/` + `.worktreeinclude` | `blocking-ci` + `CI required` aggregator, `verify_tui_core_boundary.py`, `minimumReleaseAge: 10080` npm 7-day cooldown | 31 | 50 commits / **14.7 hrs** · 0% conv (plain imperative) · 6% fix · 0% AI |
| **[`google-gemini/gemini-cli`](gemini-cli.md)** | 109.1k | 751 | TS (npm workspaces, Ink, esbuild/SEA, ESLint) | `GEMINI.md` + 571-line `CONTRIBUTING.md` + generated docs | 47-file behavioral `evals/` + 2-stage `eval-pr.yml` approval gate + `agent-session-drift-check.yml` + `deflake`/memory/perf suites | 47 | 50 commits / **18.1 days** · 88% conv · 70% fix · 14% AI |

## Key Patterns Across Flagship Harnesses

1. **The Open-Issue Stress Test proves contributor gating works:**
   - `openai/codex` (136k★, open tracker + AI dedup/label bots): **28,619 open issues**.
   - `anomalyco/opencode` (229k★, 7 automated triage/slop workflows): **4,172 open issues**.
   - `pingdotgg/t3code` (78.8k★, `VOUCHED.td` + PR limits): **3,681 open issues**.
   - `earendil-works/pi` (123.8k★, **default-closed `lgtmi`/`lgtm` gate**): **307 open issues** — a 93× reduction vs. Codex!

2. **Every top harness invented a distinct mechanical defense worth stealing:**
   - **OpenCode:** `anti-slop` custom oxlint plugin + tested `ast-grep` rules directly targeting LLM coding tics (`no-widen-then-assert`, `no-runtime-typeof`, `no-module-mocking`, `require-safety-comment-for-type-assertion`) + `check-bot-scope.yml` + `"test": "do not run tests from root"`.
   - **Pi:** Multi-agent safe Git instructions (never `git add -A`/`stash`/`reset`, review PRs without switching branches), `npm ci --ignore-scripts` + pre-commit lockfile guard + erasable TypeScript + tagged-union discipline.
   - **Codex:** `pnpm-workspace.yaml` 7-day npm supply-chain cooldown (`minimumReleaseAge: 10080`, `blockExoticSubdeps`, `strictDepBuilds`), `blocking-ci.yml` + `if: always()` single aggregator job, and Python boundary-check scripts (`verify_tui_core_boundary.py`).
   - **Gemini CLI:** 47 behavioral evals (`frugalReads`, `prompt_injection_mcp`, `answer-vs-act`, `validation_fidelity`) behind a secure two-stage `pull_request_target` approval gate (`eval-pr.yml`), plus a zero-checkout file-pair migration drift bot (`agent-session-drift-check.yml`).

3. **Explicit `Co-Authored-By` trailers undercount agent work at elite repos:**
   - OpenCode shows only 4% AI trailers on its last 50 commits, yet `opencode-agent[bot]` is its **#3 all-time contributor with 2,766 commits**. Pi, Codex, and T3 Code similarly have high agent velocity with low trailer noise — meaning clean squash-merged PR titles beat noisy bot trailers.
