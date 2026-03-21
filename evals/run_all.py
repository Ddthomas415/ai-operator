import subprocess
import sys

REQUIRED = [
    [sys.executable, "-m", "evals.run_eval"],
    [sys.executable, "-m", "evals.run_generator_eval"],
    [sys.executable, "-m", "evals.run_full_eval"],
]

OPTIONAL = [
    [sys.executable, "-m", "evals.run_clarification_eval"],
    [sys.executable, "-m", "evals.run_plan_eval"],
    [sys.executable, "-m", "evals.run_session_eval"],
    [sys.executable, "-m", "evals.smoke"],
]

def run(cmd: list[str]) -> None:
    print(f"\n==> {' '.join(cmd)}")
    completed = subprocess.run(cmd)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)

def main() -> None:
    for cmd in REQUIRED:
        run(cmd)

    for cmd in OPTIONAL:
        completed = subprocess.run(cmd)
        if completed.returncode == 0:
            print(f"\n==> {' '.join(cmd)}")
        else:
            print(f"\n==> skipping optional runner: {' '.join(cmd)}")

    print("\nAll available eval runners completed.")

if __name__ == "__main__":
    main()
