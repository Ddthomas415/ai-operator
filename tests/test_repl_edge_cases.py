from pathlib import Path
import tempfile

import pytest

import repl
import session_store


def test_resolve_resume_last_without_session_raises(monkeypatch):
    monkeypatch.setattr(repl, "latest_session_id", lambda: None)
    with pytest.raises(SystemExit, match="No previous session found."):
        repl._resolve_session_from_args(["repl.py", "--resume-last"])


def test_resolve_resume_uses_given_session(monkeypatch):
    monkeypatch.setattr(repl, "start_session", lambda session_id=None: session_id or "new-session")
    assert repl._resolve_session_from_args(["repl.py", "--resume", "abc123"]) == "abc123"


def test_load_session_events_missing_file_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(session_store, "SESSIONS_DIR", tmp_path / "sessions")
    monkeypatch.setattr(session_store, "LATEST_FILE", (tmp_path / "sessions" / "latest.txt"))
    with pytest.raises(FileNotFoundError):
        session_store.load_session_events("missing-session")


def test_latest_session_id_none_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(session_store, "SESSIONS_DIR", tmp_path / "sessions")
    monkeypatch.setattr(session_store, "LATEST_FILE", (tmp_path / "sessions" / "latest.txt"))
    assert session_store.latest_session_id() is None


def test_format_transcript_empty_session(tmp_path, monkeypatch):
    sessions_dir = tmp_path / "sessions"
    monkeypatch.setattr(session_store, "SESSIONS_DIR", sessions_dir)
    monkeypatch.setattr(session_store, "LATEST_FILE", sessions_dir / "latest.txt")

    session_id = session_store.start_session("demo-session")

    # Session starts with only session_started, which should not render as user transcript.
    transcript = session_store.format_transcript(session_id)
    assert transcript == "No transcript yet."


def test_append_and_read_transcript(tmp_path, monkeypatch):
    sessions_dir = tmp_path / "sessions"
    monkeypatch.setattr(session_store, "SESSIONS_DIR", sessions_dir)
    monkeypatch.setattr(session_store, "LATEST_FILE", sessions_dir / "latest.txt")

    session_id = session_store.start_session("demo-session")
    session_store.append_session_event(session_id, "user_input", {"input": "read demo.py"})
    session_store.append_session_event(session_id, "output", {"message": "print('hi')"})

    transcript = session_store.format_transcript(session_id)
    assert "USER: read demo.py" in transcript
    assert "OUTPUT: print('hi')" in transcript
