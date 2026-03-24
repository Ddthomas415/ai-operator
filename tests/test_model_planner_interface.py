import os

from planner.planner_interface import plan_request
from planner.schema import ActionPlan


def test_plan_request_defaults_to_heuristic():
    os.environ.pop("AI_OPERATOR_USE_MODEL_PLANNER", None)
    result = plan_request('write a file named demo.py with print("yo")')
    assert isinstance(result, ActionPlan)
    assert len(result.steps) == 1
    assert result.steps[0].action == "write_file"
    assert getattr(result, "planner_mode", None) == "heuristic"


def test_plan_request_falls_back_when_model_not_configured():
    os.environ["AI_OPERATOR_USE_MODEL_PLANNER"] = "1"
    os.environ.pop("OPENAI_API_KEY", None)
    os.environ.pop("AI_OPERATOR_MODEL", None)

    result = plan_request("read demo.py")
    assert isinstance(result, ActionPlan)
    assert len(result.steps) == 1
    assert result.steps[0].action == "read_file"
    assert getattr(result, "planner_mode", None) == "model_fallback"

    os.environ.pop("AI_OPERATOR_USE_MODEL_PLANNER", None)
