from planner.generator import generate

CASES = [
    ("write a file named demo.py with print(\"yo\")", "write_file", "demo.py", 'print("yo")'),
    ("write a file named app.py with print(\"hello world\")", "write_file", "app.py", 'print("hello world")'),
    ("create main.py with print(\"start\")", "write_file", "main.py", 'print("start")'),
    ("read demo.py", "read_file", "demo.py", None),
    ("edit demo.py with print(\"updated\")", "edit_file", "demo.py", 'print("updated")'),
    ("update parser.py to print(\"ok\")", "edit_file", "parser.py", 'print("ok")'),
    ("read the python file called script.py", "read_file", "script.py", None),
    ("create parser.py, with print(\"parse\")", "write_file", "parser.py", 'print("parse")'),
    ("make calc.py that returns 2 + 2", "write_file", "calc.py", "returns 2 + 2"),
    ("generate helper.py containing print(\"ready\")", "write_file", "helper.py", 'print("ready")'),
    ("show hello.py?", "read_file", "hello.py", None),
    ("write a file named nested/tool.py with print(\"ok\")", "write_file", "nested/tool.py", 'print("ok")'),
    ("list workspace files", "list_workspace", "", None),
]

def run() -> tuple[int, int]:
    passed = 0

    for i, (text, action, expected_filename, expected_content) in enumerate(CASES, 1):
        result = generate(text, action)

        filename_ok = result.get("filename", "") == expected_filename
        content_ok = result.get("content") == expected_content if expected_content is not None else True

        ok = filename_ok and content_ok
        status = "PASS" if ok else "FAIL"

        print(f"{i}. {status}")
        print(" input: ", text)
        print(" output:", result)

        if ok:
            passed += 1
        else:
            print(" expected:", {
                "filename": expected_filename,
                "content": expected_content,
            })

        print()

    print(f"Passed {passed}/{len(CASES)}")
    return passed, len(CASES)


if __name__ == "__main__":
    run()
