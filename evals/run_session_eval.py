from uuid import uuid4

from session_store import (
    append_session_event,
    format_transcript,
    latest_session_id,
    session_prompt_history,
    start_session,
)

CASES = [
    ("alpha", "read demo.py"),
    ("beta", "list workspace files"),
]


def run() -> tuple[int, int]:
    passed = 0
    total = 4

    session_id = start_session(f"eval-session-alpha-{uuid4().hex[:8]}")
    append_session_event(session_id, "user_input", {"input": CASES[0][1]})
    append_session_event(session_id, "output", {"message": "print('x')"})

    history = session_prompt_history(session_id)
    ok = history == [CASES[0][1]]
    print(f"1. {'PASS' if ok else 'FAIL'}")
    passed += int(ok)

    transcript = format_transcript(session_id)
    ok = "USER: read demo.py" in transcript and "OUTPUT: print('x')" in transcript
    print(f"2. {'PASS' if ok else 'FAIL'}")
    passed += int(ok)

    second_session = start_session(f"eval-session-beta-{uuid4().hex[:8]}")
    append_session_event(second_session, "user_input", {"input": CASES[1][1]})
    ok = latest_session_id() == second_session
    print(f"3. {'PASS' if ok else 'FAIL'}")
    passed += int(ok)

    resumed = start_session(second_session)
    ok = resumed == second_session
    print(f"4. {'PASS' if ok else 'FAIL'}")
    passed += int(ok)

    print(f"Passed {passed}/{total}")
    return passed, total


if __name__ == "__main__":
    run()
