# Git Task List, Checklist, and Summary

## Current Summary

This repository is in good shape as a **local operator baseline**.

What is true right now:
- core local operator flow is working
- evals are passing
- model-backed planning is optional
- heuristic planning remains the default
- the repo is suitable for controlled expansion
- the main remaining work is:
  - documentation truth
  - packaging decision
  - maintainability cleanup

## Priority Checklist

## P0 — Repo Truth
- [ ] keep `HANDOFF.md` aligned with the current committed repo

## P1 — Interactive Reliability
- [x] add clarification prompt interrupt tests
- [x] add REPL/session edge-case tests
- [x] add invalid `--resume` session behavior coverage
- [x] add corrupted session/transcript file coverage
- [x] add overwrite confirm/cancel paths end-to-end

## P2 — CI / Packaging
- [x] ensure CI runs:
  - [x] `python -m pytest -q`
  - [x] `python -m evals.run_all`
  - [x] `./scripts/verify_clean_install.sh`
  - [x] `python -m build`
- [ ] decide whether `evals/` should ship in the package

## P3 — Governance / Logging Policy
- [x] define transcript/log policy
  - [x] local personal use only
  - [x] plaintext acceptable for now
  - [x] future expansion requires retention/redaction review

## P4 — Small Cleanup
- [x] replace deprecated `datetime.utcnow()` usage in `session_store.py`
- [ ] review warnings in test output until clean

## P5 — Maintainability Refactor
- [ ] refactor root `repl.py` into smaller units
  - [ ] prompt/session UI
  - [ ] clarification flow
  - [ ] execution/reporting
- [ ] add docstrings to:
  - [ ] `workflow.py`
  - [ ] `repl.py`
  - [ ] `session_store.py`

## P6 — Expansion Guardrails
- [x] keep heuristic planner as default
- [x] keep model-backed planner optional
- [x] add explicit planner mode reporting
- [ ] only formalize `planner_mode` in schema if expansion continues

## Suggested Execution Order

1. update and commit `HANDOFF.md` and `GIT_TASKS.md`
2. verify baseline still passes
3. decide whether `evals/` should ship in the package
4. do maintainability refactor
