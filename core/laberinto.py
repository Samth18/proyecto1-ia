import random
from collections import deque # Importa deque para implementar colas eficientes, usado en asegurar_camino (BFS)

class Laberinto:
    def __init__(self, filas, columnas, densidad_paredes=0.3):
        self.filas = filas
        self.columnas = columnas
        # Representa el laberinto como una matriz 2D (0: camino, 1: pared)
        self.grid = [[0 for _ in range(columnas)] for _ in range(filas)]
        self.densidad_paredes = densidad_paredes # Proporción de paredes a generar

        # Posición inicial fija y meta inicial
        self.inicio = (1, 1)
        self.meta = (filas-2, columnas-2)

        # Control para el modo dinámico que sugiere algoritmos
        self.modo_dinamico_algoritmos = False
        # Contador para la frecuencia de cambios dinámicos
        self.contador_dinamico = 5

        # Genera la estructura inicial del laberinto
        self.generar_laberinto()

    def generar_laberinto(self):
        """Genera un laberinto aleatorio asegurando que haya un camino desde inicio a meta."""
        # Reinicia el grid
        self.grid = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]

        # Crea los bordes exteriores como paredes
        for i in range(self.filas):
            self.grid[i][0] = 1
            self.grid[i][self.columnas-1] = 1
        for j in range(self.columnas):
            self.grid[0][j] = 1
            self.grid[self.filas-1][j] = 1

        # Añade paredes internas aleatoriamente según la densidad
        for i in range(1, self.filas-1):
            for j in range(1, self.columnas-1):
                # No colocar paredes en el inicio ni en la meta
                if (i, j) != self.inicio and (i, j) != self.meta:
                    if random.random() < self.densidad_paredes:
                        self.grid[i][j] = 1

        # Verifica y garantiza que exista al menos un camino a la meta
        self.asegurar_camino()

    def asegurar_camino(self):
        """Asegura que existe un camino desde inicio a meta utilizando BFS."""
        # Usa Búsqueda en Amplitud (BFS) para verificar conectividad
        visitados = set()
        cola = deque([self.inicio])
        visitados.add(self.inicio)

        encontrado = False

        while cola and not encontrado:
            actual = cola.popleft()
            if actual == self.meta:
                encontrado = True
                break

            # Explora vecinos (arriba, abajo, izquierda, derecha)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = actual[0] + dx, actual[1] + dy
                # Verifica si el vecino es válido (dentro de límites, es camino, no visitado)
                if (0 <= nx < self.filas and 0 <= ny < self.columnas and
                    self.grid[nx][ny] == 0 and (nx, ny) not in visitados):
                    visitados.add((nx, ny))
                    cola.append((nx, ny))

        # Si BFS no encontró la meta, el camino está bloqueado
        if not encontrado:
            # Elimina algunas paredes aleatoriamente para intentar abrir un camino
            self.eliminar_paredes_aleatorias(20) # Intenta eliminar hasta 20 paredes
            self.asegurar_camino() # Llama recursivamente para verificar de nuevo

    def eliminar_paredes_aleatorias(self, n):
        """Elimina n paredes aleatorias del interior del laberinto."""
        paredes = []
        # Recolecta todas las posiciones de paredes internas
        for i in range(1, self.filas-1):
            for j in range(1, self.columnas-1):
                if self.grid[i][j] == 1:
                    paredes.append((i, j))

        # Elimina hasta n paredes o todas las que haya si son menos de n
        n = min(n, len(paredes))
        for _ in range(n):
            if paredes:
                i, j = random.choice(paredes)
                paredes.remove((i, j)) # Evita elegir la misma pared dos veces
                self.grid[i][j] = 0 # Convierte la pared en camino

    def mover_meta(self):
        """Mueve la meta a una posición aleatoria válida (camino libre)."""
        posiciones_validas = []
        # Busca todas las celdas de camino que no sean el inicio ni adyacentes a él
        for i in range(1, self.filas-1):
            for j in range(1, self.columnas-1):
                if self.grid[i][j] == 0 and (i, j) != self.inicio and (i, j) not in self.get_paredes_adyacentes(self.inicio):
                    posiciones_validas.append((i, j))

        if posiciones_validas:
            self.meta = random.choice(posiciones_validas)
        # Si no hay posiciones válidas (raro), la meta no se mueve

    def get_paredes_adyacentes(self, posicion):
        """Obtiene las posiciones adyacentes a una dada que son paredes."""
        fila, col = posicion
        adyacentes = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = fila + dx, col + dy
            # Verifica límites y si es pared
            if 0 <= nx < self.filas and 0 <= ny < self.columnas and self.grid[nx][ny] == 1:
                adyacentes.append((nx, ny))
        return adyacentes

    def cambiar_paredes_aleatorias(self, n=3):
        """Cambia aleatoriamente n celdas (añade o elimina paredes)."""
        for _ in range(n):
            # Decide aleatoriamente si añadir o eliminar una pared
            if random.random() < 0.5:
                # Intenta añadir una pared en una celda de camino válida
                posiciones_validas = []
                for i in range(1, self.filas-1):
                    for j in range(1, self.columnas-1):
                        # Solo en celdas de camino que no sean inicio ni meta
                        if (self.grid[i][j] == 0 and (i, j) != self.inicio
                            and (i, j) != self.meta):
                            posiciones_validas.append((i, j))
                if posiciones_validas:
                    i, j = random.choice(posiciones_validas)
                    self.grid[i][j] = 1 # Convierte camino en pared
            else:
                # Intenta eliminar una pared existente
                paredes = []
                for i in range(1, self.filas-1):
                    for j in range(1, self.columnas-1):
                        if self.grid[i][j] == 1:
                            paredes.append((i, j))
                if paredes:
                    i, j = random.choice(paredes)
                    self.grid[i][j] = 0 # Convierte pared en camino

        # Después de cambiar paredes, siempre asegura que el camino a la meta siga existiendo
        self.asegurar_camino()

    def calcular_situacion(self, posicion):
        """Evalúa el entorno local del agente para determinar si está 'atrapado', en un 'espacio abierto' o en un 'laberinto complejo'."""
        # Cuenta cuántas celdas libres hay en las 8 direcciones adyacentes
        espacios_libres = 0
        fila, col = posicion
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nx, ny = fila + dx, col + dy
            if 0 <= nx < self.filas and 0 <= ny < self.columnas and self.grid[nx][ny] == 0:
                espacios_libres += 1

        # Clasifica la situación basada en el número de espacios libres
        if espacios_libres <= 2: # Pocas salidas, posiblemente un pasillo estrecho
            return "atrapado"
        elif espacios_libres >= 6: # Muchas salidas, espacio abierto
            return "abierto"
        else: # Situación intermedia
            return "laberinto_complejo"

    def randomizar_meta(self, posicion_agente_actual):
        """Elige una nueva posición aleatoria para la meta."""
        posibles_metas = []
        # Busca todas las celdas de camino válidas que no sean inicio, meta actual o posición del agente
        for r in range(self.filas):
            for c in range(self.columnas):
                if self.grid[r][c] == 0 and \
                   (r, c) != self.inicio and \
                   (r, c) != self.meta and \
                   (r, c) != posicion_agente_actual:
                    posibles_metas.append((r, c))

        if not posibles_metas:
            # Si no hay opciones, no cambia la meta
            print("Advertencia: No se encontraron posiciones válidas para la nueva meta.")
            return

        # Elige aleatoriamente una de las posiciones válidas
        self.meta = random.choice(posibles_metas)
        print(f"Laberinto: Meta actualizada a {self.meta}")

    def sugerir_algoritmo(self, situacion_actual):
        """Sugiere un algoritmo basado en la situación local del agente."""
        if situacion_actual == "atrapado":
            # Si está atrapado, sugiere algoritmos de profundidad (DFS o IDS) para salir rápido
            return random.choice(["DFS", "IDS"])
        elif situacion_actual == "abierto":
            # En espacios abiertos, A* suele ser eficiente por su heurística
            return "A*"
        else: # laberinto_complejo
            # En zonas complejas, BFS garantiza el camino más corto (en pasos)
            return "BFS"

    def cambiar_modo_dinamico_algoritmos(self):
        """Activa o desactiva el modo dinámico que sugiere algoritmos."""
        self.modo_dinamico_algoritmos = not self.modo_dinamico_algoritmos
        self.contador_dinamico = 5 # Reinicia el contador al cambiar de modo
        return self.modo_dinamico_algoritmos

    def decrementar_contador_dinamico(self):
        """Decrementa el contador para cambios dinámicos. Retorna True si llega a cero."""
        if not self.modo_dinamico_algoritmos:
            return False # No hace nada si el modo está desactivado

        self.contador_dinamico -= 1
        if self.contador_dinamico <= 0:
            self.contador_dinamico = 5 # Reinicia el contador para el próximo ciclo
            return True # Indica que es momento de realizar cambios dinámicos
        return False

    def actualizar_dinamico_con_algoritmos(self, posicion_agente):
        """Realiza cambios dinámicos en el laberinto y sugiere un algoritmo."""
        resultado = {
            'meta_cambiada': False,
            'paredes_cambiadas': 0,
            'algoritmo_sugerido': None
        }

        if not self.modo_dinamico_algoritmos:
            return resultado # No hace nada si el modo está desactivado

        # Evalúa la situación actual del agente
        situacion = self.calcular_situacion(posicion_agente)

        # Cambia más paredes si el agente está atrapado para intentar abrir caminos
        num_paredes = 8 if situacion == "atrapado" else 5
        self.cambiar_paredes_aleatorias(num_paredes)
        resultado['paredes_cambiadas'] = num_paredes

        # Aumenta la probabilidad de cambiar la meta, especialmente si está atrapado
        debe_cambiar_meta = (
            situacion == "atrapado" or
            random.random() < 0.5 # 50% de probabilidad en otros casos
        )

        if debe_cambiar_meta:
            # Intenta colocar la meta en una posición que favorezca un cambio de algoritmo
            self.randomizar_meta_estrategica(posicion_agente)
            resultado['meta_cambiada'] = True
            print("Meta randomizada estratégicamente para forzar cambio de algoritmo")

        # Sugiere un algoritmo basado en la situación actual
        resultado['algoritmo_sugerido'] = self.sugerir_algoritmo(situacion)

        return resultado

    def randomizar_meta_estrategica(self, posicion_agente_actual):
        """Intenta colocar la meta en una posición que desafíe al algoritmo actual."""
        posibles_metas = []
        posiciones_distantes = [] # Guarda posiciones lejanas al agente

        # Recorre todas las celdas válidas
        for r in range(self.filas):
            for c in range(self.columnas):
                if self.grid[r][c] == 0 and \
                   (r, c) != self.inicio and \
                   (r, c) != self.meta and \
                   (r, c) != posicion_agente_actual:
                    posibles_metas.append((r, c))

                    # Calcula la distancia Manhattan desde el agente
                    dist_manhattan = abs(r - posicion_agente_actual[0]) + abs(c - posicion_agente_actual[1])

                    # Marca como 'distante' si está a más de la mitad del tamaño del laberinto
                    if dist_manhattan > (self.filas + self.columnas) / 2:
                        posiciones_distantes.append((r, c))

        if posibles_metas:
            # Con alta probabilidad (70%), si hay posiciones distantes, elige una de ellas
            # Esto tiende a favorecer algoritmos con heurística como A*
            if random.random() < 0.7 and posiciones_distantes:
                self.meta = random.choice(posiciones_distantes)
                print(f"Meta colocada lejos (distancia) en {self.meta}")
            else:
                # Si no, elige cualquier posición válida aleatoriamente
                self.meta = random.choice(posibles_metas)
                print(f"Meta colocada aleatoriamente en {self.meta}")
        else:
            # Si no hay ninguna posición válida (muy raro), no cambia la meta
            print("No se encontraron posiciones válidas para la nueva meta estratégica")
