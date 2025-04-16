import os
from pathlib import Path

# Estructura de carpetas y archivos
structure = {
    "src": {
        "core": ["laberinto.py", "agente.py"],
        "core/algoritmos": ["bfs.py", "a_star.py", "__init__.py"],
        "interfaz": ["gui.py"],
        "interfaz/assets": []
    },
    "tests": ["test_laberinto.py", "test_algoritmos.py"],
    "docs": ["decisiones.md"],
    "examples": [],
    "files": [".gitignore", "requirements.txt", "LICENSE", "README.md"]
}

# Contenido básico para archivos
file_contents = {
    ".gitignore": "__pycache__/\n*.pyc\nvenv/\n.env\n",
    "requirements.txt": "pygame==2.5.2\nnetworkx==3.2.1\n",
    "LICENSE": "MIT License\n...",  # Reemplaza con una licencia completa
    "README.md": "# Laberinto Dinámico IA\n..."
}

def create_structure(base_path="."):
    for item in structure:
        if item == "files":
            continue  # Los archivos raíz se manejan aparte
        
        for folder, files in structure[item].items() if isinstance(structure[item], dict) else [(item, structure[item])]:
            full_path = Path(base_path) / folder
            os.makedirs(full_path, exist_ok=True)
            for file in files:
                (full_path / file).touch()

    # Crear archivos en la raíz
    for file in structure["files"]:
        with open(Path(base_path) / file, "w") as f:
            if file in file_contents:
                f.write(file_contents[file])

if __name__ == "__main__":
    create_structure()
    print("✅ Estructura del repositorio creada!")