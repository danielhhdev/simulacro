"""Hook Stop: antes de terminar un turno, pasa ruff, mypy y pytest si hay cambios en Python.

Si algo falla, sale con código 2 y Claude recibe el error para arreglarlo antes de parar.
Si el hook ya bloqueó una vez en este turno (`stop_hook_active`), no vuelve a bloquear,
para evitar bucles infinitos.
"""

import json
import subprocess
import sys

CHECKS: list[tuple[str, list[str]]] = [
    ("ruff", ["uv", "run", "ruff", "check"]),
    ("mypy", ["uv", "run", "python", "-m", "mypy"]),
    ("pytest", ["uv", "run", "python", "-m", "pytest", "-q"]),
]


def hook_already_active() -> bool:
    """Indica si Claude ya está continuando por culpa de este mismo hook."""
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return False
    return bool(payload.get("stop_hook_active", False))


def python_files_changed() -> bool:
    """Comprueba con git si hay ficheros .py modificados o nuevos."""
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        capture_output=True,
        text=True,
        check=False,
    )
    if status.returncode != 0:
        return True  # Sin git no podemos saberlo: mejor comprobar.
    return any(line.rstrip().endswith(".py") for line in status.stdout.splitlines())


def main() -> int:
    if hook_already_active() or not python_files_changed():
        return 0

    failures: list[str] = []
    for name, command in CHECKS:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            output = (result.stdout + result.stderr).strip()
            failures.append(f"### {name} falla\n{output[-3000:]}")

    if failures:
        print("Las comprobaciones de calidad fallan:\n\n" + "\n\n".join(failures), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
