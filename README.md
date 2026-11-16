# Simulacro

**El carnet de conducir para agentes de IA.**

Un gemelo de una empresa donde se conecta un agente externo por MCP, se le pone a prueba con
ataques, se autocorrige lo que falla y sale con un carnet de permisos mínimos verificados.

> Estado: **Fase 0, cimientos.** Repositorio preparado para desarrollo con SDD (GitHub Spec Kit)
> y Claude Code.

## Requisitos

- Python 3.12+ y [uv](https://docs.astral.sh/uv/)
- [GitHub Spec Kit](https://github.com/github/spec-kit) (`specify` CLI)
- Claude Code
- Docker (desde la fase 1)

## Empezar

```bash
uv sync
uv run python -m pytest
uv run ruff check && uv run ruff format --check
uv run python -m mypy
uv run python -m simulacro
```

## Cómo se desarrolla

Cada feature sigue el ciclo de Spec Kit: `/speckit-specify` → `/speckit-clarify` →
`/speckit-plan` → `/speckit-tasks` → `/speckit-analyze` → `/speckit-implement`.

- Principios del proyecto: [`.specify/memory/constitution.md`](.specify/memory/constitution.md)
- Guía de desarrollo y fases: [`Simulacro guía de desarrollo con SDD.md`](Simulacro%20guía%20de%20desarrollo%20con%20SDD.md)
- Instrucciones para Claude Code: [`CLAUDE.md`](CLAUDE.md)

## Fases

| Fase | Objetivo | Estado |
| --- | --- | --- |
| 0 | Cimientos: repo, SDD, agentes y CI | En curso |
| 1 | MVP: el agente entra, falla, se corrige y sale con carnet | Pendiente |
| 2 | Más ataques y más arreglos | Pendiente |
| 3 | Génesis: una empresa a partir de un párrafo | Pendiente |
| 4 | Contexto con GraphRAG | Pendiente |
| 5 | Soberanía, ranking y panel | Pendiente |
