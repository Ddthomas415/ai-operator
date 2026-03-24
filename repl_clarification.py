from __future__ import annotations

from planner.classifier import classify_follow_up
from planner.plan_builder import first_clarification_step, plan_needs_clarification
from planner.validation import validate_clarification_answer
from workflow import plan_request

EXIT_WORDS = {"quit", "exit"}


def resolve_clarification(user_input: str, plan, prompt_func, append_session_event, session_id):
    """
    Resolve one clarification cycle.

    Returns:
    - (updated_user_input, updated_plan, filename_override)
    - raises SystemExit(0) if user exits cleanly
    - returns (user_input, plan, None) if no clarification is needed
    """
    if not plan_needs_clarification(plan):
        return user_input, plan, None

    step_index = first_clarification_step(plan)
    step = plan.steps[step_index] if step_index is not None else None

    print("\nCLARIFICATION NEEDED:")
    print(step.clarification_question if step is not None else "More information is required.")
    append_session_event(
        session_id,
        "clarification_question",
        {"question": step.clarification_question if step is not None else "More information is required."},
    )

    answer = prompt_func("> ")
    if answer is None:
        print("Goodbye.")
        raise SystemExit(0)

    append_session_event(session_id, "clarification_answer", {"answer": answer})

    if not answer:
        raise ValueError("Clarification answer cannot be empty.")

    if step is not None and step.action in {"write_file", "read_file", "edit_file"}:
        filename_override = validate_clarification_answer(answer)
        return user_input, plan, filename_override

    result = classify_follow_up(answer)
    print("\nCLASSIFIER:")
    print(result)

    if result["clarification_needed"]:
        raise RuntimeError(result["reason"])

    updated_user_input = answer
    updated_plan = plan_request(answer)
    append_session_event(
        session_id,
        "plan",
        {"step_count": len(updated_plan.steps), "plan": updated_plan.to_dict()},
    )
    return updated_user_input, updated_plan, None
