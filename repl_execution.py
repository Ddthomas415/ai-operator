from __future__ import annotations

from logger import log_event
from session_store import append_session_event
from workflow import build_payload, execute_action, requires_overwrite_confirmation


def execute_plan_steps(
    *,
    plan,
    session_id: str,
    filename_override: str | None,
    confirm_overwrite,
) -> list[str]:
    """
    Execute all plan steps, handling payload generation, overwrite confirmation,
    action execution, logging, and session event recording.

    Returns:
        list[str]: Collected action outputs in execution order.

    Raises:
        ValueError, FileExistsError, FileNotFoundError:
            Propagated from payload validation or action execution.
    """
    outputs: list[str] = []

    for index, step in enumerate(plan.steps):
        override = filename_override if index == 0 else None
        payload = build_payload(step.step_input, step.action, filename_override=override)

        print("\nGENERATOR:")
        print({"step_input": step.step_input, "payload": payload})

        allow_overwrite = False
        if requires_overwrite_confirmation(step.action, payload):
            if not confirm_overwrite(payload["filename"]):
                raise FileExistsError("Overwrite canceled by user.")
            allow_overwrite = True

        output = execute_action(step.action, payload, allow_overwrite=allow_overwrite)
        outputs.append(output)

        log_event(
            step.step_input,
            step.action,
            step.confidence,
            "ok",
            message=output,
        )
        append_session_event(session_id, "output", {"message": output})

    return outputs


def report_outputs(outputs: list[str]) -> None:
    """Print final execution outputs to the REPL."""
    print("\nOUTPUT:")
    for output in outputs:
        print(output)
