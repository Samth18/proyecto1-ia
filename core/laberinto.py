import random
import numpy as np
from collections import deque

class Laberinto:
    def __init__(self, filas, columnas, densidad_paredes=0.3):
        self.filas = filas
        self.columnas = columnas
        self.grid = [[0 for _ in range(columnas)] for _ in range(filas)]
        self.densidad_paredes = densidad_paredes
        
        # Posición inicial del agente y la meta
        self.inicio = (1, 1)
        self.meta = (filas-2, columnas-2)
        
        # Inicializar laberinto
        self.generar_laberinto()
    
    def generar_laberinto(self):
        """Genera un laberinto aleatorio asegurando que haya un camino desde inicio a meta."""
        # Limpiar el grid
        self.grid = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        
        # Añadir paredes en el borde
        for i in range(self.filas):
            self.grid[i][0] = 1
            self.grid[i][self.columnas-1] = 1
        for j in range(self.columnas):
            self.grid[0][j] = 1
            self.grid[self.filas-1][j] = 1
        
        # Añadir paredes aleatorias en el interior
        for i in range(1, self.filas-1):
            for j in range(1, self.columnas-1):
                if (i, j) != self.inicio and (i, j) != self.meta:
                    if random.random() < self.densidad_paredes:
                        self.grid[i][j] = 1
        
        # Asegurar que hay un camino desde inicio a meta
        self.asegurar_camino()
    
    def asegurar_camino(self):
        """Asegura que existe un camino desde inicio a meta utilizando BFS."""
        visitados = set()
        cola = deque([self.inicio])
        visitados.add(self.inicio)
        
        encontrado = False
        
        while cola and not encontrado:
            actual = cola.popleft()
            if actual == self.meta:
                encontrado = True
                break
            
            # Explorar vecinos
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = actual[0] + dx, actual[1] + dy
                if (0 <= nx < self.filas and 0 <= ny < self.columnas and 
                    self.grid[nx][ny] == 0 and (nx, ny) not in visitados):
                    visitados.add((nx, ny))
                    cola.append((nx, ny))
        
        # Si no hay camino, eliminar algunas paredes
        if not encontrado:
            self.eliminar_paredes_aleatorias(20)  # Eliminar varias paredes
            self.asegurar_camino()  # Verificar de nuevo
    
    def eliminar_paredes_aleatorias(self, n):
        """Elimina n paredes aleatorias del laberinto."""
        paredes = []
        for i in range(1, self.filas-1):
            for j in range(1, self.columnas-1):
                if self.grid[i][j] == 1:
                    paredes.append((i, j))
        
        n = min(n, len(paredes))
        for _ in range(n):
            if paredes:
                i, j = random.choice(paredes)
                paredes.remove((i, j))
                self.grid[i][j] = 0
    
    def mover_meta(self):
        """Mueve la meta a una posición aleatoria válida."""
        posiciones_validas = []
        for i in range(1, self.filas-1):
            for j in range(1, self.columnas-1):
                if self.grid[i][j] == 0 and (i, j) != self.inicio and (i, j) not in self.get_paredes_adyacentes(self.inicio):
                    posiciones_validas.append((i, j))
        
        if posiciones_validas:
            self.meta = random.choice(posiciones_validas)
        # Si no hay posiciones válidas, no mover la meta
    
    def get_paredes_adyacentes(self, posicion):
        """Obtiene las posiciones adyacentes que son paredes."""
        fila, col = posicion
        adyacentes = []
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = fila + dx, col + dy
            if 0 <= nx < self.filas and 0 <= ny < self.columnas and self.grid[nx][ny] == 1:
                adyacentes.append((nx, ny))
        
        return adyacentes
    
    def cambiar_paredes_aleatorias(self, n=3):
        """Cambia aleatoriamente n paredes en el laberinto (añade o elimina)."""
        for _ in range(n):
            # 50% de probabilidad de añadir o eliminar
            if random.random() < 0.5:
                # Añadir pared
                posiciones_validas = []
                for i in range(1, self.filas-1):
                    for j in range(1, self.columnas-1):
                        if (self.grid[i][j] == 0 and (i, j) != self.inicio 
                            and (i, j) != self.meta):
                            posiciones_validas.append((i, j))
                
                if posiciones_validas:
                    i, j = random.choice(posiciones_validas)
                    self.grid[i][j] = 1
            else:
                # Eliminar pared
                paredes = []
                for i in range(1, self.filas-1):
                    for j in range(1, self.columnas-1):
                        if self.grid[i][j] == 1:
                            paredes.append((i, j))
                
                if paredes:
                    i, j = random.choice(paredes)
                    self.grid[i][j] = 0
        
        # Asegurar que sigue habiendo un camino
        self.asegurar_camino()
    
    def calcular_situacion(self, posicion):
        """Calcula la situación actual del laberinto desde la posición dada."""
        # Contar espacios libres alrededor
        espacios_libres = 0
        fila, col = posicion
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nx, ny = fila + dx, col + dy
            if 0 <= nx < self.filas and 0 <= ny < self.columnas and self.grid[nx][ny] == 0:
                espacios_libres += 1
        
        # Verificar si estamos en un pasillo o espacio abierto
        if espacios_libres <= 2:
            return "atrapado"
        elif espacios_libres >= 6:
            return "abierto"
        else:
            return "laberinto_complejo"
