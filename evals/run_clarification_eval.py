from executor.actions import validate_filename
from planner.classifier import classify
from workflow import build_payload

FILENAME_CASES = [
    ("write a python file", "write_file", "demo.py", "demo.py"),
    ("read the file", "read_file", "demo.py", "demo.py"),
    ("make a file for me", "write_file", "nested/tool.py", "nested/tool.py"),
]

INVALID_FILENAME_CASES = [
    ("write a python file", "../evil.py", "Invalid path."),
    ("read the file", "", "Filename cannot be empty."),
    ("write a python file", "scripts/", "Filename must point to a Python file, not a directory."),
    ("read the file", "notes.txt", "Only .py files are supported."),
]

INVALID_EDIT_CASES = [
    ("edit the file", "demo.py", "Edit content cannot be empty."),
]

UNSUPPORTED_CASES = [
    ("open my file", "Can you rephrase that as a request to read, create, edit, or list Python files?"),
    ("launch the app", "Can you rephrase that as a request to read, create, edit, or list Python files?"),
]


def run() -> tuple[int, int]:
    passed = 0
    total = len(FILENAME_CASES) + len(INVALID_FILENAME_CASES) + len(INVALID_EDIT_CASES) + len(UNSUPPORTED_CASES)

    for i, (text, expected_action, answer, expected_filename) in enumerate(FILENAME_CASES, 1):
        result = classify(text)
        payload = build_payload(text, expected_action, filename_override=answer)
        ok = result["clarification_needed"] and payload["filename"] == expected_filename
        print(f"{i}. {'PASS' if ok else 'FAIL'}")
        if not ok:
            print(" input:   ", text)
            print(" answer:  ", answer)
            print(" result:  ", result)
            print(" payload: ", payload)
        else:
            passed += 1

    offset = len(FILENAME_CASES)
    for index, (text, answer, expected_error) in enumerate(INVALID_FILENAME_CASES, 1):
        ok = False
        try:
            classify(text)
            validate_filename(answer)
        except ValueError as error:
            ok = str(error) == expected_error

        print(f"{offset + index}. {'PASS' if ok else 'FAIL'}")
        if not ok:
            print(" input:   ", text)
            print(" answer:  ", answer)
            print(" expected:", expected_error)
        else:
            passed += 1

    offset += len(INVALID_FILENAME_CASES)
    for index, (text, answer, expected_error) in enumerate(INVALID_EDIT_CASES, 1):
        ok = False
        try:
            build_payload(text, "edit_file", filename_override=answer)
        except ValueError as error:
            ok = str(error) == expected_error

        print(f"{offset + index}. {'PASS' if ok else 'FAIL'}")
        if not ok:
            print(" input:   ", text)
            print(" answer:  ", answer)
            print(" expected:", expected_error)
        else:
            passed += 1

    offset += len(INVALID_EDIT_CASES)
    for index, (text, expected_question) in enumerate(UNSUPPORTED_CASES, 1):
        result = classify(text)
        ok = result["action"] == "none" and result["clarification_question"] == expected_question
        print(f"{offset + index}. {'PASS' if ok else 'FAIL'}")
        if not ok:
            print(" input:   ", text)
            print(" result:  ", result)
        else:
            passed += 1

    print(f"Passed {passed}/{total}")
    return passed, total


if __name__ == "__main__":
    run()
