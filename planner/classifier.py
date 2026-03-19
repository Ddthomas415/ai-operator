from planner.parsing import extract_filename

READ_KEYWORDS = ("read", "show", "display", "print")
WRITE_KEYWORDS = ("write", "create", "make", "generate")
EDIT_KEYWORDS = ("edit", "update", "modify", "change", "rewrite", "replace")
LIST_KEYWORDS = ("list", "show files", "show the files", "what files", "workspace files")


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def classify(user_input: str) -> dict:
    text = user_input.strip().lower()
    filename = extract_filename(user_input)

    if (_contains_any(text, LIST_KEYWORDS) or ("workspace" in text and "files" in text)) and "read" not in text:
        return {
            "action": "list_workspace",
            "confidence": 0.90,
            "clarification_needed": False,
            "clarification_question": None,
            "reason": "User asked to list workspace files.",
            "filename": "",
        }

    if _contains_any(text, EDIT_KEYWORDS):
        if filename:
            return {
                "action": "edit_file",
                "confidence": 0.95,
                "clarification_needed": False,
                "clarification_question": None,
                "reason": "User asked to edit a Python file.",
                "filename": filename,
            }
        return {
            "action": "edit_file",
            "confidence": 0.60,
            "clarification_needed": True,
            "clarification_question": "Which Python file do you want me to edit?",
            "reason": "Edit intent is clear, but filename is missing.",
            "filename": "",
        }

    if _contains_any(text, WRITE_KEYWORDS):
        if filename:
            return {
                "action": "write_file",
                "confidence": 0.95,
                "clarification_needed": False,
                "clarification_question": None,
                "reason": "User asked to create a Python file.",
                "filename": filename,
            }
        return {
            "action": "write_file",
            "confidence": 0.60,
            "clarification_needed": True,
            "clarification_question": "What should the Python filename be?",
            "reason": "Write intent is clear, but filename is missing.",
            "filename": "",
        }

    if _contains_any(text, READ_KEYWORDS):
        if filename:
            return {
                "action": "read_file",
                "confidence": 0.95,
                "clarification_needed": False,
                "clarification_question": None,
                "reason": "User asked to read a Python file.",
                "filename": filename,
            }
        if "file" in text or "contents" in text:
            return {
                "action": "read_file",
                "confidence": 0.60,
                "clarification_needed": True,
                "clarification_question": "Which Python file do you want me to read?",
                "reason": "Read intent is clear, but filename is missing.",
                "filename": "",
            }

    return {
        "action": "none",
        "confidence": 0.40,
        "clarification_needed": True,
        "clarification_question": "Can you rephrase that as a request to read, create, edit, or list Python files?",
        "reason": "Intent is unclear.",
        "filename": "",
    }
