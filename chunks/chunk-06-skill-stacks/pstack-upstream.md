# pstack upstream (`cursor/plugins/pstack` · Lauren Tan / `poteto`)

- **Snapshot (path-scoped, collected 2026-11-26):** Canonical original is **not** a standalone `poteto/pstack` repo. It is the public subdirectory [`cursor/plugins/pstack`](https://github.com/cursor/plugins/tree/main/pstack), version **`0.15.48`**, author **Lauren Tan**, **MIT** (`pstack/LICENSE`, Copyright 2026 Lauren Tan). Host repo `cursor/plugins` is public (`19,691★` · `2,125` forks · `705` open items · last monorepo push `2026-11-26 09:04` UK time) — those counts are **monorepo-wide and must not be treated as pstack-only popularity**.
- **Primary stack:** 59 Agent Skills (`SKILL.md`), `/poteto-mode` router with 22 playbooks, **TLA+ statechart corpus (`39` `.tla`, `30,612` bytes)** plus TypeScript (`455,116` bytes) for `statechart` / `watch-pr` tooling, generated first-party Claude Code tree at [`harness/pstack`](https://github.com/cursor/plugins/tree/main/harness/pstack). **No `.lean` files in this upstream tree.**
- **Data source:** [`data/chunk-06/cursor__plugins__pstack.json`](../../data/chunk-06/cursor__plugins__pstack.json) (path-scoped collector `scripts/collect_path.py`; `scripts/collect_chunk.py` would have attributed the whole monorepo to this plugin).

## 1. Agent Instruction & Docs Hygiene
- **No `AGENTS.md` at `pstack/` or at the monorepo root.** The instruction surface is the `28,650`-byte README manifesto plus per-skill `SKILL.md` files, many marked `disable-model-invocation: true`.
- **Sharpest anti-slop manifesto in the skill-stack cohort (upstream README, quoted):**
  > *"i'm poteto. i'm not a president or ceo, but i've worked with millions of lines of code at Meta, Netflix, and Cursor. i'm also on the react core team where i help build and maintain react compiler... i don't want to ship like a team of twenty slop artists. throughput without quality is not a goal i aspire to. if you want to go fast, go deep first."*
- **Install surfaces (primary source):** Cursor `/add-plugin pstack`; Claude Code `/plugin marketplace add cursor/plugins` then `/plugin install pstack@cursor-plugins`. Claude Code consumes the **generated** tree under `harness/pstack/` (do-not-edit-by-hand; CI fails if it drifts).
- **`/poteto-mode` is the entry router** over standalone skills (`unslop`, `how`, `why`, `tdd`, `arena`, `swarm`, `interrogate`, `reflect`, `reframe`, `statechart`, …) and composites (`create-verification-skill`, `create-formal-verification-skill`, `poteto-mode`). README states 22 playbooks.

## 2. Mechanical Gates & Quality Control
- **Monorepo workflow `validate-plugins.yml` is path-filtered to `pstack/**`, `harness/**`, plugin manifests, and schemas.** On PRs it: (1) validates plugin definitions (`scripts/validate-plugins.mjs`), (2) runs `node scripts/generate-pstack-harness-trees.mjs --check`, (3) runs `node --test pstack/skills/*/scripts/test/*.test.ts` (statechart + watch-pr tests). This is real plugin CI, but it is **one workflow in a multi-plugin repo**, not a custom lint ratchet.
- **No root `oxlint` / Biome / Knip config in the pstack subtree.** No pstack-local `.github/workflows/` directory (CI lives at repo root).
- **`/create-formal-verification-skill` is a product skill for consumer repos**, not a gate on pstack itself. The skill's text defaults TLA+ for ordering/concurrency questions and allows a proof assistant, SMT verifier, or Kani-class tool when the question needs it. A generated TLA+ check is supposed to be read with `/statechart`.

## 3. Architectural Bets & Craft
- **Formal verification as a first-class coding-agent skill** (`/create-formal-verification-skill` + `/maintain-formal-verification-skill` + `/statechart`). Upstream ships a **TLA+ test corpus** (`30.6 KB` across 39 `.tla` files) used to test the statechart compiler. **Lean is not in this tree.** **Lean is a pstack-claude addition** (`lean/Model/WatchPoll.lean`, `51,998` bytes) — see comparison below — and is not present in upstream or the backnotprop mirror.
- **First-party multi-harness story is generation, not a community port:** `harness/pstack/README.md` says the Claude Code tree is generated from `pstack/skills`, agents, docs, README, LICENSE, and `plugin.json`. Cursor uses `pstack/` directly.
- **Subtree size:** `554` files, `6,152,724` bytes (includes guide JPEGs and large `.out` fixtures).

## 4. Commit, PR & Maintenance Reality
- **Path-filtered last 50 commits on `pstack/`:** `2026-10-14 23:11` to `2026-11-24 00:41` UK time (**`50` / `40.1` days**), **`88%` conventional**, **`32%` fix/revert**, **`56%` AI co-author signal**, **`50/50` by `poteto`**. Tip commit `9e278fe` (*"feat(pstack): have /reframe list the problems a vague description could be (#1326)"*, bumps **0.15.48**).
- **`poteto/plugins` is a stale fork of `cursor/plugins`, not the current source.** Last `path=pstack` commit there is `2026-06-07` (`v0.9.0`). Host fork last push `2026-10-27`. Do not assess that fork as upstream.
- **Contributor gate for the host repo was not fully reviewed** (no pstack-specific vouch/auto-close bot observed in this pass). Unverified.

## 5. Steal vs. Avoid
- **Steal:**
  1. `/create-formal-verification-skill` (TLA+ default, leave a rerunnable project-local skill) plus `/statechart` to render checker counterexamples.
  2. Generated first-party harness tree + `--check` CI so Cursor and Claude Code cannot silently drift.
  3. Path-filtered monorepo CI that runs real `node --test` suites for plugin scripts.
- **Avoid:**
  1. Treating `cursor/plugins` star/issue counts as pstack's.
  2. Treating `poteto/plugins` as current upstream (it is months behind).
  3. Attributing pstack-claude's Lean `WatchPoll` model, `tools/forks.json` CI, or `open-pstack` installer to upstream.

## Comparison with the two assessed ports

| | `cursor/plugins/pstack` (this assessment) | [`backnotprop/pstack`](pstack.md) | [`michael-denyer/pstack-claude`](pstack-claude.md) |
| --- | --- | --- | --- |
| Role | Canonical upstream (Cursor plugin + generated Claude Code tree) | Standalone **mirror** for `npx skills add` / non-Cursor harnesses | **Build-time translation** port + installer + extra formal artifacts |
| Version at this check | `0.15.48` @ `9e278fe` (`2026-11-24 00:41` UK time) | Synced to the same `9e278fe` / `0.15.48` (its `SYNC-LOG.md`) | Own versioning (`v0.9.155` on `2026-11-24 20:25` UK time) |
| Skills | 59 skill folders | **Same 59 names** (exact set match in this pass) | Ported skill tree plus `tools/`, `installer/`, `tests/` |
| TLA+ | `30,612` B corpus under `skills/statechart/scripts/test/` | Same language total (`30,612` B TLA) | `48,807` B TLA (corpus + extra `tla/PiScheduler.tla`) |
| Lean | **None in tree** | **None** in language stats / tree search | **`lean/Model/WatchPoll.lean` (`51,998` B)** — purpose not fully read; filename suggests watch-pr polling. Unverified beyond path/size. |
| CI | Host `validate-plugins.yml` (schema + generated-tree `--check` + skill script tests) | `0` workflows; daily sync logs | `6` workflows (`forks.json`, `--check-rules`, Windows tests, scorecard, dependency-review, plugin scanner) |
| Last-50 velocity | `50` / **40.1 days**, 88% conv, 56% AI, all `poteto` | `50` / **27.9 days**, 2% conv, 2% AI, 49/50 `backnotprop` (mostly sync logs) | `50` / **6.5 days**, 0% AI in snapshot, mixed authors |
| Known port-only patches | n/a | Codex `agents/openai.yaml`; `no-comments` exception; `watch-pr` fork-PR / control-character hardening (from `cursor/plugins#1194`, noted as not necessarily upstream) | Cross-harness rewrite layer; `open-pstack` installer; Lean + extra TLA |

*Unverified in this assessment:* whether `#1194` watch-pr hardening has since landed in `0.15.48` upstream; the exact theorem/model in `WatchPoll.lean`; host-repo contributor policy beyond the one workflow file.
