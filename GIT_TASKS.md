# Git Task List, Checklist, and Summary

## Current Summary

This repository is in good shape as a **local operator baseline**.

What is true right now:
- core local operator flow is working
- evals are passing
- model-backed planning is optional
- heuristic planning remains the default
- the repo is suitable for controlled expansion
- the main remaining work is not core functionality
- the main remaining work is:
  - scope clarity
  - documentation truth
  - interactive edge-case hardening
  - CI enforcement
  - maintainability cleanup

## Current Git Summary

Use this repo state as the baseline for decisions:
- branch should be checked before work starts
- working tree should be clean before any major doc rewrite or refactor
- any untracked files must be either committed or removed in the same session
- `HANDOFF.md` should reflect the actual committed state, not transient local state

---

# Priority Checklist

## P0 — Repo Truth and Source-of-Truth Cleanup

- [ ] Decide the fate of `ai_engine/`
  - [ ] keep it and explicitly scope it
  - [ ] isolate it from the main baseline
  - [ ] remove it
- [ ] Resolve untracked REPL edge-case test files
  - [ ] `tests/test_repl_clarification_interrupts.py`
  - [ ] `tests/test_repl_edge_cases.py`
  - [ ] commit them or delete them
- [ ] Rewrite `HANDOFF.md`
  - [ ] remove absolute local paths
  - [ ] remove stale branch/version claims
  - [ ] remove stale test/eval counts
  - [ ] remove outdated remaining-work statements
  - [ ] reflect the current committed repo only

## P1 — Interactive Reliability

- [ ] Add or finalize tests for:
  - [ ] `KeyboardInterrupt` at clarification prompt
  - [ ] `EOFError` at clarification prompt
  - [ ] overwrite confirm/cancel paths
  - [ ] invalid `--resume` session ID
  - [ ] corrupted session/transcript files

## P2 — CI / Packaging

- [ ] Ensure CI runs:
  - [ ] `python -m pytest -q`
  - [ ] `python -m evals.run_all`
  - [ ] `./scripts/verify_clean_install.sh`
  - [ ] `python -m build`
  - [ ] install from built wheel
- [ ] Decide whether `evals/` should ship in the package

## P3 — Governance / Logging Policy

- [ ] Define transcript/log policy
  - [ ] local personal use only
  - [ ] plaintext acceptable for now
  - [ ] future expansion requires retention/redaction review

## P4 — Small Cleanup

- [ ] Replace deprecated `datetime.utcnow()` usage in `session_store.py`
  - [ ] use timezone-aware UTC timestamps
- [ ] Review warnings in test output until clean

## P5 — Maintainability Refactor

- [ ] Refactor root `repl.py` into smaller units
  - [ ] prompt/session UI
  - [ ] clarification flow
  - [ ] execution/reporting
- [ ] Add docstrings to:
  - [ ] `workflow.py`
  - [ ] `repl.py`
  - [ ] `session_store.py`

## P6 — Expansion Guardrails

- [ ] Keep heuristic planner as default
- [ ] Keep model-backed planner optional
- [ ] Only expand richer clarification after REPL edge-case tests are committed and stable
- [ ] Only formalize `planner_mode` in schema if expansion continues

---

# Suggested Execution Order

1. decide `ai_engine/`
2. commit or delete the two untracked test files
3. rewrite `HANDOFF.md`
4. wire evals contract into CI
5. finish REPL/session edge-case tests
6. strengthen packaging/build validation
7. document transcript/log policy
8. clean up `datetime.utcnow()` warnings
9. do refactor and longer-term maintainability work

---

# Git Command Checklist

## Inspect current state
```bash
git branch --show-current
git status --short
git log --oneline --decorate -10
