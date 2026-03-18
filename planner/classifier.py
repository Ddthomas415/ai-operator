def classify(user_input: str) -> dict:
    text = user_input.strip().lower()

    if "read" in text:
        if ".py" in text:
            parts = text.split()
            filename = next((p for p in parts if p.endswith(".py")), "")
            return {
                "action": "read_file",
                "confidence": 0.95,
                "clarification_needed": False,
                "clarification_question": None,
                "reason": "User asked to read a Python file.",
                "filename": filename,
            }
        return {
            "action": "read_file",
            "confidence": 0.60,
            "clarification_needed": True,
            "clarification_question": "Which file do you want me to read?",
            "reason": "Read intent is clear, but filename is missing.",
            "filename": "",
        }

    if "write" in text or "create" in text or "make" in text:
        if ".py" in text:
            parts = text.split()
            filename = next((p for p in parts if p.endswith(".py")), "")
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
            "clarification_question": "What should the filename be?",
            "reason": "Write intent is clear, but filename is missing.",
            "filename": "",
        }

    return {
        "action": "none",
        "confidence": 0.40,
        "clarification_needed": True,
        "clarification_question": "Can you rephrase what you want me to do?",
        "reason": "Intent is unclear.",
        "filename": "",
    }
