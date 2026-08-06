# API Contracts

## Purpose

Este documento define contratos HTTP v1 objetivo para Neuronas EV Lab API. No hay endpoints implementados actualmente en el repositorio.

## Contract Principles

- Versionar todas las rutas bajo `/api/v1`.
- Usar autenticacion explicita por cliente.
- Usar `Idempotency-Key` en operaciones de creacion o sincronizacion que puedan repetirse.
- Usar referencias externas estables para identities EVAAS.
- No exponer acceso directo a base de datos.
- No permitir que artefactos experimentales pasen automaticamente a produccion.
- Mantener `VALIDATED != PRODUCTION`.

## Authentication

Esquemas objetivo:

- EVAAS -> Neuronas: service token o JWT firmado por EVAAS, con audience de Neuronas.
- Colab -> Neuronas: token temporal de laboratorio asociado a `Principal`, `Workspace` y scope limitado.
- Usuarios/lab clients -> Neuronas: token de usuario o sesion delegada desde el proveedor admitido.

Headers comunes:

```http
Authorization: Bearer <token>
Content-Type: application/json
Idempotency-Key: <stable-operation-key>
```

## Common Response Shape

Exito:

```json
{
  "data": {},
  "meta": {
    "request_id": "req_..."
  }
}
```

Error:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request payload.",
    "details": {}
  },
  "meta": {
    "request_id": "req_..."
  }
}
```

Codigos base:

- `400 validation_error`;
- `401 unauthorized`;
- `403 forbidden`;
- `404 not_found`;
- `409 conflict`;
- `422 semantic_error`;
- `429 rate_limited`;
- `500 internal_error`.

## EVAAS Administration -> Neuronas

### Sync Principal Projection

```http
PUT /api/v1/admin/principals/{external_principal_id}
```

Uso:

- crear o actualizar la proyeccion local de una identidad administrada por EVAAS;
- operacion idempotente.

Request:

```json
{
  "provider": "evaas",
  "display_name": "Student Name",
  "email": "student@example.com",
  "access_status": "ACTIVE",
  "organization_refs": [
    {
      "external_organization_id": "org_123",
      "role": "student"
    }
  ]
}
```

Response:

```json
{
  "data": {
    "principal_id": "prn_123",
    "external_principal_id": "evaas_user_123",
    "access_status": "ACTIVE"
  }
}
```

### Administrative Activation

```http
POST /api/v1/admin/principals/{principal_id}/activate
```

Activa acceso local segun una decision administrativa externa.

### Administrative Deactivation

```http
POST /api/v1/admin/principals/{principal_id}/deactivate
```

Desactiva acceso local sin eliminar historial, LabRuns ni artefactos.

### Sync Organization Projection

```http
PUT /api/v1/admin/organizations/{external_organization_id}
```

Proyecta datos minimos de una organizacion EVAAS.

### Upsert Enrollment

```http
PUT /api/v1/admin/enrollments/{external_enrollment_id}
```

Request:

```json
{
  "external_principal_id": "evaas_user_123",
  "external_organization_id": "org_123",
  "status": "ACTIVE",
  "starts_at": "2026-08-06T00:00:00Z",
  "ends_at": null
}
```

### Access Status

```http
GET /api/v1/admin/principals/{principal_id}/access
```

Devuelve el estado de acceso calculado por Neuronas a partir de proyecciones, matriculas y reglas locales.

## Laboratory

### Create LabRun

```http
POST /api/v1/lab-runs
```

Request:

```json
{
  "workspace_id": "wks_123",
  "capsule_id": "cap_eda_intro",
  "source_type": "notebook",
  "source_ref": "notebooks/lab_eda_v3.ipynb",
  "parameters": {
    "dataset_ref": "data/personas_eda.csv"
  }
}
```

Response:

```json
{
  "data": {
    "lab_run_id": "run_123",
    "status": "CREATED"
  }
}
```

### Get LabRun

```http
GET /api/v1/lab-runs/{lab_run_id}
```

Devuelve estado, parametros, metricas, artefactos y eventos relevantes.

### Record Results

```http
POST /api/v1/lab-runs/{lab_run_id}/results
```

Request:

```json
{
  "status": "RESULTS_RECORDED",
  "metrics": {
    "rows_processed": 15,
    "columns_processed": 7
  },
  "summary": "EDA completed successfully."
}
```

### Register Artifact

```http
POST /api/v1/lab-runs/{lab_run_id}/artifacts
```

Request:

```json
{
  "artifact_type": "notebook",
  "name": "lab_eda_v3.executed.ipynb",
  "storage_uri": "artifact://run_123/lab_eda_v3.executed.ipynb",
  "checksum": "sha256:...",
  "metadata": {
    "runtime": "python",
    "format": "ipynb"
  }
}
```

### Close LabRun

```http
POST /api/v1/lab-runs/{lab_run_id}/close
```

Request:

```json
{
  "status": "CLOSED",
  "closed_reason": "completed"
}
```

## Colab

Un notebook externo debe usar la API como cliente remoto. No debe conectarse a PostgreSQL ni acceder a secretos internos.

### 1. Authenticate

```http
POST /api/v1/colab/sessions
```

Intercambia una credencial admitida por un token temporal con scopes limitados.

### 2. Create Run

```http
POST /api/v1/lab-runs
```

El notebook crea un LabRun antes de ejecutar el experimento.

### 3. Execute Experiment

La ejecucion ocurre dentro de Colab. Neuronas no asume control directo del runtime externo.

### 4. Record Metrics

```http
POST /api/v1/lab-runs/{lab_run_id}/results
```

El notebook registra metricas parciales o finales.

### 5. Send Artifacts

```http
POST /api/v1/lab-runs/{lab_run_id}/artifacts
```

El notebook sube o referencia notebook ejecutado, codigo, salida, imagenes, datasets derivados o reportes.

### 6. Close Run

```http
POST /api/v1/lab-runs/{lab_run_id}/close
```

El notebook cierra el run con estado final.

## Review

### Request Review

```http
POST /api/v1/reviews
```

Request:

```json
{
  "target_type": "LabArtifact",
  "target_id": "art_123",
  "review_type": "technical",
  "notes": "Please validate transformation logic and reproducibility."
}
```

### Approve Review

```http
POST /api/v1/reviews/{review_id}/approve
```

### Reject Review

```http
POST /api/v1/reviews/{review_id}/reject
```

### Add Observations

```http
POST /api/v1/reviews/{review_id}/observations
```

Request:

```json
{
  "observations": "Dataset transformation is reproducible, but needs automated test evidence."
}
```

### Validation Evidence

```http
POST /api/v1/reviews/{review_id}/validation-evidence
```

Request:

```json
{
  "evidence_type": "test_report",
  "evidence_ref": "artifact://run_123/test-report.json",
  "result": "PASSED"
}
```

## Promotion

### Create Promotion Candidate

```http
POST /api/v1/promotion-candidates
```

Request:

```json
{
  "source_artifact_id": "art_123",
  "source_review_id": "rev_123",
  "candidate_type": "TECHNICAL_REFERENCE",
  "title": "EDA city normalization reference",
  "description": "Validated transformation pattern for city normalization."
}
```

Un artefacto validado puede transformarse en:

1. conocimiento consolidado;
2. referencia tecnica;
3. nueva capsula educativa;
4. candidato de integracion Python para EVAAS.

### Create Integration Candidate

```http
POST /api/v1/integration-candidates
```

Request:

```json
{
  "promotion_candidate_id": "pc_123",
  "target_system": "EVAAS",
  "target_component": "analytics-python",
  "package_ref": "artifact://pc_123/package.zip",
  "contract_ref": "docs/contracts/API_CONTRACTS.md#promotion"
}
```

`VALIDATED != PRODUCTION`: este endpoint solo propone una integracion. El sistema receptor decide si acepta, rechaza, modifica o posterga.

## Idempotency

Operaciones que deben aceptar `Idempotency-Key`:

- sync principal;
- sync organization;
- upsert enrollment;
- create LabRun;
- record results;
- register artifact;
- close LabRun;
- request review;
- create promotion candidate;
- create integration candidate.

El servidor debe devolver la misma respuesta logica para reintentos equivalentes y `409 conflict` cuando una misma clave idempotente se reutilice con payload incompatible.

## Versioning

- La version publica inicial sera `/api/v1`.
- Cambios incompatibles requieren nueva version mayor de ruta.
- Cambios compatibles pueden agregarse sin romper clientes.
- Payloads deben incluir campos nuevos como opcionales hasta una version mayor.

## Authorization Rules

Reglas objetivo:

- un token EVAAS administrativo solo puede operar rutas `/admin`;
- un token Colab solo puede operar LabRuns y artefactos dentro de sus scopes;
- un usuario solo puede consultar workspaces donde sea miembro;
- reviewers requieren permisos explicitos;
- promotion e integration candidates requieren rol autorizado.

## Open Implementation Decisions

Pendiente para futuras capsulas:

- framework HTTP;
- formato exacto de tokens;
- almacenamiento fisico de artefactos;
- esquema de eventos/auditoria;
- convencion final de IDs;
- politica de retencion de runs y artefactos.
