# AI Operator — Current Handoff

## Current repo state
- Current branch: `main`
- Current baseline tag: `model-planner-baseline`
- Remote branch aligned: `origin/main`
- Working tree status: verify with `git status --short`
- Latest verified test result: `23 passed`

## What is implemented
- terminal-first local operator
- heuristic planner
- optional model-backed planner behind feature flag
- planner mode reporting:
  - `heuristic`
  - `model`
  - `model_fallback`
- REPL
- session persistence
- transcript/history support
- clarification helpers
- chained planning support
- eval runners
- clean audit zip generation

## Current verified eval baseline
- classifier: `23/23`
- generator: `13/13`
- full: `12/12`
- clarification: `10/10`
- plan: `4/4`
- session: `4/4`
- `evals.run_all`: passing
- `evals.smoke`: passing

## Current priorities
1. keep `HANDOFF.md` aligned with the current committed repo
2. finalize remaining REPL/session end-to-end tests
3. define transcript/log policy
4. decide whether `evals/` should ship in the package
5. refactor `repl.py` into smaller units if expansion continues
6. only formalize `planner_mode` in schema if expansion continues

## Verification commands
- `python3 -m pytest -q`
- `python3 -m evals.run_all`
- `./scripts/verify_clean_install.sh`
