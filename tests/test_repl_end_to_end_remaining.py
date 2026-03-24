from pathlib import Path

import pytest

import repl
import session_store


def test_resolve_resume_returns_given_session_id(monkeypatch):
    monkeypatch.setattr(repl, "start_session", lambda session_id=None: session_id or "new-session")
    assert repl._resolve_session_from_args(["repl.py", "--resume", "missing-session"]) == "missing-session"


def test_overwrite_confirm_yes(monkeypatch):
    monkeypatch.setattr(repl, "_prompt", lambda _: "y")
    assert repl._confirm_overwrite("demo.py") is True


def test_overwrite_confirm_no(monkeypatch):
    monkeypatch.setattr(repl, "_prompt", lambda _: "n")
    assert repl._confirm_overwrite("demo.py") is False


def test_overwrite_confirm_empty_defaults_no(monkeypatch):
    monkeypatch.setattr(repl, "_prompt", lambda _: "")
    assert repl._confirm_overwrite("demo.py") is False


def test_corrupted_session_file_raises(tmp_path, monkeypatch):
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(session_store, "SESSIONS_DIR", sessions_dir)
    monkeypatch.setattr(session_store, "LATEST_FILE", sessions_dir / "latest.txt")

    bad = sessions_dir / "broken.jsonl"
    bad.write_text('{"bad":\n', encoding="utf-8")

    with pytest.raises(Exception):
        session_store.load_session_events("broken")

def test_overwrite_confirm_yes(monkeypatch):
    monkeypatch.setattr(repl, "_prompt", lambda _: "y")
    assert repl._confirm_overwrite("demo.py") is True

def test_overwrite_confirm_no(monkeypatch):
    monkeypatch.setattr(repl, "_prompt", lambda _: "n")
    assert repl._confirm_overwrite("demo.py") is False

def test_overwrite_confirm_empty_defaults_no(monkeypatch):
    monkeypatch.setattr(repl, "_prompt", lambda _: "")
    assert repl._confirm_overwrite("demo.py") is False
