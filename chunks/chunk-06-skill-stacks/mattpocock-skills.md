# Matt Pocock's Skills (`mattpocock/skills`)

- **Snapshot:** `332,787★` (#1 most-starred agent skills repo on GitHub) · `27,987` forks · **`251` open issues** · `MIT` · Active (created Feb 3, 2026; pushed 2026-11-25)
- **Primary Stack:** Pure Markdown skills + 13.7 KB Shell + 6.7 KB JS; npm + Changesets, Claude Code plugin (`.claude-plugin/plugin.json` + `marketplace.json`), Codex/Copilot/Gemini/skills.sh installers, `yaml` frontmatter validator.
- **Data source:** [`data/chunk-06/mattpocock__skills.json`](../../data/chunk-06/mattpocock__skills.json)

## 1. Agent Instruction & Docs Hygiene
- **Direct philosophical challenge to heavy SDD frameworks (`README.md`):** *"Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control and make bugs in the process hard to resolve. These skills are designed to be small, easy to adapt, and composable."*
- **Crisp 33-line `AGENTS.md` (4.2 KB) with five standout skill-repo invariants:**
  1. **5-bucket maturity lifecycle:** `engineering/`, `productivity/` (promoted — shipped in plugin + docs page), `misc/`, `in-progress/` (public beta, excluded from plugin/docs), `deprecated/`.
  2. **Explicit User-invoked vs. Model-invoked split:** User-only skills set *both* `disable-model-invocation: true` (Claude Code) **and** `policy.allow_implicit_invocation: false` in `agents/openai.yaml` (Codex) so interactive workflows never fire accidentally.
  3. **Fresh-context subagent rule:** *"Every skill that dispatches a subagent says to start it with a fresh context window. Some harnesses (Codex, for one) fork the parent conversation by default, and a fork inherits the parent's context, which is what the subagent was meant to escape."*
  4. **Router-sync invariant:** Whenever any user-reachable skill is added, renamed, or changed, `ask-matt` (the meta-router skill) must be updated in the same change — *"a stale router is a router that lies."*
  5. **Strict anti-slop prose rule:** *"No em-dashes anywhere in this repo's prose... Where a sentence reaches for one, rewrite it instead with a comma, colon, period, parentheses, or a conjunction; never do a blind character substitution."*
- **Minor hygiene nit:** `CLAUDE.md` is a byte-for-byte 4,206-byte duplicate of `AGENTS.md` rather than a symlink.

## 2. Mechanical Gates & Quality Control
- **Lean 4-workflow CI:** `check.yml`, `needs-info.yml`, `release.yml`, `triage-label.yml`.
- **Installer-parity YAML frontmatter gate (`check.yml`):** Added directly after a real incident (`#1453` / `#1455` — *"check every SKILL.md's frontmatter parses with the installer's YAML parser"*), plus `claude plugin validate . --strict` and `sync-plugin-version.mjs --check`.
- **Ultra-strict issue-tracker defense (`CONTRIBUTING.md` + `SCOPE.md` + `.out-of-scope/`):**
  - **PRs are open to collaborators only** — keeps open issues to **251** at **332.8k★** (1,326 stars per open issue!).
  - Explicitly regulates AI-drafted issues: *One problem per issue; Short (fits on one screen); Repro first; No pasted specs or rewritten `SKILL.md` files; Not your project's issues.*

## 3. Architectural Bets & Craft
- **Composable failure-mode fixes over monolithic SDLC frameworks:**
  - `/grill-me` & `/grill-with-docs` fix human–agent requirement misalignment before code is written.
  - **`GLOSSARY.md` (DDD ubiquitous language)** fixes verbose agent prose by giving the model exact project terminology.
  - `/setup-matt-pocock-skills` adapts skills to each repo's own issue tracker, labels, and doc paths instead of forcing a rigid layout.
  - `scripts/link-skills.sh` symlinks local skills straight into `~/.claude/skills` and `~/.agents/skills` so `git pull` updates live sessions.

## 4. Commit, PR & Maintenance Reality
- **Deliberate, founder-curated cadence:** **50 commits over 7 weeks** (`2026-10-06` to `2026-11-25`), 16% conventional, 6% fix/revert, **66% AI signal** (`mattpocock` 42/50 + `bot` 6/50 + `github-actions[bot]` 1/50; 512 all-time by `mattpocock`).
- Active evolution into multi-agent factory skills (`chief-of-staff`, `software-factory`, `implement-spec` spawning a fresh implementer subagent per ticket).

## 5. Steal vs. Avoid
- **Steal:**
  1. **Fresh-context subagent rule** (explicitly countering Codex's default fork behavior).
  2. **Explicit `disable-model-invocation: true` + `agents/openai.yaml` parity** so interactive skills never fire implicitly on Codex or Claude Code.
  3. **Collaborators-only PRs + `SCOPE.md` + `.out-of-scope/` + "AI-drafted issues must fit on one screen, repro first, no pasted specs."**
  4. **Parsing `SKILL.md` frontmatter in CI with the installer's exact YAML parser** (`check-frontmatter.mjs`).
  5. **Project `GLOSSARY.md`** (DDD ubiquitous language) paired with `/grill-me` alignment before coding.
- **Avoid:**
  1. **Duplicating `AGENTS.md` into `CLAUDE.md`** as two separate files instead of a symlink.
