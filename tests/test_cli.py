"""Tests del hola mundo de la fase 0."""

import pytest

from simulacro.cli import greeting, main


def test_greeting_uses_default_name() -> None:
    assert greeting() == "Hola, mundo, desde Simulacro"


def test_greeting_uses_given_name() -> None:
    assert greeting("Daniel") == "Hola, Daniel, desde Simulacro"


def test_main_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hola, mundo, desde Simulacro"
