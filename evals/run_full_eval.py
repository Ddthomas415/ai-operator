from planner.classifier import classify
from planner.generator import generate

CASES = [
    ("write a file named demo.py with print(\"yo\")", "write_file", "demo.py", False, 'print("yo")'),
    ("read demo.py", "read_file", "demo.py", False, None),
    ("make me a python file that prints hello", "write_file", "", True, None),
    ("open my file", "none", "", True, None),
    ("write a file named app.py with print(\"hello world\")", "write_file", "app.py", False, 'print("hello world")'),
    ("read app.py", "read_file", "app.py", False, None),
]

passed = 0

for i, (text, expected_action, expected_filename, expected_clarification, expected_content) in enumerate(CASES, 1):
    c = classify(text)

    action_ok = c["action"] == expected_action
    clarification_ok = c["clarification_needed"] == expected_clarification
    filename_ok = c["filename"] == expected_filename

    content_ok = True
    if not c["clarification_needed"] and c["action"] in {"write_file", "read_file"}:
        g = generate(text, c["action"])
        filename_ok = g.get("filename", "") == expected_filename
        if expected_content is not None:
            content_ok = g.get("content") == expected_content

    ok = action_ok and clarification_ok and filename_ok and content_ok
    print(f"{i}. {'PASS' if ok else 'FAIL'}")

    if ok:
        passed += 1
    else:
        print(" input:   ", text)
        print(" expected:", expected_action, expected_filename, expected_clarification, expected_content)
        print(" got:     ", c)
        if not c["clarification_needed"] and c["action"] in {"write_file", "read_file"}:
            print(" payload: ", generate(text, c["action"]))
        print()

print(f"Passed {passed}/{len(CASES)}")
