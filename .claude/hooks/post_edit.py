"""Hook PostToolUse: formatea y revisa con ruff cada fichero .py recién editado.

Claude Code envía por stdin un JSON con `tool_input.file_path`. Si ruff encuentra
errores que no puede arreglar solo, sale con código 2 para que Claude los vea y los corrija.
"""

import json
import subprocess
import sys


def edited_file_path() -> str | None:
    """Lee del JSON de entrada la ruta del fichero editado, si la hay."""
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return None
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    return path if isinstance(path, str) else None


def run_ruff(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    """Ejecuta ruff a través de uv y devuelve el resultado."""
    return subprocess.run(
        ["uv", "run", "ruff", *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    path = edited_file_path()
    if path is None or not path.endswith(".py"):
        return 0

    run_ruff(["format", path])
    check = run_ruff(["check", "--fix", path])
    if check.returncode != 0:
        print(f"ruff encontró problemas en {path}:\n{check.stdout}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
