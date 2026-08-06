# 🌒 Guía Completa · Git + GitHub en Windows

## 🜁 Instalación, configuración y primer flujo de trabajo

---

## 🧭 Propósito

Esta guía te permitirá:

* Instalar Git en Windows
* Configurar tu identidad
* Crear y conectar un repositorio en GitHub
* Ejecutar tu primer flujo completo de trabajo

---

# 🛠️ 1. Instalación de Git

## Paso 1 · Descargar

Ir a: https://git-scm.com/download/win
Descargar Git for Windows.

---

## Paso 2 · Instalar

Ejecutar el archivo `.exe` y configurar:

* Editor: Visual Studio Code (opcional)
* PATH: Git from the command line and also from 3rd-party software
* Line endings: Checkout Windows-style, commit Unix-style

---

## Paso 3 · Verificar instalación

Abrir Git Bash o terminal y ejecutar:

```bash
git --version
```

---

# 🧬 2. Configuración inicial

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

Verificar:

```bash
git config --list
```

---

# 🌐 3. Crear cuenta en GitHub

Ir a: https://github.com
Crear usuario y confirmar correo.

---

# 🜂 4. Crear repositorio

* Click en "New repository"
* Nombre: neuronas-ev-lab-api
* Activar README

---

# 🌊 5. Clonar repositorio

```bash
git clone https://github.com/tu-usuario/neuronas-ev-lab-api.git
cd neuronas-ev-lab-api
code .
```

---

# 🧱 6. Crear estructura

```bash
mkdir data notebooks src outputs
```

Crear archivos:

```bash
touch main.py README.md
```

---

# 🜁 7. Hola Mundo

Archivo `main.py`:

```python
def main():
    print("Hola, mundo 🌍")

if __name__ == "__main__":
    main()
```

Ejecutar:

```bash
python main.py
```

---

# 🜂 8. Primer commit

```bash
git add .
git commit -m "estructura inicial del proyecto"
git push
```

---

# 🌱 9. Agregar dataset

Crear archivo:

```
/data/personas_eda.csv
```

---

# 🔁 10. Segundo commit

```bash
git add .
git commit -m "agrega dataset inicial"
git push
```

---

# 🧪 11. Verificación

Revisar en GitHub:

* estructura visible
* archivos cargados
* historial de commits

---

# ⚠️ Problemas comunes

### git no reconocido

* reiniciar equipo
* revisar instalación

### error en push

* autenticar con navegador

---

# 🧬 Flujo resumido

Instalar → Configurar → Crear repo → Clonar → Trabajar → Commit → Push

---

# 🜁 Cierre

> Cada commit es memoria.
> Cada push es permanencia.
>
> Este es el inicio de tu sistema de trabajo.

---
