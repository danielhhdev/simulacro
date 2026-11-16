<!--
Sync Impact Report
- Versión: plantilla → 1.0.0 (ratificación inicial)
- Principios añadidos: I–VI (todos nuevos)
- Secciones añadidas: Restricciones técnicas, Flujo de desarrollo, Gobierno
- Secciones eliminadas: ninguna
- TODOs: ninguno
-->

# Constitución de Simulacro

Simulacro es el carnet de conducir para agentes de IA: una empresa gemela con empleados
virtuales y sistemas falsos expuestos por MCP, donde se conecta un agente externo, se le
pone a prueba con ataques, el harness corrige lo que falla y se emite un carnet con los
permisos mínimos verificados.

## Principios fundamentales

### I. Cada feature se puede enseñar en una demo

- Toda feature termina en algo que se puede ejecutar y enseñar en un vídeo corto.
- Si una feature no se puede demostrar, no está terminada: se divide o se replantea.
- Cada fase se cierra con una demo grabada y el README actualizado.

**Por qué:** el proyecto se valida enseñándolo. Lo que no se ve no existe para quien lo evalúa.

### II. Ningún acceso sin permiso explícito y auditado (NO NEGOCIABLE)

- Ningún agente, ni el agente bajo prueba ni los empleados virtuales, accede a un sistema
  sin pasar por la pasarela de permisos.
- Cada acceso se comprueba contra un token y una política explícita, y queda registrado
  en la auditoría (quién, qué, cuándo, resultado).
- Por defecto se deniega: lo que la política no permite de forma explícita está prohibido.
- Todo cambio que toque permisos, MCP, tokens o ataques pasa por una revisión de seguridad.

**Por qué:** el carnet solo vale si cada permiso se ha observado y verificado. Un atajo en la
pasarela invalida todo el producto.

### III. Las métricas se calculan sobre varias ejecuciones

- Las ejecuciones de agentes son no deterministas. Ninguna métrica se saca de una sola ejecución.
- Cada escenario se repite N veces (5 por defecto) y se informa el agregado: media, dispersión
  y tasa de éxito.
- Los resultados indican el modelo, la versión del escenario y la semilla cuando la haya.

**Por qué:** una ejecución aislada puede ser suerte. Las conclusiones del carnet y del ranking
tienen que ser reproducibles.

### IV. Tests primero; las evals son código (NO NEGOCIABLE)

- Todo comportamiento importante tiene un test. Los tests se escriben antes que el código y
  primero fallan.
- Las evals (escenarios, ataques, métricas y juez LLM) viven en el repositorio, se versionan
  y se ejecutan como parte de la batería de tests.
- Una tarea no está hecha si ruff, mypy o pytest fallan.

**Por qué:** en un sistema con LLMs, sin tests y evals es imposible saber si un cambio mejora
o empeora el comportamiento.

### V. Sin datos reales ni secretos

- No se usan datos reales de empresas ni de personas. Toda la empresa gemela es ficticia.
- Ningún secreto (claves de API, tokens) entra en el repositorio. Van en `.env`, que está
  ignorado por git, con un `.env.example` documentado.

**Por qué:** es un proyecto público de demostración y de seguridad. Filtrar un dato o una
clave contradice lo que el producto promete.

### VI. Código legible para quien aprende Python

- Tipado completo con mypy en modo estricto.
- Nombres explícitos y funciones cortas con una sola responsabilidad.
- Nada de trucos: se prefiere lo claro a lo ingenioso.
- Pydantic en todo dato que cruza una frontera (API, MCP, carnet).
- Docstrings breves en español en los módulos y funciones públicas.

**Por qué:** el autor viene de Java/Spring y está aprendiendo Python con este proyecto. El
código tiene que servir también para aprender.

## Restricciones técnicas

- Python 3.12+ gestionado con uv. Calidad con ruff, mypy (estricto) y pytest.
- Los sistemas falsos de la empresa se exponen con el SDK oficial de MCP para Python.
- Empleados virtuales: 2 con LangGraph y 1 con un Agent SDK, todos con la misma interfaz
  de empleado.
- API con FastAPI y Pydantic, y persistencia en SQLite (PostgreSQL solo si hace falta).
- Toda llamada a un modelo pasa por un único cliente común que registra el coste y la traza.
- Los escenarios y ataques se describen en ficheros YAML, no en código.
- Las dependencias se añaden solo cuando una fase las necesita, y con confirmación del autor.

## Flujo de desarrollo

- SDD con GitHub Spec Kit: `specify` → `clarify` → `plan` → `tasks` → `analyze` → `implement`.
- No se implementa nada que no esté en `tasks.md`. Si falta algo, se para y se avisa.
- Una rama por feature (`NNN-nombre`) y un commit pequeño por tarea.
- Ciclo de cada tarea: `test-writer` escribe los tests (fallan), `python-implementer` escribe
  el código hasta que pasan, y `code-reviewer` revisa (más `security-reviewer` si toca
  permisos, MCP o tokens).
- La CI (GitHub Actions) ejecuta ruff, mypy y pytest en cada push y en cada PR.

## Gobierno

- Esta constitución prevalece sobre cualquier otra práctica del proyecto. `CLAUDE.md` la
  resume para el trabajo diario con agentes.
- Los planes (`plan.md`) incluyen una comprobación explícita frente a estos principios. Toda
  desviación se justifica por escrito en la sección de complejidad del plan.
- Enmiendas: se proponen con `/speckit-constitution`, las aprueba el autor y se versionan con
  semver. MAJOR elimina o redefine un principio, MINOR añade un principio o una sección y
  PATCH aclara la redacción.

**Versión**: 1.0.0 | **Ratificada**: 2026-11-16 | **Última enmienda**: 2026-11-16
