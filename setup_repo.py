import os
from pathlib import Path

# Estructura de carpetas y archivos actualizada
structure = {
    "core": {
        "": ["__init__.py", "agente.py", "laberinto.py"],
        "algoritmos": ["__init__.py", "busqueda.py", "visualizacion.py"]
    },
    "interfaz": ["__init__.py", "gui.py"],
    "interfaz/assets": [],
    "tests": ["test_laberinto.py", "test_algoritmos.py", "test_visualizacion.py"],
    "docs": ["decisiones.md"],
    "examples": [],
    "files": [".gitignore", "requirements.txt", "LICENSE", "README.md", "main.py"]
}

# Contenido básico para archivos
file_contents = {
    ".gitignore": "__pycache__/\n*.pyc\nvenv/\n.env\n.vscode/\n.idea/\n",
    "requirements.txt": "pygame==2.5.2\nnetworkx==3.2.1\nmatplotlib==3.8.2\nnumpy==1.26.2\n",
    "LICENSE": "MIT License\n...",  # Reemplaza con una licencia completa
    "README.md": "# Laberinto Dinámico con Agente Inteligente\n\nEste proyecto implementa un sistema donde un agente inteligente debe navegar por un laberinto dinámico...",
    "main.py": """#!/usr/bin/env python3
\"\"\"
Laberinto Dinámico con Agente Inteligente
=========================================

Este proyecto implementa un sistema donde un agente inteligente debe navegar por
un laberinto dinámico (que cambia durante la ejecución) utilizando diferentes
algoritmos de búsqueda (BFS, DFS, A*) y la capacidad de cambiar dinámicamente
entre ellos según las condiciones del entorno.

Uso:
    python main.py
\"\"\"

from interfaz.gui import main

if __name__ == "__main__":
    main()
"""
}

def create_structure(base_path="."):
    for item, contents in structure.items():
        if item == "files":
            continue  # Los archivos raíz se manejan aparte
        
        if isinstance(contents, dict):
            # Es una carpeta con subcarpetas
            for subfolder, files in contents.items():
                if subfolder == "":  # archivos en la carpeta principal
                    full_path = Path(base_path) / item
                else:
                    full_path = Path(base_path) / item / subfolder
                
                os.makedirs(full_path, exist_ok=True)
                
                for file in files:
                    file_path = full_path / file
                    file_path.touch()
                    print(f"Creado: {file_path}")
        else:
            # Es una carpeta con archivos
            full_path = Path(base_path) / item
            os.makedirs(full_path, exist_ok=True)
            
            for file in contents:
                file_path = full_path / file
                file_path.touch()
                print(f"Creado: {file_path}")

    # Crear archivos en la raíz
    for file in structure["files"]:
        file_path = Path(base_path) / file
        with open(file_path, "w") as f:
            if file in file_contents:
                f.write(file_contents[file])
        print(f"Creado: {file_path}")

if __name__ == "__main__":
    create_structure()
    print("✅ Estructura del repositorio creada!")