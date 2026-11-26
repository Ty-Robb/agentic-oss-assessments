# pstack-claude (`michael-denyer/pstack-claude`)

- **Snapshot:** `4,872★` · `452` forks · `16` open items · `MIT` · Active (pushed `2026-11-25`) — multi-harness downstream **translation port** of Lauren Tan's (`poteto`) canonical Cursor plugin [`cursor/plugins/pstack`](pstack-upstream.md) (see also the faithful standalone mirror [`backnotprop/pstack`](pstack.md)).
- **Primary Stack:** Agent Skills (`SKILL.md`), TypeScript/JS tooling (~1.8 MB), Mermaid statecharts, Bun 1.4.4, `open-pstack` cross-harness CLI installer, plus formal artifacts that include the upstream TLA+ statechart corpus **and port-only additions**: **`lean/Model/WatchPoll.lean` (`51,998` bytes)** and **`tla/PiScheduler.tla`**, bringing language totals to **Lean `52 KB` + TLA+ `48.8 KB`**. Neither Lean file nor `PiScheduler.tla` is present in upstream or the backnotprop mirror. The exact theorem in `WatchPoll.lean` was not fully read in this assessment (unverified beyond path and size).
- **Data source:** [`data/chunk-06/michael-denyer__pstack-claude.json`](../../data/chunk-06/michael-denyer__pstack-claude.json)

## 1. Agent Instruction & Docs Hygiene
- **Build-time harness translation over runtime prompt overhead:** Translates Cursor-specific primitives to Claude Code, Codex, Pi, OpenCode, Copilot, Antigravity, Grok, and Muse at install/build time rather than burning runtime tokens on tool-name mapping.
- **Cross-harness invocation parity:** Pairs `disable-model-invocation: true` in `SKILL.md` with per-skill `agents/openai.yaml` (`policy.allow_implicit_invocation: false`) so Codex CLI does not silently auto-load manual skills.
- **Avoids double-loading trap:** `open-pstack` refuses to select `~/.agents/skills` by default because Codex and OpenCode read both their plugin dir and `~/.agents/skills`.

## 2. Mechanical Gates & Quality Control (`6` YAML Workflows)
1. **Declared fork registry (`tools/forks.json`) enforced in CI:** CI runs a dry-run sync against `tools/upstream.json` and **fails** if any file forked from upstream is undeclared or stale.
2. **Self-pruning substitution rules (`tools/substitutions.json` + `--check-rules`):** Every mechanical Cursor→Claude/Codex/Pi rewrite requires a `rationale` field; CI fails if any rule matches zero upstream files.
3. **3-way `git merge-file` upstream sync (`tools/sync.mjs`):** Preserves file modes, refuses to follow or write through symlinks, and isolates port-only features into separate files (`watch-pr/shipping.ts`).
4. **Windows CI & security scanning:** Warms up PowerShell `ConvertFrom-Json` before timing Windows session-hook tests, runs `worktree-audit.test.mjs` and `installer.test.mjs` on `windows-latest`, plus `hol-plugin-scanner.yml`, OpenSSF `scorecard.yml`, and `dependency-review.yml`.

## 3. Formal Verification as a Project-Local Skill
- Invests in **`/create-formal-verification-skill`** — selecting the riskiest concurrency property or invariant in a consumer repo and leaving behind a reusable project-local verification skill. In *this* repo, formal artifacts are **`lean/Model/WatchPoll.lean` (`51,998` bytes)** and **TLA+ `48.8 KB`** (upstream statechart corpus plus port-only `tla/PiScheduler.tla`). Upstream and the backnotprop mirror do not ship the Lean model.

## 4. Velocity & Maintenance Reality
- **50 commits in 6.5 days** (`2026-11-19` to `2026-11-25`, `v0.9.151` → `v0.9.155`), 30/50 by `michael-denyer` alongside active community contributors shipping real cross-harness fixes (Windows `cmd.exe` `%NAME%` escaping, cloud-session REST fallback when GraphQL is blocked, Codex forked-chat routing).

## 5. Steal vs. Avoid
- **Steal:** Declared fork registry (`tools/forks.json`) + dead-rule `--check-rules` CI gate, build-time cross-harness translation, and `watch-pr` prompt-injection hardening (excluding untrusted fork PRs and stripping control characters).
- **Avoid:** Installing `poteto-mode` wholesale without checking per-skill `agents/openai.yaml` on Codex so leaf principles don't bloat startup context.
