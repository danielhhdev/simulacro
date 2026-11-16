# Simulacro: guía de desarrollo con SDD

Nov 3, 2026 · @Daniel

Esta guía es el mapa para construir Simulacro (el carnet de conducir para agentes de IA) con SDD: qué herramientas usar, en qué orden se construye y qué agentes de desarrollo trabajan en cada paso. Las specs concretas de cada fase se generan con Spec Kit a partir de lo que aquí se describe.

## Cómo usar esta guía

- **Antes de cada fase:** leer su apartado en Fases y lanzar el flujo SDD (sección Flujo SDD) con su objetivo y criterios de hecho.
- **Durante la fase:** dejar que los subagentes implementen y revisen; tú validas specs, planes y demos.
- **Al cerrar la fase:** grabar la demo. Si no se puede enseñar en un vídeo, la fase no está cerrada.

**Producto en una frase:** un gemelo de una empresa donde se conecta un agente externo por MCP, se le pone a prueba con ataques, se autocorrige lo que falla y sale con un carnet de permisos mínimos verificados.

**Fuera de alcance (por ahora):** voz, interfaz para clientes externos, despliegue multiusuario, cualquier dato real de empresa.

## Arquitectura

La pieza central es la pasarela de permisos: el agente bajo prueba nunca toca la empresa directamente.

&#91;embedded content: arquitectura de Simulacro · 9 componentes\]

El harness lanza la tarea y, tras evaluar, corrige la política de la pasarela y repite. De las trazas se deducen los permisos mínimos que acaban en el carnet. Los empleados usan los mismos sistemas MCP, y desde la fase 4 consultan el grafo de contexto.

## Stack

Todo en Python, con piezas que se incorporan solo cuando una fase las necesita. Las versiones se fijan en `pyproject.toml` al arrancar la fase 0.

| Capa | Herramienta | Para qué | Entra en |
| --- | --- | --- | --- |
| Lenguaje y entorno | Python 3.12+, uv | Proyecto, dependencias y entornos | Fase 0 |
| Calidad | ruff, mypy, pytest | Formato, lint, tipos y tests | Fase 0 |
| SDD | GitHub Spec Kit (`specify` CLI) | Constitución, specs, planes y tareas | Fase 0 |
| Desarrollo con agentes | Claude Code (subagentes, skills, hooks) | Implementar, revisar y probar | Fase 0 |
| Protocolo de herramientas | MCP (SDK oficial de Python) | Exponer los sistemas falsos de la empresa al agente bajo prueba | Fase 1 |
| Empleados virtuales | LangGraph | Empleados con rol, memoria y comportamiento atacante | Fase 1 |
| API y orquestación | FastAPI, Pydantic | Lanzar escenarios, servir resultados y el carnet | Fase 1 |
| Persistencia | SQLite (luego PostgreSQL si hace falta) | Escenarios, ejecuciones, auditoría | Fase 1 |
| Trazas | Langfuse u OpenTelemetry | Ver cada paso del agente y su coste | Fase 1 |
| Políticas de acceso | Políticas en código (luego OPA/Rego) | Permisos por agente y carnet exportable | Fase 1 |
| Evals | pytest + juez LLM + comprobaciones deterministas | Puntuar tarea, seguridad y coste | Fase 1 |
| Contexto | Neo4j + GraphRAG | Grafo de conocimiento de la empresa | Fase 4 |
| Panel | Frontend web ligero (p. ej. React o Streamlit) | Traza en directo y antes/después para la demo | Fase 5 |
| Contenedores | Docker Compose | Levantar todo con un comando | Fase 1 |

**Decisión:** de los 3 empleados virtuales del MVP, 2 se hacen con LangGraph y 1 con un Agent SDK (por ejemplo, el Claude Agent SDK). Así se aprenden las dos librerías y se pueden comparar en el mismo proyecto. Los tres implementan la misma interfaz de empleado, así que el resto del sistema no distingue cómo está hecho cada uno.

## Flujo SDD con Spec Kit

