from planner.clarification import next_clarification, validate_answer, apply_answer
from planner.generator import generate


def test_missing_filename_for_write():
    req = next_clarification("make me a python file that prints hello", "write_file")
    assert req is not None
    assert req.field == "filename"


def test_missing_content_for_write():
    req = next_clarification("write a file named demo.py", "write_file")
    assert req is not None
    assert req.field == "content"


def test_filename_validation():
    assert validate_answer("filename", "demo.py") is True
    assert validate_answer("filename", "../evil.py") is False
    assert validate_answer("filename", "./demo.py") is False
    assert validate_answer("filename", "demo.txt") is False


def test_apply_answer():
    overrides = {}
    overrides = apply_answer(overrides, "filename", "demo.py")
    overrides = apply_answer(overrides, "content", 'print("hi")')
    assert overrides == {"filename": "demo.py", "content": 'print("hi")'}


def test_generate_uses_content_override():
    result = generate(
        "write a file named demo.py",
        "write_file",
        filename_override="demo.py",
        content_override='print("hi")',
    )
    assert result["filename"] == "demo.py"
    assert result["content"] == 'print("hi")'


def test_edit_generate_supports_to_phrase():
    result = generate("update parser.py to print('ok')", "edit_file")
    assert result["filename"] == "parser.py"
    assert "print('ok')" in result["content"]
