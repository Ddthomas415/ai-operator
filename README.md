# AI Operator

A terminal-first AI operator for local development workflows.

## Current scope

This version supports:

- write_file
- read_file
- clarification for ambiguous requests
- sandboxed file access inside `workspace/`
- JSONL logging
- classifier, generator, and full evals

## Run

python3 main.py 'write a file named demo.py with print("yo")'
python3 main.py 'read demo.py'

## Evals

python3 -m evals.run_eval
python3 -m evals.run_generator_eval
python3 -m evals.run_full_eval
