.PHONY: run clean help

run:
	python3 main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -exec rm -f {} +

all: run clean

help:
	@echo "Comandos disponibles:"
	@echo "  make run    : Ejecutar main.py"
	@echo "  make clean  : Eliminar archivos de caché"
	@echo "  make all    : Ejecutar main.py y luego limpiar"