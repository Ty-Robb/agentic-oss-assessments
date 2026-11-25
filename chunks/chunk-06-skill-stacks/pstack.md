# pstack Ecosystem (`cursor/plugins/pstack` · `backnotprop/pstack` · `michael-denyer/pstack-claude`)

- **Snapshot:** Upstream by **Lauren Tan (`poteto`)** in `cursor/plugins/pstack` (Cursor Principal Engineer / React Core Team); tracked via canonical standalone ports:
  - [`backnotprop/pstack`](https://github.com/backnotprop/pstack): `5,167★` · `395` forks · `2` open issues · `MIT` · Active (pushed 2026-11-25)
  - [`michael-denyer/pstack-claude`](https://github.com/michael-denyer/pstack-claude): `4,872★` · `452` forks · `16` open issues · `MIT` · Active (pushed 2026-11-25)
  - *(Plus T3 Code-native ports `chhoumann/t3-pstack` 322★ & `uzairansaruzi/p3-stack` 164★)*
- **Primary Stack:** Agent Skills (`SKILL.md`), TypeScript/JS tooling (~1.8 MB in `pstack-claude`), **Lean (`52 KB`) + TLA+ (`48.8 KB`)** formal verification artifacts, Mermaid statecharts, Bun 1.4.4, `open-pstack` cross-harness CLI installer.
- **Data sources:** [`data/chunk-06/backnotprop__pstack.json`](../../data/chunk-06/backnotprop__pstack.json) · [`data/chunk-06/michael-denyer__pstack-claude.json`](../../data/chunk-06/michael-denyer__pstack-claude.json)

## 1. Agent Instruction & Docs Hygiene
- **Sharpest anti-slop manifesto in the skill-stack cohort (Poteto's upstream README):**
  > *"i'm poteto. i'm not a president or ceo, but i've worked with millions of lines of code at Meta, Netflix, and Cursor. i'm also on the react core team where i help build and maintain react compiler... i don't want to ship like a team of twenty slop artists. throughput without quality is not a goal i aspire to. if you want to go fast, go deep first."*
- **Composable skill graph + `/poteto-mode` entry router:** Cleanly separates standalone skills (`unslop`, `how`, `why`, `tdd`, `arena`, `swarm`, `interrogate`, `reflect`, `show-me-your-work`, `blast-radius`, `statechart`, `reframe`) from dependent composite skills (`create-verification-skill`, `create-formal-verification-skill`, `poteto-mode`).
- **Key cross-harness discovery documented in both ports:** Codex CLI ignores `disable-model-invocation: true` in `SKILL.md`, so explicit-only skills require a companion `agents/openai.yaml` to keep them out of Codex's startup context (`backnotprop/pstack#26`).

## 2. Mechanical Gates & Quality Control
- **Two starkly different port engineering models:**
  - **`backnotprop/pstack` (`0` workflows):** Lightweight daily mirror (`SYNC-LOG.md`, `MIRROR.md`) optimized for `npx skills add backnotprop/pstack` with minimal surgical patches (e.g., `watch-pr` stripping control characters and excluding fork PRs from watched stacks to prevent prompt injection).
  - **`michael-denyer/pstack-claude` (`6` workflows — a masterclass in maintaining a multi-harness downstream port):**
    1. **Declared fork registry (`tools/forks.json`) enforced in CI:** CI runs a dry-run sync against `tools/upstream.json` and **fails** if any file forked from upstream is undeclared or if a declared fork is stale!
    2. **Self-pruning substitution rules (`tools/substitutions.json` + `--check-rules`):** Every mechanical Cursor→Claude/Codex/Pi rewrite requires a `rationale` field; CI fails if any rule matches zero upstream files (forcing deletion or conversion to a denylist entry that catches upstream re-introducing Cursor-isms).
    3. **3-way `git merge-file` upstream sync (`tools/sync.mjs`):** Preserves file modes, refuses to follow or write through symlinks (security boundary), and isolates port-only features into separate files (`watch-pr/shipping.ts`) to prevent merge conflicts.
    4. **Real Windows CI & security scanning:** Warms up PowerShell `ConvertFrom-Json` before timing Windows session-hook tests, runs `worktree-audit.test.mjs` and `installer.test.mjs` on `windows-latest`, plus `hol-plugin-scanner.yml` (AI plugin security scanner), OpenSSF `scorecard.yml`, and `dependency-review.yml`.

## 3. Architectural Bets & Craft
- **Formal verification as a first-class coding-agent skill:** Unlike every other skill pack in Chunk 6, `pstack` (and `michael-denyer/pstack-claude`) invests in **`/create-formal-verification-skill`** — picking the riskiest concurrency property or invariant in a repo, verifying it with **TLA+ (`48.8 KB`), Lean (`52 KB`), or Kani**, and leaving behind a reusable project-local verification skill that future agents rerun!
- **Build-time translation over runtime translation (`pstack-claude`):** Translates Cursor-specific primitives to Claude Code / Codex / Pi / OpenCode / Copilot / Antigravity / Grok / Muse *at build/install time* instead of burning runtime prompt tokens asking the model to mentally map tool names.
- **Avoids double-loading trap:** `open-pstack` refuses to select `~/.agents/skills` by default because Codex and OpenCode read both their plugin dir and `~/.agents/skills`, which would silently load every skill twice.

## 4. Commit, PR & Maintenance Reality
- **`backnotprop/pstack`:** 50 commits in 28 days (49/50 by `backnotprop`), mostly daily upstream sync logs (`0.15.44` → `0.15.48`), 2% conv, 2% AI signal.
- **`michael-denyer/pstack-claude`:** **50 commits in 6.5 days** (`2026-11-19` to `2026-11-25`, `v0.9.151` → `v0.9.155`), 30/50 by `michael-denyer` + active community contributors (`oliver-mee`, `abc123931`, `flipcyde101`, `wes-davis`), shipping real cross-harness fixes (Windows `cmd.exe` `%NAME%` escaping, cloud-session REST fallback when GraphQL is blocked, Codex forked-chat routing).

## 5. Steal vs. Avoid
- **Steal:**
  1. **Formal verification skill generation (`/create-formal-verification-skill` with TLA+/Lean/Kani)** for concurrency, state-machine, and billing invariants that unit tests miss.
  2. **Declared fork registry (`tools/forks.json`) + dead-rule CI check (`--check-rules`)** for *any* team maintaining a downstream fork or cross-harness translation layer.
  3. **Build-time harness translation + avoiding `~/.agents/skills` double-loading** across multi-agent setups.
  4. **`watch-pr` prompt-injection hardening:** exclude untrusted fork PRs from watched stacks and strip control characters from review text/paths before feeding into agent context.
- **Avoid:**
  1. **Installing `poteto-mode` wholesale without checking implicit-invocation config on Codex** — always verify `agents/openai.yaml` so leaf principles don't bloat startup context.
