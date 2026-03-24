from __future__ import annotations

import os

from planner.plan_builder import build_plan
from planner.schema import ActionPlan


def _model_enabled() -> bool:
    return os.getenv("AI_OPERATOR_USE_MODEL_PLANNER", "").lower() in {"1", "true", "yes"}


def _attach_mode(plan: ActionPlan, mode: str) -> ActionPlan:
    """
    Attach planner_mode without forcing a schema change yet.
    Human Review Required: promote this to ActionPlan if you want it persisted formally.
    """
    setattr(plan, "planner_mode", mode)
    return plan


def plan_request(user_input: str) -> ActionPlan:
    """
    Single planner entrypoint.

    Modes:
    - heuristic
    - model
    - model_fallback
    """
    if _model_enabled():
        try:
            from planner.model_planner import plan_with_model
            return _attach_mode(plan_with_model(user_input), "model")
        except Exception:
            # Fallback keeps the local tool usable even if API/config/model fails.
            return _attach_mode(build_plan(user_input), "model_fallback")

    return _attach_mode(build_plan(user_input), "heuristic")
