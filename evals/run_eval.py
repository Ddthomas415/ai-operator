from planner.classifier import classify

CASES = [
    ("write a file named demo.py with print(\"yo\")", "write_file", "demo.py", False),
    ("read demo.py", "read_file", "demo.py", False),
    ("edit demo.py with print(\"updated\")", "edit_file", "demo.py", False),
    ("update parser.py to print(\"ok\")", "edit_file", "parser.py", False),
    ("list workspace files", "list_workspace", "", False),
    ("make me a python file that prints hello", "write_file", "", True),
    ("open my file", "none", "", True),
    ("write a file named app.py with print(\"hello world\")", "write_file", "app.py", False),
    ("read app.py", "read_file", "app.py", False),
    ("create script.py that adds two numbers", "write_file", "script.py", False),
    ("read the python file called script.py", "read_file", "script.py", False),
    ("make a file for me", "write_file", "", True),
    ("show me my code", "none", "", True),
    ("display parser.py", "read_file", "parser.py", False),
    ("show me the file contents", "read_file", "", True),
    ("print util.py", "read_file", "util.py", False),
    ("generate helper.py with print(\"ready\")", "write_file", "helper.py", False),
    ("create parser.py, with print(\"parse\")", "write_file", "parser.py", False),
    ("make calc.py that returns 2 + 2", "write_file", "calc.py", False),
    ("write a python file", "write_file", "", True),
    ("read the file", "read_file", "", True),
    ("show hello.py?", "read_file", "hello.py", False),
    ("generate code for me", "write_file", "", True),
]

def run() -> tuple[int, int]:
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
    return passed, len(CASES)


if __name__ == "__main__":
    run()
