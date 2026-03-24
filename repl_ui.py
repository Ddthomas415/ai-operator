from __future__ import annotations

from session_store import format_transcript, session_prompt_history


def show_session_banner(session_id: str, previous_event_count: int) -> None:
    """Print the REPL banner and current session state."""
    print("AI Operator REPL")
    print("Type 'quit' to exit.")
    print("Type 'history' to show this session's prompts.\n")
    print(f"Session: {session_id}")
    if previous_event_count > 1:
        print(f"Resumed with {len(session_prompt_history(session_id))} prior prompt(s).")
    print("Type 'transcript' to show the saved session transcript.\n")


def handle_builtin_command(user_input: str, session_id: str) -> bool:
    """
    Handle REPL built-in commands.

    Returns True if the command was handled and the caller should continue
    the REPL loop without running the planner.
    """
    command = user_input.lower()

    if command == "history":
        print("\nHISTORY:")
        history = session_prompt_history(session_id)
        if history:
            for index, entry in enumerate(history, 1):
                print(f"{index}. {entry}")
        else:
            print("No prompts yet.")
        return True

    if command == "transcript":
        print("\nTRANSCRIPT:")
        print(format_transcript(session_id))
        return True

    return False
