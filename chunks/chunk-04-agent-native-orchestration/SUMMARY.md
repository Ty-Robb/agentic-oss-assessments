# Chunk 4 Summary — Agent-Native Orchestration & Memory

*Snapshot date: 2026-11-25. Combined stars in this chunk: **569,309★**.*

## Side-by-Side Matrix

| Repo | Stars | Open Issues | Primary Stack | `AGENTS.md` / Skills | Signature Mechanical Gate | CI Workflows | Last-50 Velocity & Hygiene |
| --- | ---: | ---: | --- | --- | --- | ---: | --- |
| **[`openclaw/openclaw`](openclaw.md)** | 395.2k | 9,182 | TS (**474.7 MB**!) + Swift/Kotlin/Rust, pnpm isolated, Kysely, SolidJS | 123-line (<20 KB) `AGENTS.md` ("new rule cites an incident") + **55 skills** | Strictest `.oxlintrc.json` (`correctness`/`perf`/`suspicious` = `"error"`), `prefix-stability.test.ts`, 7-day `minimumReleaseAgeStrict`, `periphery`, 20-PR cap | **133** | 50 commits / **2.3 hrs** · 98% conv · 64% fix · 8% AI trailer (trailers banned; `roboclaw-bot` 3.8k commits) |
| **[`paperclipai/paperclip`](paperclip.md)** | 116.9k | 6,812 | TS (157.8 MB) + Rust runner, Express/React/Drizzle/Postgres, Turbo | 221-line `AGENTS.md` + `grep`-indexed `rules/*.mdc` + **37 skills** + `maps/` | `pnpm verify` (incremental + exit code 2), real Postgres `pg_dump`/restore CI, 1,000-line file cap, `crash-points` & chaos evals | 41 | 50 commits / **14.5 hrs** · 94% conv · 56% fix · 58% AI |
| **[`openai/symphony`](symphony.md)** | 28.2k | **0** | **`SPEC.md`** + 914 KB Elixir/OTP + Burrito | Spec-first (`SPEC.md` + 41-line README) | `mix pr_body.check`, language-agnostic spec ("ask your agent to build it") | 4 | 47 commits / **6 mos** · 17% conv · 10.6% fix · 21% AI |
| **[`gastownhall/beads`](beads.md)** | 29.0k | 1,828 | Go (51.4 MB) + Bazel + embedded/server Dolt | 245-line `AGENTS.md` + symlink `CLAUDE.md` + 15-row `engdocs/` table | Bazel `nogo` + anonymous `--config=fork-cache`, `main-ci-alert.yml`, `scripts/gh-body-lint`, `NOT_ENOUGH_INFO` & "verify test actually ran" rules | 23 | 50 commits / **8.0 days** · 100% conv · 82% fix · **100% AI** (`gascity-eddie[bot]` = 41/50!) |

## Key Patterns Across Chunk 4

1. **This chunk shows the two extreme poles of AI-era architecture — both work for opposite reasons:**
   - **Maximalist agent-built platforms (`OpenClaw` 475 MB TS / 133 workflows; `Paperclip` 158 MB TS / 41 workflows):** Survive extreme multi-agent velocity (50 commits every 2–14 hours!) *only* by investing heavily in mechanical invariants (`oxlint` all-error triad, `pnpm verify`, real Postgres backup/restore proofs, prompt-prefix stability tests, 37–55 procedural skills, and automated bot triage).
   - **Minimalist spec-as-product (`Symphony` 914 KB Elixir + `SPEC.md`):** Avoids the entire maintenance treadmill by publishing a crisp specification that any team's agent can re-implement natively in their own language.

2. **Autonomous bot-operated maintenance is already live in production OSS:**
   - In `beads`, `gascity-eddie[bot]` authored **41 of the last 50 commits** (100% conventional, 100% `Agent-Signature:`, burning down backlog bugs via a labeled review/merge pipeline) while preserving external contributor credit.
   - In `openclaw`, `roboclaw-bot` (3,873 commits) and `openclaw-mantis[bot]` (1,001 commits) operate alongside Peter Steinberger's 70,042 contributions.

3. **Three universal agent-engineering laws crystallized in Chunk 4:**
   - **Anti-overengineering guardrails (`OpenClaw`):** Explicitly instruct agents to choose cheap, recoverable mechanisms (idempotency key + one check + retry) and cite an incident before adding any new rule to `AGENTS.md`.
   - **Progressive rule indexing (`Paperclip`):** Keep rules in `rules/*.mdc` with frontmatter headers so agents `grep` headers cheaply instead of paying 20k tokens per turn.
   - **Anti-vacuous verification (`Beads` & `OpenClaw`):** Prove the real failing boundary end-to-end, never trust a filtered test run that silently skipped all subtests, and require `NOT_ENOUGH_INFO` when evidence runs out.
