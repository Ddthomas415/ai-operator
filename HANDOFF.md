# AI Operator — Current Handoff

## Current repo state
- Current branch: `feature/model-backed-planner`
- Current HEAD: `7db3b7a`
- Remote branch aligned: `origin/feature/model-backed-planner`
- Working tree status at audit capture: clean
- Latest recorded test result: `10 passed`

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
1. harden REPL edge cases
2. strengthen CI/build verification
3. decide fate of `ai_engine/`
4. keep model-backed planning optional until explicitly verified with real API config

## Known open questions
- Should `ai_engine/` remain in this repo?
- Should `planner_mode` become a formal schema field?
- Should `evals/` ship in the package?

## Verification commands
- python3 -m pytest -q
- python3 -m evals.run_all
- ./scripts/verify_clean_install.sh
