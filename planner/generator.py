from planner.parsing import extract_edit_content, extract_filename, extract_write_content


def generate(user_input: str, action: str, filename_override: str | None = None) -> dict:
    filename = filename_override or extract_filename(user_input)

    if action == "write_file":
        return {
            "filename": filename,
            "content": extract_write_content(user_input, filename),
        }

    if action == "read_file":
        return {
            "filename": filename,
        }

    if action == "edit_file":
        return {
            "filename": filename,
            "content": extract_edit_content(user_input, filename),
        }

    if action == "list_workspace":
        return {}

    return {}
