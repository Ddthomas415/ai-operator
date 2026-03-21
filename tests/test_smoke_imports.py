def test_import_classifier():
    from planner.classifier import classify
    result = classify("read demo.py")
    assert isinstance(result, dict)
    assert "action" in result

def test_import_generator():
    from planner.generator import generate
    result = generate('write a file named demo.py with print("yo")', "write_file")
    assert isinstance(result, dict)
