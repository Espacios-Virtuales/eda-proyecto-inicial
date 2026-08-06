# Roadmap

## Current Baseline

El repositorio parte de una base real de laboratorio EDA:

- runner local de notebooks en `src/main.py`;
- notebooks `lab_eda_v1`, `lab_eda_v2` y `lab_eda_v3`;
- dataset `data/personas_eda.csv`;
- documentacion pedagogica inicial;
- dependencias minimas para pandas, Jupyter y nbconvert.

No existen API HTTP, base de datos, migraciones, modelos, autenticacion, tests ni integraciones externas. Por eso el roadmap empieza consolidando el repositorio y luego introduce capas de aplicacion de forma incremental.

## Phase 1 - Documentation and Repository Consolidation

Objetivo:

- congelar una arquitectura documental coherente con el codigo existente.

Componentes:

- README actualizado;
- arquitectura;
- modelo de datos conceptual;
- contratos HTTP;
- roadmap;
- limpieza de referencias obsoletas.

Contratos afectados:

- ninguno implementado.

Pruebas requeridas:

- `git diff --check`;
- validacion de sintaxis Python existente;
- revision de enlaces Markdown;
- busqueda de referencias obsoletas.

Criterio de cierre:

- documentacion consistente con el estado real;
- ninguna implementacion nueva de API, modelos o migraciones.

## Phase 2 - HTTP Skeleton

Objetivo:

- crear el skeleton de `neuronas-ev-lab-api` sin logica compleja.

Componentes:

- seleccion de framework HTTP;
- estructura de aplicacion;
- healthcheck;
- versionado `/api/v1`;
- manejo base de errores;
- configuracion por entorno.

Contratos afectados:

- base comun de API;
- errores;
- versionado.

Pruebas requeridas:

- tests de healthcheck;
- tests de errores comunes;
- lint o formato definido;
- validacion de arranque local.

Criterio de cierre:

- servidor local arranca;
- existe una ruta de salud;
- no hay persistencia todavia salvo configuracion basica.

## Phase 3 - PostgreSQL and Migrations

Objetivo:

- introducir persistencia propia de Neuronas.

Componentes:

- conexion PostgreSQL;
- herramienta de migraciones;
- esquema inicial;
- modelo `Principal` minimo;
- convenciones de IDs y timestamps.

Contratos afectados:

- ninguno publico obligatorio, salvo health/config internos.

Pruebas requeridas:

- migracion upgrade/downgrade o equivalente;
- tests de conexion en ambiente local/test;
- tests de constraints internas.

Criterio de cierre:

- base Neuronas separada;
- ninguna foreign key externa;
- migraciones versionadas.

## Phase 4 - Principals and EVAAS Administration

Objetivo:

- permitir proyeccion administrativa desde EVAAS sin compartir base de datos.

Componentes:

- `Principal`;
- `Enrollment`;
- organizacion como referencia externa;
- estado de acceso;
- idempotencia en sync.

Contratos afectados:

- `PUT /api/v1/admin/principals/{external_principal_id}`;
- `POST /api/v1/admin/principals/{principal_id}/activate`;
- `POST /api/v1/admin/principals/{principal_id}/deactivate`;
- `PUT /api/v1/admin/organizations/{external_organization_id}`;
- `PUT /api/v1/admin/enrollments/{external_enrollment_id}`;
- `GET /api/v1/admin/principals/{principal_id}/access`.

Pruebas requeridas:

- idempotencia;
- activacion/desactivacion;
- no borrado de historial;
- autorizacion de service token.

Criterio de cierre:

- EVAAS puede administrar acceso solo por contratos.

## Phase 5 - Student Base and Learning Progress

Objetivo:

- modelar aprendizaje y avance estudiantil.

Componentes:

- `StudentProfile`;
- `LearningModule`;
- `Capsule`;
- `LearningProgress`;
- seed inicial para linea EDA.

Contratos afectados:

- futuros endpoints de consulta y progreso.

Pruebas requeridas:

- creacion de perfiles;
- progreso por modulo/capsula;
- reglas de acceso segun enrollment.

Criterio de cierre:

- Neuronas puede representar estudiantes y progreso sin depender de tablas EVAAS.

