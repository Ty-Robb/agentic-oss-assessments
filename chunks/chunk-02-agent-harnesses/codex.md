# OpenAI Codex CLI (`openai/codex`)

- **Snapshot:** `136,407★` · `21,631` forks · `28,619` open issues · `Apache-2.0` · Active (pushed 2026-11-25)
- **Primary Stack:** Massive Rust workspace (90.7 MB Rust, 1.8 MB Python, Bazel + RBE + Cargo dual build, `justfile`, thin npm/Python SDK wrappers, embedded V8/rusty_v8, packaged ripgrep).
- **Data source:** [`data/chunk-02/openai__codex.json`](../../data/chunk-02/openai__codex.json)

## 1. Agent Instruction & Docs Hygiene
- **Surprisingly minimal root agent instructions:** No root `AGENTS.md` or `CLAUDE.md` (though `docs/agents_md.md` documents the `AGENTS.md` standard Codex popularized, and nested guides may live under `codex-rs/`).
- **Clean, user-focused `docs/` (15 files):** Covers `sandbox.md`, `execpolicy.md`, `agents_md.md`, `skills.md`, `config.md`, `contributing.md`, `open-source-fund.md`. Root README stays ultra-crisp (81 lines) and is mechanically checked by `asciicheck.py` and `readme_toc.py`.
- **Worktree awareness:** Ships `.worktreeinclude` at root to declare untracked files copied into new worktrees.

## 2. Mechanical Gates & Quality Control
- **Gold-standard CI merge-gate architecture (`blocking-ci.yml` + `postmerge-ci.yml`):**
  - Separates merge-blocking fast checks (`blocking-ci.yml`: Bazel, `blob-size-policy`, `cargo-deny`, `codespell`, `repo-checks`, `rust-ci`, `sdk`) from heavy main-only postmerge suites (`postmerge-ci.yml`: `rust-ci-full`, `v8-canary`).
  - Uses a single final aggregator job (`CI required`, `if: always()`) running `.github/scripts/check_ci_results.py` on `toJSON(needs)` so branch rulesets only pin one check and a failed dependency can never silently skip the gate!
- **Architectural invariants enforced as fast Python CI checks (`repo-checks.yml`):**
  - `verify_tui_core_boundary.py`: enforces that `codex-tui` never imports `codex-core` directly (and recent commit `#63898` just dropped `codex-core` from `app-server` transport too!).
  - `verify_cargo_workspace_manifests.py`: enforces workspace inheritance across every crate.
  - `verify_bazel_clippy_lints.py`: keeps Bazel and Cargo clippy lints in lockstep.
  - `blob-size-policy.yml`: blocks accidental large binary blobs from entering git history.
  - `rust-release-argument-comment-lint.yml` & `check-clean-worktree` (fails CI if any build/test dirtied tracked files).
  - Unit tests for **all** release, installer, PyPI verification, and macOS signing scripts!
- **Best-in-class npm supply-chain hardening (`pnpm-workspace.yaml`):**
  - `minimumReleaseAge: 10080` (7-day quarantine before installing newly published npm versions!)
  - `blockExoticSubdeps: true`, `strictDepBuilds: true`, `trustPolicy: no-downgrade`
  - SHA-512 hash pinned directly on `packageManager: pnpm@10.34.5+sha512...`.
- **Automated PR hygiene:** `close-stale-contributor-prs.yml` (closes inactive collaborator PRs after 14 days), `issue-deduplicator.yml`, `issue-labeler.yml`, `issue-translator.yml`.

## 3. Architectural Bets & Craft
- **Full Rust rewrite paid off in performance & sandboxing:** 90.7 MB of Rust compiled via both Cargo and Bazel (with remote build execution `rbe.bzl`), shipping single native binaries (`musl` Linux, macOS, Windows) plus `codex app-server` JSON-RPC protocol (consumed by T3 Code and other GUIs).
- **Strict crate decoupling:** Actively peeling `codex-core` out of both `codex-tui` and `app-server` transport so protocol/UI layers stay thin and fast to compile.
- **High-cadence alpha releases:** Multiple tagged alpha releases *per day* (`rust-v0.174.0-alpha.1` through `alpha.5` in 24 hours).

## 4. Commit, PR & Maintenance Reality
- **Industrial-scale team velocity:** Last 50 commits landed in **14.7 hours** (PR `#63,898`), driven by a large full-time OpenAI engineering org (`jif-oai` 2,105, `etraut-openai` 1,149, `bolinfest` 1,057, `pakrym-oai` 623, `charliemarsh-oai` 320, etc.).
- **Plain imperative commit titles:** 0% conventional-commit prefixes (e.g., `Drop the production dependency on codex-core from app-server transport (#63898)`), 0% explicit AI co-author trailers.
- **Open-issue explosion without a gate:** **28,619 open issues** (even with automated deduplicator/labeler/translator bots) — stark proof that passive AI triage cannot keep up with 136k-star inbound volume the way Pi's default-closed gate does.

## 5. Steal vs. Avoid
- **Steal:**
  1. **`pnpm-workspace.yaml` supply-chain hardening** (`minimumReleaseAge: 10080`, `blockExoticSubdeps: true`, `strictDepBuilds: true`, `trustPolicy: no-downgrade`) — 5 lines that neutralize most npm supply-chain attacks.
  2. **Single-entrypoint `blocking-ci.yml` with an `if: always()` `CI required` aggregator** + separate `postmerge-ci.yml` for slow suites.
  3. **Fast repo-invariant CI scripts** (`verify_*_boundary.py`, `blob-size-policy`, `check-clean-worktree`, and unit tests for release/signing scripts).
  4. **`.worktreeinclude`** for declaring untracked local files that worktrees should copy automatically.
- **Avoid:**
  1. **Dual Bazel + Cargo build systems** unless you have a Google/OpenAI-sized infra team maintaining `verify_bazel_clippy_lints.py` and RBE.
  2. **Relying solely on AI dedup/labeling bots without a contribution gate** at 100k+ stars — leads to 28k+ unmanageable open issues.
