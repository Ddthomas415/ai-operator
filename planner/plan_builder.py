import re

from planner.classifier import classify
from planner.generator import generate
from planner.schema import ActionPlan, ActionStep

PLAN_SPLIT_PATTERN = re.compile(r"\s+(?:and then|then)\s+", re.IGNORECASE)


def split_into_steps(user_input: str) -> list[str]:
    parts = [part.strip() for part in PLAN_SPLIT_PATTERN.split(user_input.strip()) if part.strip()]
    return parts or [user_input.strip()]


def build_plan(user_input: str) -> ActionPlan:
    steps: list[ActionStep] = []
    for step_input in split_into_steps(user_input):
        result = classify(step_input)
        payload: dict[str, object] = {}
        if not result["clarification_needed"] and result["action"] != "none":
            payload = generate(step_input, result["action"])
        steps.append(
            ActionStep(
                step_input=step_input,
                action=result["action"],
                confidence=result["confidence"],
                clarification_needed=result["clarification_needed"],
                clarification_question=result["clarification_question"],
                reason=result["reason"],
                filename=result.get("filename", ""),
                payload=payload,
            )
        )
    return ActionPlan(original_input=user_input, steps=steps)
