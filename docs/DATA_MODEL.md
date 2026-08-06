# Data Model

## Purpose

Este documento disena conceptualmente la futura base PostgreSQL propia de Neuronas EV Lab API. No representa migraciones implementadas.

Principio de ownership:

- Neuronas posee su propio dominio y persistencia.
- Identidades provenientes de EVAAS se almacenan como referencias externas estables.
- No debe haber foreign keys hacia bases de datos externas.
- EVAAS no escribe directamente en la base de datos de Neuronas.

## Current State

El repositorio actual no contiene modelos, base de datos ni migraciones. La unica informacion persistida esta en archivos:

- `data/personas_eda.csv`;
- notebooks bajo `notebooks/`;
- documentos bajo `docs/`.

## Target Entities

### Principal

Representa una identidad conocida por Neuronas.

Responsabilidades:

- almacenar la referencia externa estable de identidad EVAAS cuando exista;
- mantener estado local de acceso;
- desacoplar identidad externa de participacion interna en Neuronas.

Campos conceptuales:

- `id`;
- `external_identity_provider`;
- `external_principal_id`;
- `display_name`;
- `email`;
- `access_status`;
- `created_at`;
- `updated_at`.

Relaciones:

- uno a uno opcional con `StudentProfile`;
- uno a muchos con `Enrollment`;
- uno a muchos con `WorkspaceMember`;
- uno a muchos con `LabRun`;
- uno a muchos con `Review`.

Ownership:

- EVAAS puede proyectar identidad y estado administrativo.
- Neuronas decide como esa proyeccion habilita operaciones internas.

### StudentProfile

Perfil academico/laboratorio de un principal.

Responsabilidades:

- registrar informacion pedagogica local;
- separar identidad administrativa de progreso educativo.

Campos conceptuales:

- `id`;
- `principal_id`;
- `level`;
- `learning_goals`;
- `metadata`;
- `created_at`;
- `updated_at`.

Relaciones:

- pertenece a `Principal`;
- participa en `LearningProgress`.

### Enrollment

Matricula o habilitacion de acceso a una organizacion, cohorte, curso o modulo.

Responsabilidades:

- reflejar altas/bajas administrativas;
- habilitar o restringir acceso al laboratorio.

Campos conceptuales:

- `id`;
- `principal_id`;
- `external_organization_id`;
- `external_enrollment_id`;
- `status`;
- `starts_at`;
- `ends_at`;
- `created_at`;
- `updated_at`.

Relaciones:

- pertenece a `Principal`;
- puede habilitar progreso en `LearningModule`.

Ownership:

- EVAAS puede proyectar altas, bajas y organizacion.
- Neuronas conserva historial local y reglas de acceso.

### LearningModule

Unidad de aprendizaje dentro del laboratorio.

Responsabilidades:

- agrupar capsulas, actividades y criterios de progreso;
- permitir progresion trazable.

Campos conceptuales:

- `id`;
- `slug`;
- `title`;
- `description`;
- `status`;
- `version`;
- `created_at`;
- `updated_at`.

Relaciones:

- uno a muchos con `Capsule`;
- uno a muchos con `LearningProgress`.

### Capsule

Unidad educativa o experimental concreta.

Responsabilidades:

- describir una actividad de estudio o laboratorio;
- vincular guias, notebooks, datasets o contratos esperados.

Campos conceptuales:

- `id`;
- `learning_module_id`;
- `slug`;
- `title`;
- `description`;
- `content_ref`;
- `status`;
- `version`;
- `created_at`;
- `updated_at`.

Relaciones:

- pertenece a `LearningModule`;
- puede originar `LabRun`;
- puede ser resultado de `PromotionCandidate`.

### LearningProgress

Estado de avance de un estudiante en modulo o capsula.

Responsabilidades:

- registrar progreso educativo;
- conectar estudio, experimentos y validacion.

Campos conceptuales:

- `id`;
- `principal_id`;
- `learning_module_id`;
- `capsule_id`;
- `status`;
- `progress_percent`;
- `last_activity_at`;
- `evidence_ref`;
- `created_at`;
- `updated_at`.

Relaciones:

- pertenece a `Principal`;
- referencia `LearningModule`;
- referencia opcionalmente `Capsule`.

### Workspace

Espacio de trabajo individual o colaborativo.

Responsabilidades:

- agrupar participantes, LabRuns y artefactos;
- aislar experimentos por contexto.

Campos conceptuales:

- `id`;
- `name`;
- `description`;
- `visibility`;
- `status`;
- `created_by_principal_id`;
- `created_at`;
- `updated_at`.

Relaciones:

- uno a muchos con `WorkspaceMember`;
- uno a muchos con `LabRun`.

### WorkspaceMember

Participacion de un principal en un workspace.

Responsabilidades:

- definir rol local;
- registrar pertenencia colaborativa.

