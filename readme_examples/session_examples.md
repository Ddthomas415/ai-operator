# Session Examples

## One-shot CLI

```bash
python3 main.py 'write a file named hello.py with print("hello")'
python3 main.py 'read hello.py'
```

## Clarification in REPL

```text
task> write a python file
CLARIFICATION NEEDED:
What should the Python filename be?
> hello.py
```

## Rephrase unsupported intent

```text
task> open my file
CLARIFICATION NEEDED:
Can you rephrase that as a request to read or create a Python file?
> read hello.py
```

## REPL history

```text
task> history
HISTORY:
1. write a python file
2. read hello.py
```
