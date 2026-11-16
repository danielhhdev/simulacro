# Simulacro

Carnet de conducir para agentes de IA. Una empresa gemela con empleados virtuales
y sistemas falsos expuestos por MCP. Se conecta un agente externo, se le pone a
prueba con ataques, el harness corrige lo que falla y emite un carnet con los
permisos mínimos verificados.

Guía completa del proyecto: `Simulacro guía de desarrollo con SDD.md`.

## Cómo trabajamos
- SDD con GitHub Spec Kit. Constitución en `.specify/memory/constitution.md`.
- Cada feature vive en `specs/NNN-nombre/` (spec.md, plan.md, tasks.md).
- Skills de Spec Kit: `/speckit-specify`, `/speckit-clarify`, `/speckit-plan`,
  `/speckit-tasks`, `/speckit-analyze`, `/speckit-implement`.
- No se implementa nada que no esté en `tasks.md`. Si falta algo, se para y se avisa.
- Una tarea cada vez: tests primero, luego código, luego revisión.
- El autor está aprendiendo Python (viene de Java/Spring): código claro, tipado y
  con nombres explícitos. Nada de trucos.

## Stack
- Python 3.12+, uv, ruff, mypy, pytest.
- Empleados virtuales: 2 con LangGraph y 1 con un Agent SDK, todos con la misma interfaz.
- MCP (SDK oficial de Python) para los sistemas falsos.
- FastAPI + Pydantic, SQLite, Langfuse para trazas, Docker Compose.
- Neo4j + GraphRAG desde la fase 4.

## Comandos
En esta máquina Windows los lanzadores `.exe` de `.venv` están bloqueados por
política corporativa ("Acceso denegado"). Usa siempre `uv run python -m <herramienta>`
(ruff es binario nativo y funciona directo).

- Instalar: `uv sync`
- Tests: `uv run python -m pytest`
- Lint y formato: `uv run ruff check --fix && uv run ruff format`
- Tipos: `uv run python -m mypy`
- Ejecutar: `uv run python -m simulacro`
- Levantar todo (desde la fase 1): `docker compose up`

## Estructura
- `src/simulacro/company/`: empleados virtuales (2 con LangGraph, 1 con Agent SDK) y su memoria.
- `src/simulacro/systems/`: servidores MCP falsos (tickets, correo, wiki).
- `src/simulacro/gateway/`: pasarela de permisos, tokens y auditoría.
- `src/simulacro/scenarios/`: tareas y ataques (definidos en YAML).
- `src/simulacro/harness/`: ejecución, evaluación, diagnóstico y autoarreglo.
- `src/simulacro/license/`: generación del carnet.
- `src/simulacro/genesis/` (fase 3), `src/simulacro/context/` (fase 4), `src/simulacro/api/`.
- `evals/`, `tests/`, `specs/`, `dashboard/` (fase 5).

## Reglas no negociables
- Ningún acceso a los sistemas sin pasar por la pasarela de permisos.
- Toda llamada a un modelo pasa por el cliente común (registra coste y traza).
- Las métricas de agentes se calculan sobre varias ejecuciones, nunca una.
- Pydantic en todo dato que cruce una frontera (API, MCP, carnet).
- Sin secretos ni datos reales en el repo. Las claves van en `.env`.
- No hacer `git push` ni instalar dependencias sin confirmación.

## Subagentes
Definidos en `.claude/agents/`: architect, python-implementer, test-writer,
code-reviewer, security-reviewer, eval-designer, python-tutor, demo-scribe.
Si un cambio toca permisos, MCP o tokens, pasa también por security-reviewer.

Flujo de cada tarea en `/speckit-implement`:
1. `test-writer` escribe los tests de la tarea (fallan).
2. `python-implementer` escribe el código hasta que pasan.
3. `code-reviewer` revisa (y `security-reviewer` si toca permisos, MCP o tokens).
4. Opcional: `python-tutor` explica lo escrito.

## Hooks
- Tras cada edición de un `.py`: `ruff format` y `ruff check --fix` sobre ese fichero.
- Al terminar un turno con cambios en Python: ruff, mypy y pytest; si fallan, hay que arreglarlo.

## Definición de hecho
Una tarea está hecha cuando tiene tests que pasan, ruff y mypy están limpios,
la ha revisado code-reviewer y está marcada en tasks.md.
