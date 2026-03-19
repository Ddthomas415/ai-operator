from workflow import plan_needs_clarification, plan_request

CASES = [
    (
        'write a file named plan_a.py with print("a") and then read plan_a.py',
        ["write_file", "read_file"],
        False,
    ),
    (
        "list workspace files and then read demo.py",
        ["list_workspace", "read_file"],
        False,
    ),
    (
        "write a python file and then read demo.py",
        ["write_file", "read_file"],
        True,
    ),
    (
        'edit demo.py with print("updated") and then read demo.py',
        ["edit_file", "read_file"],
        False,
    ),
]


def run() -> tuple[int, int]:
    passed = 0
    for i, (text, expected_actions, expected_clarification) in enumerate(CASES, 1):
        plan = plan_request(text)
        actions_ok = [step.action for step in plan.steps] == expected_actions
        clarification_ok = plan_needs_clarification(plan) == expected_clarification
        ok = actions_ok and clarification_ok
        print(f"{i}. {'PASS' if ok else 'FAIL'}")
        if not ok:
            print(" input:   ", text)
            print(" expected:", expected_actions, expected_clarification)
            print(" got:     ", plan.to_dict())
        else:
            passed += 1
    print(f"Passed {passed}/{len(CASES)}")
    return passed, len(CASES)


if __name__ == "__main__":
    run()
