from pathlib import Path
import subprocess
import sys


def ejecutar_y_convertir(notebook_path: Path, output_dir: Path) -> None:
    subprocess.run([
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        str(notebook_path)
    ], check=True)

    subprocess.run([
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "script",
        str(notebook_path),
        "--output-dir", str(output_dir)
    ], check=True)


def main():
    base_dir = Path(__file__).resolve().parent.parent
    notebooks_dir = base_dir / "notebooks"
    output_dir = base_dir / "src" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 👇 Aquí decides el archivo
    if len(sys.argv) < 2:
        print("Debes indicar el notebook. Ejemplo:")
        print("python src/main.py lab_eda_v3.ipynb")
        sys.exit(1)

    notebook_name = sys.argv[1]
    notebook_path = notebooks_dir / notebook_name

    if not notebook_path.exists():
        raise FileNotFoundError(f"No existe: {notebook_path}")

    print(f"Procesando: {notebook_name}")
    ejecutar_y_convertir(notebook_path, output_dir)

    print("Proceso completado.")


if __name__ == "__main__":
    main()