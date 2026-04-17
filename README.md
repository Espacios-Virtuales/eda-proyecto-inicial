# 🌱 Proyecto EDA — Primer Umbral

> “Este repositorio no es solo código.  
> Es memoria, práctica y conciencia en construcción.”

---

## 🧭 Propósito

Este proyecto nace como un espacio para:

- explorar datos
- comprender patrones
- construir pensamiento analítico
- registrar el proceso de aprendizaje

Aquí no solo se busca responder preguntas,  
sino aprender a formularlas.

---

## 🧱 Estructura del proyecto

```
eda-proyecto-inicial/
 ├─ data/           # Acceso a datasets
 │   └─ personas_eda.csv
 ├─ docs/           # Documentación de proyecto
 │   ├─ bitacoras/
 │   ├─ clases/
 │   └─ trabajos/  
 ├─ notebooks/      # Exploración (laboratorio)
 │   ├─ lab_eda.ipynb
 │   └─ lab_eda_v3.ipynb
 ├─ src/            # Código ejecutable / orquestación
 │   ├─ main.py
 │   └─ generated/  # Scripts generados desde notebooks
 ├─ requirements.txt
 ├─ LICENSE            
 └─ README.md    
```

## ⚙️ Configuración del entorno

- Crear entorno virtual

```bash
    python -m venv .venv
```

- Activar entorno

Linux / Mac
```bash
    source .venv/bin/activate
```

- Instalar Independencias
```bash
    pip install -r requirements.txt
```

## ▶️ Ejecución del proyecto

Ejecutar pipeline desde main.py

```bash
    python src/main.py lab_eda_v3.ipynb
```

Esto:

Ejecuta el notebook
Genera un .py en src/generated/

---

## 🧬 Reflexión

Este repositorio no busca perfección inmediata,  
sino trazabilidad del aprendizaje.

Cada paso, incluso el error,  
forma parte del proceso.

---

## 🜂 Conjuro del proceso

> No avanzo para terminar,  
> avanzo para comprender.  
>  
> No oculto mis errores,  
> los integro como parte del camino.  
>  
> Este proyecto crece conmigo.

---