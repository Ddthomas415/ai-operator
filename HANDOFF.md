# AI Operator — Current Handoff

## Current repo state
- Current branch: `main`
- Current baseline tag: `model-planner-baseline`
- Remote branch aligned: `origin/main`
- Working tree status: verify with `git status --short`
- Latest verified test result: `18 passed`

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

## Current priorities
1. harden remaining REPL/session edge cases
2. keep CI/build verification strong
3. keep model-backed planning optional until explicitly verified with real API config
4. decide whether `planner_mode` should become a formal schema field
5. decide whether `evals/` should ship in the package

## Verification commands
- python3 -m pytest -q
- python3 -m evals.run_all
- ./scripts/verify_clean_install.sh
