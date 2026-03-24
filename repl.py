import sys

from logger import log_event
from repl_clarification import resolve_clarification
from repl_execution import execute_plan_steps, report_outputs
from repl_session import load_previous_events, resolve_session_from_args
from repl_ui import handle_builtin_command, show_session_banner
from session_store import (
    append_session_event,
    format_transcript,
    latest_session_id,
    load_session_events,
    session_prompt_history,
    start_session,
)
from workflow import (
    classify_follow_up,
    first_clarification_step,
    plan_needs_clarification,
    plan_request,
    validate_clarification_answer,
)

EXIT_WORDS = {"quit", "exit"}


def _prompt(prompt: str) -> str | None:
    answer = input(prompt).strip()
    if answer.lower() in EXIT_WORDS:
        return None
    return answer


def _confirm_overwrite(filename: str) -> bool:
    answer = _prompt(f"Overwrite {filename}? [y/N] ")
    return answer is not None and answer.lower() in {"y", "yes"}


def run_once(user_input: str, session_id: str) -> None:
    append_session_event(session_id, "user_input", {"input": user_input})
    plan = plan_request(user_input)
    filename_override = None

    print("\nPLAN:")
    print(plan.to_dict())
    append_session_event(session_id, "plan", {"step_count": len(plan.steps), "plan": plan.to_dict()})

    try:
        user_input, plan, filename_override = resolve_clarification(
            user_input=user_input,
            plan=plan,
            prompt_func=_prompt,
            append_session_event=append_session_event,
            session_id=session_id,
        )
    except ValueError as e:
        print(f"\nERROR: {e}")
        step_index = first_clarification_step(plan)
        step = plan.steps[step_index] if step_index is not None else None
        log_event(
            user_input,
            step.action if step is not None else "none",
            step.confidence if step is not None else 0.0,
            "error",
            error_type=type(e).__name__,
            message=str(e),
        )
        append_session_event(session_id, "error", {"message": str(e)})
        return
    except RuntimeError as e:
        print("\nERROR: Unsupported request after clarification.")
        result = classify_follow_up(str(e))
        log_event(
            user_input,
            result.get("action", "none"),
            result.get("confidence", 0.0),
            "unsupported",
            message=str(e),
        )
        append_session_event(session_id, "error", {"message": str(e)})
        return

    for step in plan.steps:
        if step.action == "none":
            print("\nERROR: No supported action.")
            log_event(
                step.step_input,
                step.action,
                step.confidence,
                "unsupported",
                message=step.reason,
            )
            append_session_event(session_id, "error", {"message": step.reason})
            return

    try:
        outputs = execute_plan_steps(
            plan=plan,
            session_id=session_id,
            filename_override=filename_override,
            confirm_overwrite=_confirm_overwrite,
        )
    except (ValueError, FileExistsError, FileNotFoundError) as e:
        print(f"\nERROR: {e}")
        step = plan.steps[0] if plan.steps else None
        log_event(
            step.step_input if step is not None else user_input,
            step.action if step is not None else "none",
            step.confidence if step is not None else 0.0,
            "error",
            error_type=type(e).__name__,
            message=str(e),
        )
        append_session_event(session_id, "error", {"message": str(e)})
        return

    report_outputs(outputs)


def _resolve_session_from_args(argv: list[str]) -> str:
    """Resolve the session id from CLI arguments.

    Supported forms:
    - no args: start a new session
    - --resume <session_id>: resume that exact session
    - --resume-last: resume the most recent session
    """
    if len(argv) >= 3 and argv[1] == "--resume":
        return start_session(argv[2])
    if len(argv) >= 2 and argv[1] == "--resume-last":
        session_id = latest_session_id()
        if session_id is None:
            raise SystemExit("No previous session found.")
        return start_session(session_id)
    return start_session()


def main() -> None:
    """Run the interactive REPL loop for the local operator."""
    session_id = _resolve_session_from_args(sys.argv)
    previous_events = load_session_events(session_id)

    show_session_banner(session_id, len(previous_events))

    while True:
        try:
            user_input = input("task> ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break
        if user_input.lower() in EXIT_WORDS:
            print("Goodbye.")
            break
        if not user_input:
            continue
        if handle_builtin_command(user_input, session_id):
            continue
        try:
            run_once(user_input, session_id)
        except KeyboardInterrupt:
            print("\nERROR: Interrupted.")
            append_session_event(session_id, "error", {"message": "Interrupted."})
        except EOFError:
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()
