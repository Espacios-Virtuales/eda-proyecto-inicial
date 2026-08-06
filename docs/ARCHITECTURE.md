# Architecture

## Purpose

Neuronas EV Lab API debe evolucionar desde el laboratorio local actual hacia una aplicacion independiente para aprendizaje, experimentacion, colaboracion, revision, validacion y promocion controlada de conocimiento y codigo reutilizable dentro del ecosistema EVAAS.

Este documento separa el estado actual de la arquitectura objetivo. No declara como implementado ningun componente que todavia no exista en el repositorio.

## Current State

El repositorio actual contiene:

- `src/main.py`: runner local que recibe el nombre de un notebook, lo ejecuta con `jupyter nbconvert --execute --inplace` y lo convierte a script en `src/generated/`.
- `notebooks/lab_eda_v1.ipynb`: exploracion basica del dataset con `info()` y `describe()`.
- `notebooks/lab_eda_v2.ipynb`: carga e impresion del dataset completo.
- `notebooks/lab_eda_v3.ipynb`: transformacion de la columna `ciudad`.
- `data/personas_eda.csv`: dataset CSV de ejemplo.
- `requirements.txt`: dependencias para notebooks y pandas.
- `docs/`: clases, bitacoras, guia Git y esta documentacion tecnica.

No existe todavia:

- API HTTP;
- framework web;
- modelos de dominio;
- base de datos;
- migraciones;
- autenticacion;
- cola de tareas;
- almacenamiento de artefactos;
- tests automatizados;
- integracion con EVAAS;
- integracion con Google Colab;
- integracion con Liora.

## Target Architecture

La arquitectura objetivo organiza Neuronas como una aplicacion de laboratorio con dominio propio.

```text
External Clients
  ├─ EVAAS Admin/Governance
  ├─ Google Colab notebooks
  ├─ Web or CLI lab clients
  └─ Review/validation clients

HTTP API v1
  ├─ Administration contracts
  ├─ Learning contracts
  ├─ Workspace contracts
  ├─ LabRun contracts
  ├─ Review contracts
  └─ Promotion contracts

Application Domain
  ├─ Principals and profiles
  ├─ Enrollment and access projection
  ├─ Learning progress
  ├─ Workspaces and members
  ├─ LabRuns and artifacts
  ├─ Reviews and validation evidence
  └─ Promotion and integration candidates

Persistence
  ├─ Neuronas PostgreSQL database
  └─ Artifact storage reference layer
```

## Neuronas EV Lab Responsibilities

Neuronas owns:

- aprendizaje;
- laboratorios;
- experimentos;
- colaboracion;
- LabRuns;
- artefactos;
- revision;
- validacion;
- progreso;
- candidatos de promocion.

En terminos operativos, Neuronas debe:

- persistir su propio dominio;
- aceptar proyecciones administrativas externas sin ceder ownership del estado interno;
- ejecutar o registrar experimentos reproducibles;
- asociar evidencia, metricas y artefactos a LabRuns;
- mantener trazabilidad de revision y validacion;
- producir candidatos versionados, no cambios productivos automaticos.

## EVAAS Responsibilities

EVAAS owns:

- identidad;
- organizaciones;
- administracion;
- gobierno;
- permisos administrativos;
- integracion final con el ecosistema.

EVAAS puede administrar Neuronas mediante contratos HTTP autenticados y versionados. Puede proyectar principals, organizaciones, matriculas y estados de acceso, pero no debe escribir directamente sobre la base de datos de Neuronas.

## Independence Principle

Neuronas debe poder operar como aplicacion independiente, aunque pueda ser administrada y gobernada desde EVAAS mediante contratos.

Reglas obligatorias:

- Neuronas tiene persistencia propia.
- Neuronas no comparte tablas con EVAAS.
- Neuronas no usa foreign keys hacia bases de datos externas.
- Neuronas no comparte credenciales de PostgreSQL con EVAAS.
- Neuronas no accede directamente a repositories internos de EVAAS.
- EVAAS no escribe directamente en la base de datos de Neuronas.
- Toda administracion externa entra por contratos autenticados, versionados e idempotentes cuando corresponda.

## Experimentation Boundary

El codigo proveniente de notebooks nunca pasa automaticamente a servicios productivos.

Flujo requerido:

```text
Experiment -> Artifact -> Review -> Test -> Validate -> PromotionCandidate
```

Solo despues de ese flujo puede existir un `IntegrationCandidate`. El servicio receptor decide finalmente si lo integra.

## Liora Boundary

Neuronas no modifica directamente el nucleo de Liora.

Cualquier conocimiento o artefacto derivado debe ingresar mediante fronteras y contratos admitidos por el ecosistema. Si un resultado experimental es util para Liora, se representa como conocimiento validado o candidato de integracion, no como cambio directo.

## Google Colab Boundary

Google Colab debe tratarse como cliente externo. Un notebook de Colab no debe acceder a la base de datos de Neuronas ni a credenciales internas.

El flujo objetivo es:

1. obtener credenciales o token temporal;
2. crear un LabRun mediante API;
3. ejecutar el experimento en Colab;
4. registrar metricas y eventos;
5. subir o referenciar artefactos;
6. cerrar el LabRun.

## Storage

Estado actual:

- dataset versionado en Git bajo `data/`;
- notebooks versionados bajo `notebooks/`;
- scripts generados localmente en `src/generated/` cuando se ejecuta el runner.

Estado objetivo:

- PostgreSQL propio para entidades transaccionales;
- almacenamiento de artefactos mediante referencias estables;
- checksum, metadata, version y relacion con LabRun para cada artefacto;
- politica explicita para artefactos generados localmente, externos o subidos por API.

## Configuration

Estado actual:

- no hay archivo de configuracion de aplicacion;
- no hay variables de entorno documentadas;
- no hay settings por ambiente.

Estado objetivo:

- configuracion por variables de entorno;
- separacion de ambientes local, test, staging y produccion;
- secretos fuera del repositorio;
- contratos de integracion configurados explicitamente.

## Testing and Validation

Estado actual:

- no hay tests automatizados.

Estado objetivo:

- pruebas unitarias del dominio;
- pruebas de contratos HTTP;
- pruebas de integracion con PostgreSQL;
- pruebas de idempotencia;
- pruebas de ejecucion de LabRuns;
- pruebas de seguridad para boundaries EVAAS, Colab y Liora.

## Roadmap Link

La secuencia incremental esta definida en [ROADMAP.md](ROADMAP.md).
