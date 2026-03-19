from typing import Any

from config import CONFIDENCE_THRESHOLD, SUPPORTED_ACTIONS
from executor.actions import edit_file, file_exists, list_workspace, read_file, validate_filename, write_file
from planner.classifier import classify
from planner.generator import generate
from planner.plan_builder import build_plan
from planner.schema import ActionPlan


def should_request_clarification(result: dict[str, Any]) -> bool:
    if result.get("clarification_needed"):
        return True
    if result.get("action") in SUPPORTED_ACTIONS and result.get("confidence", 0.0) < CONFIDENCE_THRESHOLD:
        return True
    return False


def validate_clarification_answer(answer: str) -> str:
    cleaned = answer.strip()
    validate_filename(cleaned)
    return cleaned


def build_payload(user_input: str, action: str, filename_override: str | None = None) -> dict[str, Any]:
    if filename_override is not None:
        validate_filename(filename_override)
    payload = generate(user_input, action, filename_override=filename_override)
    if action == "edit_file" and not payload.get("content", "").strip():
        raise ValueError("Edit content cannot be empty.")
    return payload


def requires_overwrite_confirmation(action: str, payload: dict[str, Any]) -> bool:
    return action == "write_file" and file_exists(payload["filename"])


def execute_action(action: str, payload: dict[str, Any], *, allow_overwrite: bool = False) -> str:
    if action == "read_file":
        return read_file(payload["filename"])
    if action == "write_file":
        return write_file(payload["filename"], payload["content"], allow_overwrite=allow_overwrite)
    if action == "edit_file":
        return edit_file(payload["filename"], payload["content"])
    if action == "list_workspace":
        return list_workspace()
    raise ValueError(f"Unsupported action: {action}")


def classify_follow_up(user_input: str) -> dict[str, Any]:
    return classify(user_input)


def plan_request(user_input: str) -> ActionPlan:
    return build_plan(user_input)


def plan_needs_clarification(plan: ActionPlan) -> bool:
    return any(should_request_clarification(step.to_dict()) for step in plan.steps)


def first_clarification_step(plan: ActionPlan) -> int | None:
    for index, step in enumerate(plan.steps):
        if should_request_clarification(step.to_dict()):
            return index
    return None
