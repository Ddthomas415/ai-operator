# Jarvis Expansion Task Map

This repository is not a full "Jarvis AI" system today. It is a safe local operator. The practical path from the current codebase to a broader assistant is:

## Phase 1: Broaden local file operations

- add `edit_file`
- add `list_workspace`
- support controlled overwrite and update flows
- expand evals for new actions
- preserve sandbox guarantees

## Phase 2: Better planning

Completed in this workspace:

- added structured action schemas
- added a structured multi-step request planner

Still remaining:

- replace heuristic parsing with a model-backed planner
- improve clarification for multi-field requests
- add confidence calibration and fallback behavior

## Phase 3: Multi-step local workflows

Completed in this workspace:

- support chained file operations
- add resumable session state
- add richer history and transcripts

Still remaining:

- add richer task decomposition

## Phase 4: Tool expansion

- add optional shell tooling behind explicit safety gates
- add search/browse only if intentionally enabled
- add code-aware editing tools
- add repo inspection commands

## Phase 5: Productization

- add formal tests beyond eval scripts
- add CI
- add packaging and release workflow
- add configuration management
- add telemetry policy and docs

## Phase 6: Optional "Jarvis-like" capabilities

- voice or desktop surfaces
- autonomous background jobs
- memory and retrieval
- browser automation
- multi-agent orchestration

Those later phases are intentionally out of scope for the current repository baseline. The implementation in this workspace now covers Phase 1 plus the first concrete slice of Phase 2 and Phase 3.
