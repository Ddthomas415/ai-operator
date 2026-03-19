import sys

from logger import log_event
from workflow import (
    build_payload,
    execute_action,
    first_clarification_step,
    plan_needs_clarification,
    plan_request,
    requires_overwrite_confirmation,
)


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python3 main.py "your task here"')
        raise SystemExit(1)

    user_input = " ".join(sys.argv[1:])
    plan = plan_request(user_input)

    print("PLAN:")
    print(plan.to_dict())

    if plan_needs_clarification(plan):
        step_index = first_clarification_step(plan)
        step = plan.steps[step_index] if step_index is not None else None
        print("\nCLARIFICATION NEEDED:")
        print(step.clarification_question if step is not None else "More information is required.")
        log_event(
            user_input,
            step.action if step is not None else "none",
            step.confidence if step is not None else 0.0,
            "clarification_needed",
            message=step.clarification_question if step is not None else "More information is required.",
        )
        return

    outputs: list[str] = []
    for step in plan.steps:
        if step.action == "none":
            print("\nERROR:")
            print("No supported action.")
            log_event(
                step.step_input,
                step.action,
                step.confidence,
                "unsupported",
                message=step.reason,
            )
            return

        try:
            payload = build_payload(step.step_input, step.action)
            print("\nGENERATOR:")
            print({"step_input": step.step_input, "payload": payload})
            if requires_overwrite_confirmation(step.action, payload):
                message = f"{payload['filename']} already exists. Refusing to overwrite in one-shot mode."
                print("\nERROR:")
                print(message)
                log_event(
                    step.step_input,
                    step.action,
                    step.confidence,
                    "error",
                    error_type="FileExistsError",
                    message=message,
                )
                return
            output = execute_action(step.action, payload)
            outputs.append(output)
            log_event(
                step.step_input,
                step.action,
                step.confidence,
                "ok",
                message=output,
            )
        except (ValueError, FileExistsError, FileNotFoundError) as e:
            print(f"\nERROR: {e}")
            log_event(
                step.step_input,
                step.action,
                step.confidence,
                "error",
                error_type=type(e).__name__,
                message=str(e),
            )
            return

    print("\nOUTPUT:")
    for output in outputs:
        print(output)


if __name__ == "__main__":
    main()
