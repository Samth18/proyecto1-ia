import heapq
import math
from collections import deque

class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo=0):
        self.estado = estado  # Tupla (fila, columna)
        self.padre = padre    # Nodo padre
        self.accion = accion  # Acción que llevó a este estado
        self.costo = costo    # Costo acumulado

    def __lt__(self, otro):
        return self.costo < otro.costo

def reconstruir_camino(nodo):
    """Reconstruye el camino desde el nodo inicial hasta el nodo actual."""
    camino = []
    while nodo:
        camino.append(nodo.estado)
        nodo = nodo.padre
    return list(reversed(camino))

def acciones_validas(estado, laberinto):
    """Obtiene las acciones válidas desde un estado."""
    fila, col = estado
    acciones = []
    
    # Posibles movimientos: arriba, derecha, abajo, izquierda
    movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    nombres = ["arriba", "derecha", "abajo", "izquierda"]
    
    for i, (df, dc) in enumerate(movimientos):
        nueva_fila, nueva_col = fila + df, col + dc
        
        # Verificar que esté dentro del laberinto
        if (0 <= nueva_fila < laberinto.filas and 
            0 <= nueva_col < laberinto.columnas and 
            laberinto.grid[nueva_fila][nueva_col] == 0):
            acciones.append((nombres[i], (nueva_fila, nueva_col)))
    
    return acciones

def distancia_manhattan(estado1, estado2):
    """Calcula la distancia Manhattan entre dos estados."""
    return abs(estado1[0] - estado2[0]) + abs(estado1[1] - estado2[1])

def bfs(laberinto, estado_inicial, meta):
    """Búsqueda en amplitud (BFS)."""
    nodo_inicial = Nodo(estado_inicial)
    if estado_inicial == meta:
        return reconstruir_camino(nodo_inicial), [estado_inicial], nodo_inicial
    
    frontera = deque([nodo_inicial])
    explorados = set()
    estados_frontera = {estado_inicial}  # Conjunto de estados en la frontera
    todos_visitados = []  # Para visualización
    
    while frontera:
        nodo = frontera.popleft()
        estados_frontera.remove(nodo.estado)  # Eliminar de frontera
        
        explorados.add(nodo.estado)
        todos_visitados.append(nodo.estado)
        
        for accion, estado in acciones_validas(nodo.estado, laberinto):
            if estado not in explorados and estado not in estados_frontera:
                hijo = Nodo(estado, nodo, accion, nodo.costo + 1)
                
                if estado == meta:
                    return reconstruir_camino(hijo), todos_visitados, hijo
                
                frontera.append(hijo)
                estados_frontera.add(estado)
    
    return None, todos_visitados, None  # No se encontró camino

def dfs(laberinto, estado_inicial, meta):
    """Búsqueda en profundidad (DFS)."""
    nodo_inicial = Nodo(estado_inicial)
    if estado_inicial == meta:
        return reconstruir_camino(nodo_inicial), [estado_inicial], nodo_inicial
    
    frontera = [nodo_inicial]  # Lista como pila
    estados_frontera = {estado_inicial}  # Conjunto de estados en la frontera
    explorados = set()
    todos_visitados = []  # Para visualización
    
    while frontera:
        nodo = frontera.pop()  # Extraer del final (LIFO)
        estados_frontera.remove(nodo.estado)  # Eliminar de frontera
        
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            todos_visitados.append(nodo.estado)
            
            if nodo.estado == meta:
                return reconstruir_camino(nodo), todos_visitados, nodo
            
            # Añadir los sucesores
            for accion, estado in acciones_validas(nodo.estado, laberinto):
                if estado not in explorados and estado not in estados_frontera:
                    hijo = Nodo(estado, nodo, accion, nodo.costo + 1)
                    frontera.append(hijo)
                    estados_frontera.add(estado)
    
    return None, todos_visitados, None  # No se encontró camino

def a_estrella(laberinto, estado_inicial, meta):
    """Algoritmo A* con heurística de distancia Manhattan."""
    nodo_inicial = Nodo(estado_inicial)
    if estado_inicial == meta:
        return reconstruir_camino(nodo_inicial), [estado_inicial], nodo_inicial
    
    # Cola de prioridad: (f-value, contador, nodo)
    contador = 0  # Para desempates
    frontera = [(distancia_manhattan(estado_inicial, meta), contador, nodo_inicial)]
    heapq.heapify(frontera)
    contador += 1
    
    # Conjunto de estados en la frontera
    estados_frontera = {estado_inicial}
    
    explorados = set()
    todos_visitados = []  # Para visualización
    
    # Mapa de costos g para los estados
    g_costo = {estado_inicial: 0}
    
    while frontera:
        _, _, nodo = heapq.heappop(frontera)
        estados_frontera.remove(nodo.estado)
        
        if nodo.estado == meta:
            return reconstruir_camino(nodo), todos_visitados, nodo
        
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            todos_visitados.append(nodo.estado)
            
            for accion, estado in acciones_validas(nodo.estado, laberinto):
                nuevo_costo = g_costo[nodo.estado] + 1
                
                if estado not in g_costo or nuevo_costo < g_costo[estado]:
                    g_costo[estado] = nuevo_costo
                    f_valor = nuevo_costo + distancia_manhattan(estado, meta)
                    hijo = Nodo(estado, nodo, accion, nuevo_costo)
                    
                    if estado not in estados_frontera:
                        heapq.heappush(frontera, (f_valor, contador, hijo))
                        estados_frontera.add(estado)
                        contador += 1
                    # Si ya está en la frontera pero con un costo mayor, actualizarlo
                    # (esto requeriría una implementación más compleja con diccionarios adicionales)
    
    return None, todos_visitados, None  # No se encontró camino

def elegir_algoritmo(laberinto, estado_actual, meta, algoritmo="A*"):
    """Selecciona y ejecuta el algoritmo de búsqueda apropiado."""
    if algoritmo == "BFS":
        return bfs(laberinto, estado_actual, meta)
    elif algoritmo == "DFS":
        return dfs(laberinto, estado_actual, meta)
    elif algoritmo == "A*":
        return a_estrella(laberinto, estado_actual, meta)
    else:
        # Por defecto, usar A* (mejor opción para la mayoría de casos)
        return a_estrella(laberinto, estado_actual, meta)

# Función para determinar si el agente está atrapado
def agente_atrapado(laberinto, estado, umbral=1):
    """Comprueba si el agente está potencialmente atrapado."""
    acciones = acciones_validas(estado, laberinto)
    return len(acciones) <= umbral  # Si hay pocas opciones, podría estar atrapado

# Función para sugerir cambio de algoritmo
def sugerir_algoritmo(algoritmo_actual, situacion):
    """Sugiere un algoritmo según la situación del laberinto."""
    if situacion == "atrapado":
        # Si está atrapado, DFS puede ser mejor para explorar salidas
        return "DFS" if algoritmo_actual != "DFS" else "BFS"
    elif situacion == "abierto":
        # En espacios abiertos, A* es más eficiente
        return "A*"
    elif situacion == "laberinto_complejo":
        # En laberintos complejos, BFS garantiza el camino más corto
        return "BFS"
    else:
        # Por defecto, A* es una buena combinación de eficiencia y optimalidad
        return "A*" 