# Neuronas EV Lab API

Laboratorio tecnico y pedagogico para experimentar, estudiar, validar y promover conocimiento y codigo reutilizable dentro del ecosistema EVAAS.

Neuronas EV Lab API evoluciona desde una linea inicial de estudio EDA hacia una API de laboratorio para aprendizaje, experimentacion, colaboracion, revision y promocion controlada de artefactos tecnicos. El repositorio todavia no implementa la API objetivo: hoy contiene notebooks, datos de ejemplo, documentacion pedagogica y un runner local para ejecutar y convertir notebooks.

## Learning Cycle

```text
Study -> Experiment -> Extract -> Review -> Test -> Validate -> Promote
```

- Study: estudiar conceptos, clases, datasets y bitacoras.
- Experiment: ejecutar notebooks y pruebas exploratorias.
- Extract: convertir resultados o codigo experimental en artefactos trazables.
- Review: someter artefactos a revision tecnica y pedagogica.
- Test: validar comportamiento esperado con pruebas reproducibles.
- Validate: marcar evidencia como validada dentro del laboratorio.
- Promote: proponer conocimiento, capsulas o candidatos de integracion hacia otros sistemas.

`VALIDATED != PRODUCTION`: un artefacto validado en Neuronas no entra automaticamente a produccion. La decision final pertenece al sistema receptor.

## Current State

El estado real del repositorio es de laboratorio local basado en notebooks:

- Python: un runner en `src/main.py`.
- Notebooks: tres notebooks EDA en `notebooks/`.
- Dataset: `data/personas_eda.csv`, con 15 registros de personas y columnas demograficas/laborales.
- Dependencias: `pandas`, `notebook`, `nbconvert`, `ipykernel`.
- Ejecucion: `src/main.py` ejecuta un notebook con `jupyter nbconvert --execute --inplace` y luego lo convierte a script en `src/generated/`.
- Documentacion: clases, bitacoras y guia Git en `docs/`.
- API HTTP: no existe todavia.
- Persistencia: no hay base de datos ni migraciones.
- Tests: no hay suite de tests en el repositorio.
- Integraciones: no hay integraciones implementadas con EVAAS, Liora, Google Colab ni servicios externos.

## Scope

Este repositorio debe convertirse en una aplicacion independiente para:

- registrar estudiantes, perfiles y avances de aprendizaje;
- administrar espacios de trabajo colaborativos;
- ejecutar y trazar LabRuns;
- almacenar artefactos generados por notebooks o experimentos;
- revisar, probar y validar evidencia;
- crear PromotionCandidates e IntegrationCandidates versionados;
- exponer contratos para administracion desde EVAAS sin compartir persistencia.

EDA es la primera linea de estudio, no el limite conceptual del proyecto.

## General Architecture

Neuronas debe operar con dominio y persistencia propios. EVAAS puede administrar y gobernar el laboratorio solo mediante contratos HTTP autenticados y versionados.

Fronteras principales:

- Neuronas EV Lab: aprendizaje, laboratorios, experimentos, colaboracion, LabRuns, artefactos, revisiones, validaciones y candidatos de promocion.
- EVAAS: identidad, organizaciones, administracion, gobierno y permisos administrativos.
- Liora: nucleo externo que no debe ser modificado directamente por Neuronas.
- Google Colab: cliente externo futuro para ejecutar notebooks y reportar runs, metricas y artefactos.

EVAAS no debe escribir directamente en la base de datos de Neuronas. Las identidades externas se guardaran como referencias estables, no como foreign keys hacia otra base de datos.

## Local Execution

Crear y activar entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar un notebook desde el runner:

```bash
python src/main.py lab_eda_v3.ipynb
```

El runner:

1. busca el notebook dentro de `notebooks/`;
2. lo ejecuta en el archivo original;
3. genera un script en `src/generated/`.

`src/generated/` es salida generada localmente y no forma parte de la arquitectura estable.

## Available Notebooks

- `notebooks/lab_eda_v1.ipynb`: carga `data/personas_eda.csv`, muestra estructura del `DataFrame` y estadisticas descriptivas.
- `notebooks/lab_eda_v2.ipynb`: carga el dataset y lo imprime completo.
- `notebooks/lab_eda_v3.ipynb`: carga el dataset, transforma `ciudad` reemplazando `Viña del Mar` por `Valparaiso` y muestra el resultado.

## Repository Structure

```text
.
├── data/
│   └── personas_eda.csv
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATA_MODEL.md
│   ├── ROADMAP.md
│   ├── bitacoras/
│   ├── clases/
│   ├── contracts/
│   │   └── API_CONTRACTS.md
│   └── works/
├── notebooks/
│   ├── lab_eda_v1.ipynb
│   ├── lab_eda_v2.ipynb
│   └── lab_eda_v3.ipynb
├── src/
│   └── main.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Google Colab

La relacion con Google Colab todavia no esta implementada. La arquitectura objetivo considera que un notebook externo pueda:

1. autenticarse contra la API;
2. crear un LabRun;
3. ejecutar un experimento;
4. registrar metricas;
5. subir o referenciar artefactos;
6. cerrar el run con estado final.

Mientras no exista la API, los notebooks se ejecutan localmente o en entornos compatibles copiando el repositorio y sus dependencias.

## Future API

La API HTTP v1 debera cubrir:

- administracion EVAAS -> Neuronas;
- principals, matriculas y estado de acceso;
- workspaces colaborativos;
- LabRuns y LabArtifacts;
- revision y validacion;
- PromotionCandidates e IntegrationCandidates;
- contratos de integracion con Colab.

Ver [API_CONTRACTS.md](docs/contracts/API_CONTRACTS.md).

## Promotion Model

El flujo de promocion esperado es:

```text
Experiment -> Artifact -> Review -> Test -> Validate -> PromotionCandidate -> IntegrationCandidate
```

Un artefacto validado puede transformarse en:

- conocimiento consolidado;
- referencia tecnica;
- nueva capsula educativa;
- candidato de integracion Python para EVAAS.

La integracion productiva requiere una decision posterior del sistema receptor.

## Relationship With EVAAS

Neuronas pertenece al ecosistema EVAAS, pero no debe compartir tablas, foreign keys, credenciales de PostgreSQL ni acceso directo a repositories internos de EVAAS.

EVAAS puede proyectar identidad, organizacion, matricula y gobierno mediante contratos autenticados. Neuronas conserva su propio modelo, auditoria y persistencia.

## Technical Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Data Model](docs/DATA_MODEL.md)
- [API Contracts](docs/contracts/API_CONTRACTS.md)
- [Roadmap](docs/ROADMAP.md)