Campos conceptuales:

- `id`;
- `workspace_id`;
- `principal_id`;
- `role`;
- `status`;
- `created_at`;
- `updated_at`.

Relaciones:

- pertenece a `Workspace`;
- pertenece a `Principal`.

### LabRun

Ejecucion trazable de un experimento, notebook, script o laboratorio.

Responsabilidades:

- registrar inicio, cierre, estado, parametros y entorno;
- conectar experimento con artefactos, metricas y evidencia.

Campos conceptuales:

- `id`;
- `workspace_id`;
- `principal_id`;
- `capsule_id`;
- `source_type`;
- `source_ref`;
- `status`;
- `parameters`;
- `metrics`;
- `started_at`;
- `closed_at`;
- `created_at`;
- `updated_at`.

Relaciones:

- pertenece a `Workspace`;
- pertenece a `Principal`;
- puede pertenecer a `Capsule`;
- uno a muchos con `LabArtifact`;
- puede originar `Review`.

Estados sugeridos:

- `CREATED`;
- `RUNNING`;
- `RESULTS_RECORDED`;
- `CLOSED`;
- `FAILED`;
- `CANCELLED`.

### LabArtifact

Resultado material de un LabRun.

Responsabilidades:

- registrar archivos, codigo, metricas, notebooks ejecutados o referencias externas;
- preservar trazabilidad y checksum.

Campos conceptuales:

- `id`;
- `lab_run_id`;
- `artifact_type`;
- `name`;
- `storage_uri`;
- `checksum`;
- `version`;
- `metadata`;
- `created_at`.

Relaciones:

- pertenece a `LabRun`;
- puede participar en `Review`;
- puede originar `PromotionCandidate`.

### Review

Evaluacion tecnica o pedagogica de un LabRun o artefacto.

Responsabilidades:

- registrar decision, observaciones y evidencia;
- separar revision humana/automatizada de validacion final.

Campos conceptuales:

- `id`;
- `target_type`;
- `target_id`;
- `requested_by_principal_id`;
- `reviewed_by_principal_id`;
- `status`;
- `observations`;
- `validation_evidence`;
- `created_at`;
- `updated_at`;
- `closed_at`.

Estados sugeridos:

- `REQUESTED`;
- `IN_REVIEW`;
- `APPROVED`;
- `REJECTED`;
- `CHANGES_REQUESTED`;
- `VALIDATED`.

### PromotionCandidate

Propuesta para promover un artefacto validado a conocimiento, referencia, capsula o candidato de integracion.

Responsabilidades:

- representar una promocion potencial;
- preservar version, origen y decision.

Campos conceptuales:

- `id`;
- `source_artifact_id`;
- `source_review_id`;
- `candidate_type`;
- `title`;
- `description`;
- `status`;
- `version`;
- `evidence_ref`;
- `created_at`;
- `updated_at`.

Tipos sugeridos:

- `CONSOLIDATED_KNOWLEDGE`;
- `TECHNICAL_REFERENCE`;
- `EDUCATIONAL_CAPSULE`;
- `INTEGRATION_CANDIDATE`.

### IntegrationCandidate

Propuesta versionada y trazable para que otro sistema evalúe una integracion.

Responsabilidades:

- describir cambio propuesto para EVAAS u otro servicio receptor;
- dejar claro que no equivale a despliegue productivo.

Campos conceptuales:

- `id`;
- `promotion_candidate_id`;
- `target_system`;
- `target_component`;
- `package_ref`;
- `contract_ref`;
- `status`;
- `version`;
- `decision_ref`;
- `created_at`;
- `updated_at`.

Estados sugeridos:

- `PROPOSED`;
- `SUBMITTED`;
- `ACCEPTED_BY_RECEIVER`;
- `REJECTED_BY_RECEIVER`;
- `SUPERSEDED`;

## Relationship Summary

```text
Principal
  ├─ StudentProfile
  ├─ Enrollment
  ├─ LearningProgress
  ├─ WorkspaceMember -> Workspace
  └─ LabRun -> LabArtifact -> PromotionCandidate -> IntegrationCandidate

LearningModule
  └─ Capsule
      ├─ LearningProgress
      └─ LabRun

Review
  ├─ targets LabRun or LabArtifact
  └─ can validate source evidence for PromotionCandidate
```

## External Identity References

Para identities de EVAAS:

- guardar `external_identity_provider`;
- guardar `external_principal_id`;
- opcionalmente guardar `external_organization_id` o `external_enrollment_id`;
- no crear foreign keys fuera de Neuronas;
- usar idempotencia en endpoints de sincronizacion.

## Migration Policy

Este documento no debe generar migraciones todavia. La siguiente capsula de implementacion debera convertir este modelo conceptual en:

- entidades de dominio;
- migraciones versionadas;
- constraints internas;
- indices;
- fixtures minimos;
- tests de integridad.
