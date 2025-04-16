# Laberinto Dinámico con Agente Inteligente

Este proyecto implementa un sistema donde un agente inteligente debe navegar por un laberinto dinámico (que cambia durante la ejecución) utilizando diferentes algoritmos de búsqueda (BFS, DFS, A*) y la capacidad de cambiar dinámicamente entre ellos según las condiciones del entorno.

## Características

- **Laberinto Dinámico**: Las paredes y la meta pueden cambiar durante la ejecución.
- **Algoritmos de Búsqueda**: Implementa BFS, DFS y A* para encontrar caminos.
- **Adaptación Dinámica**: El agente puede cambiar automáticamente de algoritmo según la situación.
- **Interfaz Gráfica**: Visualización del laberinto, el agente y su ruta.
- **Panel de Control**: Permite controlar la ejecución, cambiar algoritmos y ajustar la velocidad.
- **Visualización de Árboles**: Muestra la estructura de árbol generada por cada algoritmo de búsqueda.

## Estructura del Proyecto

```
.
├── core/              # Núcleo de la aplicación
│   ├── __init__.py
│   ├── agente.py       # Implementación del agente inteligente
│   ├── laberinto.py    # Implementación del laberinto dinámico
│   └── algoritmos/     # Implementaciones de algoritmos de búsqueda
│       ├── __init__.py
│       ├── busqueda.py # BFS, DFS, A* y utilidades
│       └── visualizacion.py # Visualización de árboles de búsqueda
├── interfaz/           # Componentes de la interfaz gráfica
│   ├── __init__.py
│   └── gui.py          # Interfaz de usuario con Pygame
├── main.py             # Punto de entrada principal
└── README.md           # Este archivo
```

## Requisitos

- Python 3.6 o superior
- Pygame
- NetworkX
- Matplotlib
- NumPy

## Instalación

1. Clona el repositorio:
   ```
   git clone https://github.com/tu-usuario/laberinto-dinamico.git
   cd laberinto-dinamico
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Ejecuta el programa:
```
python main.py
```

### Controles

- **Iniciar/Pausar**: Comienza o pausa la simulación.
- **Reiniciar**: Reinicia el laberinto y el agente.
- **Modo Dinámico**: Activa o desactiva los cambios dinámicos en el laberinto.
- **Mostrar/Ocultar Árbol**: Activa o desactiva la visualización del árbol de búsqueda.
- **Selección de Algoritmo**: Cambia manualmente el algoritmo de búsqueda.
- **Velocidad**: Ajusta la velocidad de la simulación.

## Algoritmos de Búsqueda

### BFS (Breadth-First Search)
- Garantiza encontrar el camino más corto
- Eficiente en laberintos abiertos con pocas obstáculos
- Alto consumo de memoria

### DFS (Depth-First Search)
- Bueno para explorar profundamente en laberintos con pasillos largos
- Bajo consumo de memoria
- No garantiza el camino más corto

### A* (A-Star)
- Combina la eficiencia de búsqueda con una heurística (distancia Manhattan)
- Balance entre BFS y DFS
- Garantiza el camino óptimo si la heurística es admisible

## Adaptación Dinámica

El agente elegirá automáticamente el mejor algoritmo según la situación:

- En espacios abiertos: A* (eficiencia con optimalidad)
- En pasillos estrechos o cuando está "atrapado": DFS (exploración profunda)
- En laberintos complejos: BFS (garantía de camino más corto)

## Visualización de Árboles

El proyecto incluye la capacidad de visualizar la estructura de árbol generada por cada algoritmo de búsqueda:

- Muestra cómo el algoritmo explora el espacio de búsqueda
- Destaca el camino óptimo encontrado
- Ayuda a entender las diferencias entre los algoritmos

## Autores

César David Peñaranda Melo
Juan David Cuellar López
Joseph Herrera Libreros
Samuel Escobar Rivera 

## Licencia

=======
Este proyecto está licenciado bajo la licencia MIT - ver el archivo [LICENSE](LICENSE)  para más detalles.
