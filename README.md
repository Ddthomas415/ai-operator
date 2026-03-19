# AI Operator

AI Operator is a terminal-first Python tool for local development workflows. It converts plain-English requests into safe local file operations through a structured planner -> generator -> executor pipeline constrained to `workspace/`.

## Product scope

Current supported workflow:

- create a Python file from a plain-English request
- read a Python file back
- edit an existing Python file from a plain-English request
- list Python files in `workspace/`
- ask for clarification when the filename is missing or the intent is unclear
- chain multiple safe local actions in one request using `and then`

Current intentional constraints:

- local file operations only
- Python files only
- workspace sandbox only
- no shell execution
- no browser automation
- no background agents

## Architecture

```text
User input
  -> structured plan
  -> clarification gate
  -> per-step generator
  -> per-step executor
  -> workspace/
  -> logger
```

Key modules:

- [main.py](/Users/baitus/ai-operator/main.py): one-shot CLI
- [repl.py](/Users/baitus/ai-operator/repl.py): interactive clarification loop
- [planner/classifier.py](/Users/baitus/ai-operator/planner/classifier.py): intent classification
- [planner/generator.py](/Users/baitus/ai-operator/planner/generator.py): payload generation
- [planner/plan_builder.py](/Users/baitus/ai-operator/planner/plan_builder.py): multi-step request planning
- [planner/schema.py](/Users/baitus/ai-operator/planner/schema.py): structured plan and step schemas
- [executor/actions.py](/Users/baitus/ai-operator/executor/actions.py): sandboxed file reads and writes
- [logger.py](/Users/baitus/ai-operator/logger.py): JSONL event logging
- [workflow.py](/Users/baitus/ai-operator/workflow.py): shared flow helpers used by CLI, REPL, and evals

## Requirements

- Python 3.11+
- `uv` is optional

## Setup

Using Python directly:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

Using `uv`:

```bash
uv sync
```

## Run

One-shot CLI:

```bash
python3 main.py 'write a file named hello.py with print("hello")'
python3 main.py 'read hello.py'
python3 main.py 'edit hello.py with print("updated")'
python3 main.py 'list workspace files'
python3 main.py 'write a file named flow.py with print("x") and then read flow.py'
python3 -m ai_operator 'read hello.py'
```

Interactive REPL:

```bash
python3 repl.py
python3 -m ai_operator.repl
python3 repl.py --resume-last
```

REPL features:

- clarification loop for missing filenames
- follow-up rephrase for unsupported prompts
- multi-step plans in one request
- `history` command for the current session
- `transcript` command for the saved session transcript
- resumable sessions via `--resume <session_id>` or `--resume-last`
- overwrite confirmation before replacing an existing file

One-shot CLI behavior:

- stops on clarification-needed states
- refuses to overwrite an existing file

## Verification

Individual eval suites:

```bash
python3 -m evals.run_eval
python3 -m evals.run_generator_eval
python3 -m evals.run_full_eval
python3 -m evals.run_clarification_eval
python3 -m evals.run_plan_eval
python3 -m evals.run_session_eval
```

Run all evals:

```bash
python3 -m evals.smoke
```

## Safety model

- all file access is restricted to `workspace/`
- path traversal such as `../evil.py` is rejected
- only `.py` files are accepted
- workspace listing only returns Python source files
- write operations require overwrite confirmation in REPL mode
- write operations are rejected in one-shot mode if the target already exists

## Logging

Logs are written to `logs/events.jsonl`.
Session transcripts are written to `logs/sessions/<session_id>.jsonl`.

Each event includes:

- `ts`
- `input`
- `action`
- `confidence`
- `status`
- `error_type`
- `message`

`logs/` and `workspace/` are intentionally ignored by Git.

## Version state

- `main`: stable repo baseline
- `v1`: first stable tag
- current working branch in this workspace: `v2-clarification-loop`

## Docs

- full handoff: [HANDOFF.md](/Users/baitus/ai-operator/HANDOFF.md)
- session examples: [readme_examples/session_examples.md](/Users/baitus/ai-operator/readme_examples/session_examples.md)
- change log: [CHANGELOG.md](/Users/baitus/ai-operator/CHANGELOG.md)

## Known limitations

- scope is intentionally limited to Python file reads and writes
- edits replace full file contents rather than applying semantic patches
- content generation is still heuristic, not model-backed
- multi-step clarification is still limited to the first ambiguous step

## Roadmap

The repo now includes the first expansion slice beyond the original narrow core plus a structured multi-step planner. The broader remaining expansion path is mapped in [JARVIS_TASK_MAP.md](/Users/baitus/ai-operator/JARVIS_TASK_MAP.md).
