import sys

from logger import log_event
from session_store import (
    append_session_event,
    format_transcript,
    latest_session_id,
    load_session_events,
    session_prompt_history,
    start_session,
)
from workflow import (
    build_payload,
    classify_follow_up,
    execute_action,
    first_clarification_step,
    plan_needs_clarification,
    plan_request,
    requires_overwrite_confirmation,
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

    if plan_needs_clarification(plan):
        step_index = first_clarification_step(plan)
        step = plan.steps[step_index] if step_index is not None else None
        print("\nCLARIFICATION NEEDED:")
        print(step.clarification_question if step is not None else "More information is required.")
        append_session_event(
            session_id,
            "clarification_question",
            {"question": step.clarification_question if step is not None else "More information is required."},
        )
        answer = _prompt("> ")
        if answer is None:
            print("Goodbye.")
            raise SystemExit(0)
        append_session_event(session_id, "clarification_answer", {"answer": answer})
        if not answer:
            print("\nERROR: Clarification answer cannot be empty.")
            log_event(
                user_input,
                step.action if step is not None else "none",
                step.confidence if step is not None else 0.0,
                "error",
                error_type="ValidationError",
                message="Clarification answer cannot be empty.",
            )
            append_session_event(
                session_id,
                "error",
                {"message": "Clarification answer cannot be empty."},
            )
            return

        if step is not None and step.action in {"write_file", "read_file", "edit_file"}:
            try:
                filename_override = validate_clarification_answer(answer)
            except ValueError as e:
                print(f"\nERROR: {e}")
                log_event(
                    user_input,
                    step.action,
                    step.confidence,
                    "error",
                    error_type=type(e).__name__,
                    message=str(e),
                )
                append_session_event(session_id, "error", {"message": str(e)})
                return
        else:
            result = classify_follow_up(answer)
            print("\nCLASSIFIER:")
            print(result)
            if result["clarification_needed"]:
                print("\nERROR: Unsupported request after clarification.")
                log_event(
                    user_input,
                    result["action"],
                    result["confidence"],
                    "unsupported",
                    message=result["reason"],
                )
                append_session_event(session_id, "error", {"message": result["reason"]})
                return
            user_input = answer
            plan = plan_request(answer)
            append_session_event(session_id, "plan", {"step_count": len(plan.steps), "plan": plan.to_dict()})

    outputs: list[str] = []
    for index, step in enumerate(plan.steps):
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
            override = filename_override if index == 0 else None
            payload = build_payload(step.step_input, step.action, filename_override=override)
            print("\nGENERATOR:")
            print({"step_input": step.step_input, "payload": payload})

            allow_overwrite = False
            if requires_overwrite_confirmation(step.action, payload):
                if not _confirm_overwrite(payload["filename"]):
                    print("\nERROR: Overwrite canceled.")
                    log_event(
                        step.step_input,
                        step.action,
                        step.confidence,
                        "error",
                        error_type="FileExistsError",
                        message="Overwrite canceled by user.",
                    )
                    append_session_event(session_id, "error", {"message": "Overwrite canceled by user."})
                    return
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
            append_session_event(session_id, "error", {"message": str(e)})
            return

    print("\nOUTPUT:")
    for output in outputs:
        print(output)


def _resolve_session_from_args(argv: list[str]) -> str:
    if len(argv) >= 3 and argv[1] == "--resume":
        return start_session(argv[2])
    if len(argv) >= 2 and argv[1] == "--resume-last":
        session_id = latest_session_id()
        if session_id is None:
            raise SystemExit("No previous session found.")
        return start_session(session_id)
    return start_session()


def main() -> None:
    session_id = _resolve_session_from_args(sys.argv)
    previous_events = load_session_events(session_id)

    print("AI Operator REPL")
    print("Type 'quit' to exit.")
    print("Type 'history' to show this session's prompts.\n")
    print(f"Session: {session_id}")
    if len(previous_events) > 1:
        print(f"Resumed with {len(session_prompt_history(session_id))} prior prompt(s).")
    print("Type 'transcript' to show the saved session transcript.\n")

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
        if user_input.lower() == "history":
            print("\nHISTORY:")
            history = session_prompt_history(session_id)
            if history:
                for index, entry in enumerate(history, 1):
                    print(f"{index}. {entry}")
            else:
                print("No prompts yet.")
            continue
        if user_input.lower() == "transcript":
            print("\nTRANSCRIPT:")
            print(format_transcript(session_id))
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
