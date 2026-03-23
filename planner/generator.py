from __future__ import annotations

import re
from typing import Any


def extract_filename(text: str) -> str:
    """
    Extract the first workspace-relative .py filename.
    Handles trailing punctuation like '?', ',', '.', ':'.
    """
    matches = re.findall(r'([A-Za-z0-9_\-/]+\.py)\b', text)
    return matches[0] if matches else ""


def _extract_content(text: str, action: str) -> str:
    """
    Extract content for write/edit style prompts.

    Supported phrases:
    - with ...
    - containing ...
    - to ...
    - that ...
    - returns ...
    """
    if action not in {"write_file", "edit_file"}:
        return ""

    patterns = [
        r"\bwith\s+(.+)$",
        r"\bcontaining\s+(.+)$",
        r"\bto\s+(.+)$",
        r"\bthat\s+(.+)$",
        r"\breturns\s+(.+)$",
    ]

    for pattern in patterns:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            content = m.group(1).strip()
            # Normalize bare "returns X" into code-like content if desired later.
            return content

    return ""


def generate(
    user_input: str,
    action: str,
    filename_override: str | None = None,
    content_override: str | None = None,
) -> dict[str, Any]:
    text = user_input.strip()

    if action == "write_file":
        filename = filename_override or extract_filename(text)
        content = content_override or _extract_content(text, action)
        return {
            "filename": filename,
            "content": content,
        }

    if action == "edit_file":
        filename = filename_override or extract_filename(text)
        content = content_override or _extract_content(text, action)
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