Cada fase es una o varias features de Spec Kit, y cada feature recorre el mismo ciclo. La constitución se escribe una sola vez, en la fase 0. Spec Kit va por la versión 1.0.x ([releases](https://github.com/github/spec-kit/releases)).

**Instalación e inicio**

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.0.1
specify init simulacro --integration claude
```

Con la integración de Claude, los comandos aparecen como skills en Claude Code. Según la versión se escriben `/speckit.specify` o `/speckit-specify`.

**Ciclo por feature**

1. `constitution` (solo fase 0): principios no negociables del proyecto.
2. `specify`: qué y por qué, sin tecnología. Genera `spec.md`. Tú lo revisas.
3. `clarify`: el agente pregunta lo ambiguo antes de planificar.
4. `plan`: cómo, con stack y arquitectura. Genera `plan.md`, modelo de datos y contratos.
5. `checklist` (opcional): lista de calidad de requisitos.
6. `tasks`: desglose en `tasks.md`, ordenado y con tareas paralelizables marcadas.
7. `analyze`: comprueba coherencia entre spec, plan y tareas. No se implementa si hay huecos.
8. `implement`: los subagentes ejecutan las tareas.
9. **Cierre (tuyo):** revisión, demo grabada, merge.

**Principios de la constitución**

- Cada feature se puede enseñar en una demo.
- Ningún agente (bajo prueba ni empleado) accede a nada sin un permiso explícito y auditado.
- Las ejecuciones de agentes son no deterministas: toda métrica se calcula sobre varias ejecuciones.
- Todo comportamiento importante tiene test; las evals forman parte del código, no son un extra.
- Sin datos reales de empresas ni secretos en el repositorio.
- Código legible para alguien que aprende Python: tipos, nombres claros, funciones cortas.

## Fases

Seis fases. Las fases 0 y 1 dan ya el vídeo del MVP; el resto añade profundidad. No se pasa de fase sin su demo.

### Fase 0: cimientos

**Objetivo:** repositorio listo para trabajar con agentes y SDD.

- Repo con uv, ruff, mypy, pytest y CI básico (GitHub Actions).
- `specify init` con la integración de Claude y constitución escrita.
- `CLAUDE.md`, subagentes de desarrollo y hooks de calidad (sección Agentes).
- Esqueleto de carpetas (sección Estructura).

**Hecho cuando:** un "hola mundo" pasa lint, tipos y tests en CI, y un subagente puede implementar una tarea trivial de principio a fin.

### Fase 1: MVP, la primera prueba de fuego

**Objetivo:** el vídeo de 60 segundos. El agente entra, falla, se corrige y sale con carnet.

Features de Spec Kit sugeridas:

1. **Empresa a mano:** 3 empleados virtuales con rol y memoria simple; 2 sistemas falsos (tickets y correo) como servidores MCP.
2. **Pasarela de permisos:** todo acceso del agente pasa por una capa que comprueba su token, aplica su política y lo registra.
3. **Escenario y ataque:** 1 tarea ("resuelve la incidencia del cliente X") y 1 ataque (un empleado pide datos que no corresponden).
4. **Evaluación:** tarea resuelta, permisos usados frente a concedidos, si cayó en el ataque, pasos y coste.
5. **Autoarreglo de permisos:** deducir los permisos mínimos de la traza, aplicar la política recortada y repetir.
6. **Carnet:** documento exportable (JSON y vista legible) con permisos mínimos, puntuación y política.

**Demo:** conectar un agente real (por ejemplo, Claude Code) por MCP, ver el ataque, el fallo, el recorte y el antes y después.

**Hecho cuando:** el escenario corre con un comando, se repite 5 veces con resultados agregados y genera el carnet.

### Fase 2: más ataques y más arreglos

**Objetivo:** que la autocuración no sea un truco de un solo caso.

- Ataques: inyección de prompts en un ticket, documento envenenado en la wiki, suplantación de un jefe.
- Arreglos: añadir el contexto que faltaba, guardrails contra instrucciones de fuentes no fiables, políticas más estrictas.
- Diagnóstico: el harness clasifica cada fallo (permisos, contexto, fuente no fiable) antes de elegir el arreglo.

**Hecho cuando:** al menos 3 tipos de ataque y 3 tipos de arreglo, cada uno con su test y su prueba de antes y después.

### Fase 3: génesis

**Objetivo:** crear una empresa a partir de un párrafo.

- Generador que, desde una descripción, produce empleados, sistemas MCP, datos de ejemplo y escenarios.
- Validación del gemelo generado (esquema, coherencia, escenarios ejecutables).
- Plantillas de sector: consultora, ecommerce, clínica y **fábrica aeronáutica**. Esta última es una empresa gemela con planificación de producción, órdenes de trabajo, control de calidad y trazabilidad de piezas, donde el agente bajo prueba gestiona incidencias de una célula de fabricación. Sirve de puente con la línea de Physical AI de Sopra Steria y FIDAMC (simulación y gemelos digitales para robótica industrial): mismo patrón de probar en un gemelo antes de lo real, aplicado a los agentes que coordinan la producción en lugar de a los robots.

**Hecho cuando:** una descripción nueva produce en minutos una empresa sobre la que corren los escenarios sin tocar código.

### Fase 4: contexto con GraphRAG

**Objetivo:** que la empresa tenga memoria y conocimiento estructurado.

- Grafo en Neo4j: personas, equipos, clientes, procesos, documentos y quién puede ver qué.
- GraphRAG para que empleados y arreglos de contexto consulten el grafo.
- Los permisos del grafo alimentan la política del carnet.

**Hecho cuando:** un escenario falla sin el grafo y se resuelve con él, y la diferencia aparece medida en la puntuación.

### Fase 5: soberanía, ranking y panel

**Objetivo:** la demo completa para LinkedIn.

- Mismo escenario con distintos modelos de fondo, incluido uno de pesos abiertos.
- Ranking de agentes y modelos por tarea, seguridad y coste.
- Panel web con la traza en directo, los ataques, los arreglos y el carnet.

**Hecho cuando:** el vídeo final se graba de principio a fin desde el panel.

## Agentes y subagentes de desarrollo

El agente principal de Claude Code orquesta y delega en subagentes especializados, cada uno con su propio contexto, herramientas limitadas y modelo. Viven en `.claude/agents/` y se versionan con el repo ([docs de subagentes](https://code.claude.com/docs/en/sub-agents)). No hay que confundirlos con los empleados virtuales del producto: estos agentes construyen Simulacro; aquellos son parte de él.

| Subagente | Cuándo entra | Herramientas | Modelo |
| --- | --- | --- | --- |
| `architect` | En `plan`: propone diseño, contratos y riesgos; no escribe código | Read, Grep, Glob, WebSearch | Opus |
| `python-implementer` | En `implement`: ejecuta tareas de `tasks.md` con tests primero | Read, Edit, Write, Bash | Sonnet |
| `test-writer` | Antes de cada tarea: escribe tests a partir de los criterios de la spec | Read, Write, Bash | Sonnet |
| `code-reviewer` | Tras cada tarea: calidad, legibilidad y fidelidad a la spec | Read, Grep, Glob, Bash | Sonnet |
| `security-reviewer` | Al tocar permisos, MCP, tokens o ataques | Read, Grep, Glob | Opus |
| `eval-designer` | Fases 1, 2 y 4: diseña escenarios, ataques y métricas | Read, Write | Opus |
| `python-tutor` | Cuando quieras: explica el código recién escrito para aprender Python | Read, Grep | Sonnet |
| `demo-scribe` | Al cerrar fase: guion del vídeo, README y post de LinkedIn | Read, Write | Sonnet |

**Flujo típico de una tarea en `implement`**

1. `test-writer` escribe los tests de la tarea (fallan).
2. `python-implementer` escribe el código hasta que pasan.
3. `code-reviewer` revisa; si toca permisos o MCP, también `security-reviewer`.
4. Opcional: `python-tutor` te explica lo que se ha escrito.

**Plantilla de subagente** (`.claude/agents/python-implementer.md`)

```markdown
---
name: python-implementer
description: Implementa tareas de tasks.md de Spec Kit en Python. Úsalo durante /speckit.implement, una tarea cada vez.
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
---

Eres un desarrollador Python sénior en el proyecto Simulacro.

Antes de escribir código:
- Lee la constitución, spec.md, plan.md y la tarea asignada.
- Comprueba que existen tests para la tarea; si no, para y avisa.

Al escribir código:
- Python 3.12, tipado completo, funciones cortas, nombres claros.
- Ningún acceso a sistemas sin pasar por la pasarela de permisos.
- Nada de secretos ni datos reales.

Al terminar:
- Ejecuta `uv run ruff check`, `uv run mypy` y `uv run pytest`.
- Marca la tarea en tasks.md y resume qué cambió en 3 líneas.
```

**Más configuración de Claude Code**

- `CLAUDE.md`: resumen del proyecto, comandos de uv y enlace a la constitución.
- **Hooks:** tras cada edición, `ruff format` y `ruff check`; antes de terminar una tarea, la batería de tests.
- **Skills propias:** `nuevo-escenario` (plantilla de escenario más ataque) y `nuevo-servidor-mcp` (esqueleto de sistema falso).
- **Permisos:** prohibir `git push` y borrados fuera del repo; pedir confirmación para instalar dependencias.

## Estructura del repositorio

```text
simulacro/
├── .claude/
│   ├── agents/            # subagentes de desarrollo
│   ├── skills/            # nuevo-escenario, nuevo-servidor-mcp
│   └── settings.json      # hooks y permisos
├── .specify/              # constitución, plantillas y scripts de Spec Kit
├── specs/                 # una carpeta por feature: spec.md, plan.md, tasks.md
├── src/simulacro/
│   ├── company/           # empleados virtuales y su memoria
│   ├── systems/           # servidores MCP falsos (tickets, correo, wiki)
│   ├── gateway/           # pasarela de permisos, tokens y auditoría
│   ├── scenarios/         # tareas y ataques
│   ├── harness/           # ejecución, evaluación, diagnóstico y autoarreglo
│   ├── license/           # generación del carnet
│   ├── genesis/           # fase 3
│   ├── context/           # fase 4: grafo y GraphRAG
│   └── api/               # FastAPI
├── evals/                 # escenarios de evaluación y resultados
├── tests/
├── dashboard/             # fase 5
├── docker-compose.yml
├── pyproject.toml
└── CLAUDE.md
```

## Convenciones y definición de hecho

**Convenciones**

- Una rama por feature de Spec Kit (`001-empresa-a-mano`, `002-pasarela-permisos`…).
- Commits pequeños, uno por tarea de `tasks.md`.
- Tipos en todo el código; Pydantic para cualquier dato que cruce una frontera (API, MCP, carnet).
- Las llamadas a modelos pasan por un único cliente con registro de coste y trazas.
- Los escenarios se describen en ficheros (YAML), no en código.

**Una tarea está hecha cuando**

- [ ] Tiene tests y pasan, junto con ruff y mypy.
- [ ] La ha revisado `code-reviewer` (y `security-reviewer` si toca permisos).
- [ ] Está marcada en `tasks.md`.

**Una fase está hecha cuando**

- [ ] Cumple su "hecho cuando".
- [ ] Las métricas se han calculado sobre varias ejecuciones.
- [ ] La demo está grabada y el README actualizado.

## CLAUDE.md

Fichero raíz para Claude Code. Copiar tal cual en `simulacro/CLAUDE.md` al crear el proyecto.

```markdown
# Simulacro

Carnet de conducir para agentes de IA. Una empresa gemela con empleados virtuales
y sistemas falsos expuestos por MCP. Se conecta un agente externo, se le pone a
prueba con ataques, el harness corrige lo que falla y emite un carnet con los
permisos mínimos verificados.

## Cómo trabajamos
- SDD con GitHub Spec Kit. Constitución en `.specify/memory/constitution.md`.
- Cada feature vive en `specs/NNN-nombre/` (spec.md, plan.md, tasks.md).
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
- Instalar: `uv sync`
- Tests: `uv run pytest`
- Lint y formato: `uv run ruff check --fix && uv run ruff format`
- Tipos: `uv run mypy src`
- Levantar todo: `docker compose up`

## Estructura
- `src/simulacro/company/`: empleados virtuales (2 con LangGraph, 1 con Agent SDK) y su memoria.
- `src/simulacro/systems/`: servidores MCP falsos (tickets, correo, wiki).
- `src/simulacro/gateway/`: pasarela de permisos, tokens y auditoría.
- `src/simulacro/scenarios/`: tareas y ataques (definidos en YAML).
- `src/simulacro/harness/`: ejecución, evaluación, diagnóstico y autoarreglo.
- `src/simulacro/license/`: generación del carnet.
- `evals/`, `tests/`, `specs/`.

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

## Definición de hecho
Una tarea está hecha cuando tiene tests que pasan, ruff y mypy están limpios,
la ha revisado code-reviewer y está marcada en tasks.md.
```

## Fuentes

- [GitHub Spec Kit: releases](https://github.com/github/spec-kit/releases)
- [GitHub Spec Kit: guía de instalación](https://github.github.com/spec-kit/installation.html)
- [Claude Code: subagentes](https://code.claude.com/docs/en/sub-agents)
