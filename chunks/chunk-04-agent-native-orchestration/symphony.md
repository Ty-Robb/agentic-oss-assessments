# OpenAI Symphony (`openai/symphony`)

- **Snapshot:** `28,155★` · `2,904` forks · `0` open issues · `Apache-2.0` · Preview/Reference (created Feb 26, 2026; last pushed 2026-09-15)
- **Primary Stack:** Specification (`SPEC.md`) + tiny **Elixir/OTP** reference implementation (`elixir/`, 914 KB Elixir), Burrito single-binary packaging, `mise` toolchain manager, 4 GitHub Actions workflows.
- **Data source:** [`data/chunk-04/openai__symphony.json`](../../data/chunk-04/openai__symphony.json)

## 1. Agent Instruction & Docs Hygiene
- **Spec-first radical minimalism:** No root `AGENTS.md`, `CLAUDE.md`, or `CONTRIBUTING.md`; the entire repository centers on **`SPEC.md`** and a 41-line `README.md`.
- **"Implement it with your agent" distribution model:** README Option 1 literally tells users to point their coding agent at `SPEC.md` and generate Symphony in whatever language their team runs — treating a crisp, language-agnostic specification as a first-class open-source deliverable!
- **Only 2 files in `docs/`** (smoke board review & smoke test one).

## 2. Mechanical Gates & Quality Control
- **Ultra-lean 4-workflow CI:** `make-all.yml`, `pr-description-lint.yml`, `burrito-nightly.yml`, and `burrito-release.yml`.
- **Clean PR body linter (`pr-description-lint.yml`):** Uses `mix pr_body.check --file /tmp/pr_body.md` (with JSON-escaped `PR_BODY_JSON` via `jq -r` to avoid shell injection) to enforce structured PR proof-of-work sections.
- **Proof-of-work contract:** Symphony's core thesis (from OpenAI's *Harness Engineering* post) is that autonomous issue-to-PR runs only work when the target repo already has strong harness engineering — and every agent PR produces CI status, review feedback, complexity analysis, and walkthrough video proof.

## 3. Architectural Bets & Craft
- **Elixir/OTP as a deliberate concurrency bet:** Using Elixir/BEAM for the reference daemon gives lightweight process supervision, fault isolation, clean retry timers, and hot-reloaded `WORKFLOW.md` polling in under 1 MB of code — a sharp contrast to 150–475 MB TypeScript monorepos!
- **Generic issue-tracker adapter boundary:** Cleanly decoupled tracker interface with adapters for Linear, GitHub Issues, Jira Cloud, Asana, and GitLab Issues (including blocking-issue link gating and safe terminal workspace cleanup) added cleanly in ~20 commits.
- **Burrito single-binary packaging:** Compiles the Elixir/OTP release into standalone executables for frictionless installs.

## 4. Commit, PR & Maintenance Reality
- **Small, focused reference preview:** Only **47 total commits** (Mar–Sep 2026), 72% authored by `frantic-openai` (34 commits), 21.3% explicit AI co-author, 17% conventional commits, 10.6% fix/revert.
- **0 open issues** — maintained strictly as a specification + low-key reference preview rather than a community-driven product.

## 5. Steal vs. Avoid
- **Steal:**
  1. **Writing a self-contained `SPEC.md`** so any team (or agent) can re-implement an orchestration daemon cleanly in their own stack instead of adopting a massive monolithic framework.
  2. **Blocking-issue awareness + safe terminal workspace cleanup + anchored local roots** (commits `#108`, `cbd2158d`, `7cf29df6`) as core invariants for autonomous issue runners.
  3. **`mix pr_body.check` (lightweight PR body linter)** passing PR body safely via `toJson(...) | jq -r` into a temp file instead of inline shell interpolation.
- **Avoid:**
  1. **Assuming an autonomous issue-to-PR daemon works without harness engineering first:** Symphony's own README warns it only pays off *after* a repo has strong automated tests, linters, and verification proofs.
