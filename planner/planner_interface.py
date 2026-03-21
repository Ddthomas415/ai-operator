from __future__ import annotations

import os

from planner.plan_builder import build_plan
from planner.schema import ActionPlan


def _model_enabled() -> bool:
    return os.getenv("AI_OPERATOR_USE_MODEL_PLANNER", "").lower() in {"1", "true", "yes"}


def plan_request(user_input: str) -> ActionPlan:
    """
    Single planner entrypoint.

    Behavior:
    - default: heuristic planner
    - feature flag on: try model planner
    - on model failure: fall back to heuristic planner
    """
    if _model_enabled():
        try:
            from planner.model_planner import plan_with_model

            return plan_with_model(user_input)
        except Exception:
            # Human Review Required: this currently swallows model-path errors
            # and falls back to heuristic behavior for safety/stability.
            return build_plan(user_input)

    return build_plan(user_input)
