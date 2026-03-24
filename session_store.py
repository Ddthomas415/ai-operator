import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

SESSIONS_DIR = Path("logs/sessions")
LATEST_FILE = SESSIONS_DIR / "latest.txt"


def _session_path(session_id: str) -> Path:
    """Return the JSONL transcript path for a session id."""
    return SESSIONS_DIR / f"{session_id}.jsonl"


def start_session(session_id: str | None = None) -> str:
    """Create or resume a session and mark it as the latest session."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    resolved = session_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-") + uuid4().hex[:8]
    path = _session_path(resolved)
    if not path.exists():
        append_session_event(resolved, "session_started", {"session_id": resolved})
    LATEST_FILE.write_text(resolved, encoding="utf-8")
    return resolved


def latest_session_id() -> str | None:
    """Return the latest known session id, or None if none exists."""
    if not LATEST_FILE.exists():
        return None
    return LATEST_FILE.read_text(encoding="utf-8").strip() or None


def append_session_event(session_id: str, event_type: str, payload: dict) -> None:
    """Append one event row to the session transcript JSONL file."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "event_type": event_type,
        "payload": payload,
    }
    with _session_path(session_id).open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def load_session_events(session_id: str) -> list[dict]:
    """Load all JSONL events for a session id."""
    path = _session_path(session_id)
    if not path.exists():
        raise FileNotFoundError(f"Session {session_id} does not exist.")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def session_prompt_history(session_id: str) -> list[str]:
    """Return only user-input prompts from a saved session."""
    prompts: list[str] = []
    for event in load_session_events(session_id):
        if event["event_type"] == "user_input":
            prompts.append(event["payload"]["input"])
    return prompts


def format_transcript(session_id: str) -> str:
    """Render a human-readable transcript from stored session events."""
    lines: list[str] = []
    for event in load_session_events(session_id):
        event_type = event["event_type"]
        payload = event["payload"]
        if event_type == "user_input":
            lines.append(f"USER: {payload['input']}")
        elif event_type == "plan":
            lines.append(f"PLAN: {payload['step_count']} step(s)")
        elif event_type == "clarification_question":
            lines.append(f"CLARIFICATION: {payload['question']}")
        elif event_type == "clarification_answer":
            lines.append(f"ANSWER: {payload['answer']}")
        elif event_type == "output":
            lines.append(f"OUTPUT: {payload['message']}")
        elif event_type == "error":
            lines.append(f"ERROR: {payload['message']}")
    return "\n".join(lines) if lines else "No transcript yet."
