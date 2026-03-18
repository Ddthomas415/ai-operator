from planner.classifier import classify

CASES = [
    ("write a file named demo.py with print(\"yo\")", "write_file", "demo.py", False),
    ("read demo.py", "read_file", "demo.py", False),
    ("make me a python file that prints hello", "write_file", "", True),
    ("open my file", "none", "", True),
    ("write a file named app.py with print(\"hello world\")", "write_file", "app.py", False),
    ("read app.py", "read_file", "app.py", False),
    ("create script.py that adds two numbers", "write_file", "script.py", False),
    ("read the python file called script.py", "read_file", "script.py", False),
    ("make a file for me", "write_file", "", True),
    ("show me my code", "none", "", True),
]

passed = 0

for i, (text, expected_action, expected_filename, expected_clarification) in enumerate(CASES, 1):
    result = classify(text)

    action_ok = result["action"] == expected_action
    filename_ok = result["filename"] == expected_filename
    clarification_ok = result["clarification_needed"] == expected_clarification

    ok = action_ok and filename_ok and clarification_ok
    status = "PASS" if ok else "FAIL"

    print(f"{i}. {status}")
    print(" input: ", text)
    print(" output:", result)

    if ok:
        passed += 1
    else:
        print(" expected:", {
            "action": expected_action,
            "filename": expected_filename,
            "clarification_needed": expected_clarification,
        })

    print()

print(f"Passed {passed}/{len(CASES)}")
