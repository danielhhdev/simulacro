"""Punto de entrada de la línea de comandos de Simulacro."""


def greeting(name: str = "mundo") -> str:
    """Devuelve el saludo de prueba de la fase 0."""
    return f"Hola, {name}, desde Simulacro"


def main() -> None:
    """Imprime el saludo. Se ejecuta con `uv run simulacro`."""
    print(greeting())
