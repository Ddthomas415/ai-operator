import builtins

import pytest

import repl


def test_prompt_raises_eoferror(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: (_ for _ in ()).throw(EOFError()))
    with pytest.raises(EOFError):
        repl._prompt("> ")


def test_prompt_raises_keyboardinterrupt(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt):
        repl._prompt("> ")
