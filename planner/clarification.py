from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from planner.parsing import extract_filename

ClarificationField = Literal["filename", "content"]


@dataclass
class ClarificationRequest:
    field: ClarificationField
    question: str


def _has_content_phrase(user_input: str) -> bool:
    text = user_input.lower()
    markers = [
        " with ",
        " containing ",
        " content ",
        " to ",
        " update ",
        " edit ",
    ]
    return any(marker in text for marker in markers)


def needs_filename(user_input: str, action: str) -> bool:
    if action not in {"write_file", "read_file", "edit_file"}:
        return False
    return extract_filename(user_input) == ""


def needs_content(user_input: str, action: str) -> bool:
    if action not in {"write_file", "edit_file"}:
        return False
    return not _has_content_phrase(user_input)


def next_clarification(user_input: str, action: str) -> Optional[ClarificationRequest]:
    if needs_filename(user_input, action):
        return ClarificationRequest(
            field="filename",
            question="What should the filename be? Use a workspace-relative .py path.",
        )

    if needs_content(user_input, action):
        return ClarificationRequest(
            field="content",
            question="What content should I write?",
        )

    return None


def validate_answer(field: ClarificationField, answer: str) -> bool:
    answer = answer.strip()
    if not answer:
        return False

    if field == "filename":
        if answer.startswith("/") or answer.startswith("./") or ".." in answer:
            return False
        return answer.endswith(".py")

    return True


def apply_answer(
    overrides: dict[str, str],
    field: ClarificationField,
    answer: str,
) -> dict[str, str]:
    updated = dict(overrides)
    updated[field] = answer.strip()
    return updated
