from evals.run_clarification_eval import run as run_clarification
from evals.run_eval import run as run_classifier
from evals.run_full_eval import run as run_full
from evals.run_generator_eval import run as run_generator
from evals.run_plan_eval import run as run_plan
from evals.run_session_eval import run as run_session


def _report(name: str, passed: int, total: int) -> bool:
    print(f"{name}: {passed}/{total}")
    return passed == total


def main() -> None:
    results = [
        ("classifier", *run_classifier()),
        ("generator", *run_generator()),
        ("full", *run_full()),
        ("clarification", *run_clarification()),
        ("plan", *run_plan()),
        ("session", *run_session()),
    ]
    ok = all(_report(name, passed, total) for name, passed, total in results)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
