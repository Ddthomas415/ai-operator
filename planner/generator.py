def generate(user_input: str, action: str) -> dict:
    text = user_input.strip()

    if action == "write_file":
        parts = text.split()
        filename = next((p for p in parts if p.endswith(".py")), "")

        content = ""
        if " with " in text:
            content = text.split(" with ", 1)[1].strip()

        return {
            "filename": filename,
            "content": content,
        }

    if action == "read_file":
        parts = text.split()
        filename = next((p for p in parts if p.endswith(".py")), "")
        return {
            "filename": filename,
        }

    return {}
