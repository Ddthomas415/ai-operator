from __future__ import annotations

def extract_filename(text: str) -> str:
    parts = text.replace(",", " ").split()
    return next((p for p in parts if p.endswith(".py")), "")

def generate(
    user_input: str,
    action: str,
    filename_override: str | None = None,
    content_override: str | None = None,
) -> dict:
    text = user_input.strip()

    if action == "write_file":
        filename = filename_override or extract_filename(text)
        content = content_override or ""
        if not content and " with " in text:
            content = text.split(" with ", 1)[1].strip()
        return {
            "filename": filename,
            "content": content,
        }

    if action == "edit_file":
        filename = filename_override or extract_filename(text)
        content = content_override or ""
        if not content and " with " in text:
            content = text.split(" with ", 1)[1].strip()
        elif not content and " to " in text:
            content = text.split(" to ", 1)[1].strip()
        return {
            "filename": filename,
            "content": content,
        }

    if action == "read_file":
        filename = filename_override or extract_filename(text)
        return {
            "filename": filename,
        }

    if action == "list_workspace":
        return {}

    return {}
