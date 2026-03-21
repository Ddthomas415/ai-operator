from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

from planner.parsing import split_into_steps
from planner.schema import ActionPlan, ActionStep

SYSTEM_PROMPT = """You are the planning layer for a local Python file operator.

Return JSON only.
Rules:
- Allowed actions: write_file, read_file, edit_file, list_workspace, none
- Filenames must be workspace-relative Python paths like demo.py or nested/tool.py
- Never use absolute paths
- Never use ../ or ./ prefixes
- If the request is ambiguous, set clarification_needed=true
- For list_workspace, filename="" and content=""
- For read_file, content=""
- For none, filename="" and content=""
- Keep confidence between 0.0 and 1.0
"""

STEP_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["write_file", "read_file", "edit_file", "list_workspace", "none"],
        },
        "confidence": {"type": "number"},
        "clarification_needed": {"type": "boolean"},
        "clarification_question": {"type": ["string", "null"]},
        "reason": {"type": "string"},
        "filename": {"type": "string"},
        "content": {"type": "string"},
    },
    "required": [
        "action",
        "confidence",
        "clarification_needed",
        "clarification_question",
        "reason",
        "filename",
        "content",
    ],
    "additionalProperties": False,
}


def _model_enabled() -> bool:
    return os.getenv("AI_OPERATOR_USE_MODEL_PLANNER", "").lower() in {"1", "true", "yes"}


def _configured() -> bool:
    return bool(os.getenv("OPENAI_API_KEY")) and bool(os.getenv("AI_OPERATOR_MODEL"))


def _step_to_payload(action: str, filename: str, content: str) -> dict[str, Any]:
    if action in {"write_file", "edit_file"}:
        return {"filename": filename, "content": content}
    if action == "read_file":
        return {"filename": filename}
    if action == "list_workspace":
        return {}
    return {}


def plan_with_model(user_input: str) -> ActionPlan:
    """
    Real model-backed planner.

    Assumptions:
    - OPENAI_API_KEY and AI_OPERATOR_MODEL are set.
    - Caller decides whether to fall back on failure.
    """
    if not _model_enabled():
        raise RuntimeError("Model planner is disabled.")
    if not _configured():
        raise RuntimeError("Model planner is not configured. Set OPENAI_API_KEY and AI_OPERATOR_MODEL.")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.environ["AI_OPERATOR_MODEL"]

    steps: list[ActionStep] = []

    for step_input in split_into_steps(user_input):
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": step_input},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "planner_step",
                    "schema": STEP_SCHEMA,
                }
            },
        )

        data = json.loads(response.output_text)

        action = data["action"]
        filename = (data.get("filename") or "").strip()
        content = data.get("content") or ""

        steps.append(
            ActionStep(
                step_input=step_input,
                action=action,
                confidence=float(data["confidence"]),
                clarification_needed=bool(data["clarification_needed"]),
                clarification_question=data.get("clarification_question"),
                reason=data["reason"],
                filename=filename,
                payload=_step_to_payload(action, filename, content),
            )
        )

    plan = ActionPlan(original_input=user_input, steps=steps)
    # Inline annotation so downstream code/tests can inspect which planner path ran.
    setattr(plan, "planner_mode", "model")
    return plan
