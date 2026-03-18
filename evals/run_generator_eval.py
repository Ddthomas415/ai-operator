from planner.generator import generate

CASES = [
    ("write a file named demo.py with print(\"yo\")", "write_file", "demo.py", 'print("yo")'),
    ("write a file named app.py with print(\"hello world\")", "write_file", "app.py", 'print("hello world")'),
    ("create main.py with print(\"start\")", "write_file", "main.py", 'print("start")'),
    ("read demo.py", "read_file", "demo.py", None),
    ("read the python file called script.py", "read_file", "script.py", None),
]

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
