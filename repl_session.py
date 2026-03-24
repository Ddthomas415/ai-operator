from __future__ import annotations

import sys

from session_store import latest_session_id, load_session_events, start_session


def resolve_session_from_args(argv: list[str]) -> str:
    """
    Resolve the session id from CLI args.

    Supported:
    - no args: start a new session
    - --resume <session_id>: resume that exact session id
    - --resume-last: resume the latest known session
    """
    if len(argv) >= 3 and argv[1] == "--resume":
        session_id = argv[2]
        # Validate the session exists by attempting to load it.
        load_session_events(session_id)
        return start_session(session_id)

    if len(argv) >= 2 and argv[1] == "--resume-last":
        session_id = latest_session_id()
        if not session_id:
            raise SystemExit("No previous session found.")
        load_session_events(session_id)
        return start_session(session_id)

    return start_session()


def load_previous_events(session_id: str) -> list[dict]:
    """Load prior session events, returning an empty list if missing/corrupt."""
    try:
        return load_session_events(session_id)
    except FileNotFoundError:
        return []
