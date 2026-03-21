import os

from planner.planner_interface import plan_request
from planner.schema import ActionPlan

CASES = [
    ("write a file named demo.py with print(\"yo\")", "write_file", "heuristic"),
    ("read demo.py", "read_file", "heuristic"),
]

passed = 0

os.environ.pop("AI_OPERATOR_USE_MODEL_PLANNER", None)

for i, (text, expected_action, expected_mode) in enumerate(CASES, 1):
    result = plan_request(text)
    ok = (
        isinstance(result, ActionPlan)
        and len(result.steps) == 1
        and result.steps[0].action == expected_action
        and getattr(result, "planner_mode", None) == expected_mode
    )

    print(f"{i}. {'PASS' if ok else 'FAIL'}")
    print(" input: ", text)
    print(" output:", {
        "planner_mode": getattr(result, "planner_mode", None),
        "steps": result.to_dict(),
    })
    print()

    if ok:
        passed += 1

print(f"Passed {passed}/{len(CASES)}")