## Phase 6 - Collaborative Workspaces

Objetivo:

- habilitar espacios colaborativos para laboratorio.

Componentes:

- `Workspace`;
- `WorkspaceMember`;
- roles locales;
- permisos de lectura/escritura por workspace.

Contratos afectados:

- endpoints futuros de workspaces y members.

Pruebas requeridas:

- membresia;
- autorizacion por rol;
- aislamiento entre workspaces.

Criterio de cierre:

- un principal puede operar solo dentro de workspaces permitidos.

## Phase 7 - LabRuns and LabArtifacts

Objetivo:

- registrar experimentos y resultados trazables.

Componentes:

- `LabRun`;
- `LabArtifact`;
- estados de ejecucion;
- metricas;
- referencias de almacenamiento;
- checksums.

Contratos afectados:

- `POST /api/v1/lab-runs`;
- `GET /api/v1/lab-runs/{lab_run_id}`;
- `POST /api/v1/lab-runs/{lab_run_id}/results`;
- `POST /api/v1/lab-runs/{lab_run_id}/artifacts`;
- `POST /api/v1/lab-runs/{lab_run_id}/close`.

Pruebas requeridas:

- transiciones de estado;
- idempotencia;
- registro de metricas;
- registro de artefactos;
- autorizacion por workspace.

Criterio de cierre:

- un experimento puede trazarse desde creacion hasta cierre.

## Phase 8 - Google Colab Integration

Objetivo:

- permitir que notebooks externos reporten ejecuciones a Neuronas.

Componentes:

- tokens temporales;
- scopes limitados;
- helper cliente para notebooks;
- flujo create/run/results/artifacts/close.

Contratos afectados:

- `POST /api/v1/colab/sessions`;
- contratos de LabRuns.

Pruebas requeridas:

- token limitado;
- expiracion;
- envio de metricas;
- envio de artefactos;
- cierre idempotente.

Criterio de cierre:

- un notebook externo puede registrar un LabRun sin acceder a base de datos ni secretos internos.

## Phase 9 - Review and Validation

Objetivo:

- introducir revision tecnica/pedagogica y evidencia de validacion.

Componentes:

- `Review`;
- observaciones;
- aprobacion/rechazo;
- evidencia de validacion;
- reglas para `VALIDATED`.

Contratos afectados:

- `POST /api/v1/reviews`;
- `POST /api/v1/reviews/{review_id}/approve`;
- `POST /api/v1/reviews/{review_id}/reject`;
- `POST /api/v1/reviews/{review_id}/observations`;
- `POST /api/v1/reviews/{review_id}/validation-evidence`.

Pruebas requeridas:

- permisos de reviewer;
- estados de review;
- evidencia obligatoria para validacion;
- rechazo y cambios solicitados.

Criterio de cierre:

- un artefacto puede pasar por revision y quedar validado con evidencia.

## Phase 10 - Promotion Candidates and EVAAS Integration

Objetivo:

- convertir artefactos validados en candidatos trazables.

Componentes:

- `PromotionCandidate`;
- `IntegrationCandidate`;
- versionado;
- decision del sistema receptor;
- paquetes o referencias de integracion.

Contratos afectados:

- `POST /api/v1/promotion-candidates`;
- `POST /api/v1/integration-candidates`.

Pruebas requeridas:

- solo artefactos validados pueden promoverse;
- `VALIDATED != PRODUCTION`;
- decision externa no modifica historial;
- versionado de candidatos.

Criterio de cierre:

- Neuronas puede proponer integraciones sin modificar EVAAS, Liora ni servicios productivos.

## Phase 11 - Observability, Security and Pilot

Objetivo:

- preparar piloto controlado.

Componentes:

- logging estructurado;
- request IDs;
- auditoria;
- rate limits;
- politicas de retencion;
- monitoreo basico;
- hardening de configuracion.

Contratos afectados:

- todos los contratos publicos.

Pruebas requeridas:

- trazabilidad de requests;
- autorizacion negativa;
- errores consistentes;
- pruebas de carga minimas;
- revision de secretos y configuracion.

Criterio de cierre:

- piloto ejecutable con usuarios controlados, datos propios de Neuronas y fronteras respetadas.
