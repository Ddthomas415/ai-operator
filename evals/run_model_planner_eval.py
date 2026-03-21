import os

from planner.planner_interface import plan_request
from planner.schema import ActionPlan

CASES = [
    ("write a file named demo.py with print(\"yo\")", "write_file"),
    ("read demo.py", "read_file"),
]

passed = 0

# Default path: heuristic mode
os.environ.pop("AI_OPERATOR_USE_MODEL_PLANNER", None)

for i, (text, expected_action) in enumerate(CASES, 1):
    result = plan_request(text)
    ok = (
        isinstance(result, ActionPlan)
        and len(result.steps) == 1
        and result.steps[0].action == expected_action
    )

    print(f"{i}. {'PASS' if ok else 'FAIL'}")
    print(" input: ", text)
    print(" output:", result.to_dict())
    print()

    if ok:
        passed += 1

print(f"Passed {passed}/{len(CASES)}")
