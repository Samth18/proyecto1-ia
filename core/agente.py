from core.algoritmos import elegir_algoritmo, agente_atrapado, sugerir_algoritmo
from core.algoritmos.visualizacion import VisualizadorArbol

class Agente:
    def __init__(self, posicion_inicial=(1, 1)):
        self.posicion = posicion_inicial  # Posición actual del agente
        self.camino_optimo = []  # Mejor camino encontrado hasta ahora
        self.visitados = []  # Lista de celdas visitadas por el agente
        self.algoritmo_actual = None  # Algoritmo de búsqueda en uso
        self.algoritmo_manual = False  # Indica si el algoritmo fue seleccionado manualmente
        self.estado = "Esperando"  # Estado actual del agente (Esperando, Buscando, Siguiendo camino, Meta encontrada, Sin solución)
        self.pasos_sin_avance = 0  # Contador de pasos sin poder seguir el camino actual
        self.ciclos_atrapado = 0  # Contador de ciclos en los que el agente se considera atrapado
        self.ultimo_camino = None  # El camino calculado más recientemente
        self.indice_camino = 0  # Índice del paso actual en ultimo_camino
        self.historial_posiciones = [posicion_inicial]  # Registra todas las posiciones por las que pasa el agente
        self.nodo_final = None  # Nodo final del último cálculo de camino, para visualización
        self.visualizador = VisualizadorArbol()  # Instancia para visualizar el árbol de búsqueda

    def reiniciar(self, posicion_inicial):
        # Reinicia el estado del agente a sus valores iniciales.
        self.posicion = posicion_inicial
        self.camino_optimo = []
        self.visitados = []
        self.estado = "Esperando"
        self.pasos_sin_avance = 0
        self.ciclos_atrapado = 0
        self.ultimo_camino = None
        self.indice_camino = 0
        self.historial_posiciones = [posicion_inicial]
        self.nodo_final = None
        self.visualizador.limpiar()
        # No se reinicia el algoritmo actual ni la bandera de selección manual

    def actuar(self, laberinto):
        # Define el comportamiento del agente en cada paso.
        # Si el agente no está buscando o siguiendo un camino, no hace nada
        if self.estado not in ["Buscando", "Siguiendo camino"]:
            return False

        # Marca la posición actual como visitada
        if self.posicion not in self.visitados:
            self.visitados.append(self.posicion)

        # Comprueba si ha llegado a la meta
        if self.posicion == laberinto.meta:
            self.estado = "Meta encontrada"
            return True

        # Determina si necesita recalcular el camino
        # Esto ocurre si no hay camino, se completó el camino actual, o lleva varios pasos sin avanzar
        necesita_recalcular = (self.ultimo_camino is None or
                              self.indice_camino >= len(self.ultimo_camino) or
                              self.pasos_sin_avance >= 3)

        if necesita_recalcular:
            # Si el algoritmo no fue seleccionado manualmente, puede cambiar automáticamente
            if not self.algoritmo_manual:
                # Evalúa si el agente está en una situación difícil (pocas salidas)
                if agente_atrapado(laberinto, self.posicion):
                    self.ciclos_atrapado += 1
                    # Si lleva varios ciclos atrapado, sugiere un cambio de algoritmo
                    if self.ciclos_atrapado >= 2:
                        self.algoritmo_actual = sugerir_algoritmo(self.algoritmo_actual, "atrapado")
                        self.ciclos_atrapado = 0 # Reinicia el contador después del cambio
                else:
                    self.ciclos_atrapado = 0 # Reinicia si ya no está atrapado
                    # Evalúa la situación general del laberinto para sugerir un algoritmo
                    situacion = laberinto.calcular_situacion(self.posicion) # Podría ser 'abierto', 'laberinto_complejo', etc.
                    algoritmo_sugerido = sugerir_algoritmo(self.algoritmo_actual, situacion)
                    if algoritmo_sugerido != self.algoritmo_actual:
                        self.algoritmo_actual = algoritmo_sugerido # Cambia al algoritmo sugerido

            # Intenta calcular un nuevo camino usando el algoritmo actual
            print(f"Calculando camino con: {self.algoritmo_actual}")
            camino, nodos_generados, nodo_final = elegir_algoritmo(
                laberinto, self.posicion, laberinto.meta, self.algoritmo_actual
            )

            # Guarda el nodo final para la visualización del árbol
            self.nodo_final = nodo_final

            # Actualiza la visualización del árbol de búsqueda usando el nodo final
            # Guarda el algoritmo usado para que el visualizador sepa cómo colorear
            self.visualizador.ultimo_algoritmo = self.algoritmo_actual
            self.visualizador.construir_arbol_desde_nodo(nodo_final)

            # Actualiza la lista de visitados con los nodos explorados por el algoritmo
            for nodo_estado in nodos_generados: # Asumiendo que nodos_generados contiene estados o nodos con .estado
                estado_a_visitar = nodo_estado.estado if hasattr(nodo_estado, 'estado') else nodo_estado
                if estado_a_visitar not in self.visitados:
                    self.visitados.append(estado_a_visitar)

            # Si el algoritmo actual no encontró camino, intenta con otros algoritmos como respaldo
            if camino is None:
                print(f"Algoritmo {self.algoritmo_actual} no encontró camino. Probando alternativas...")
                # Define un orden de prueba para los algoritmos de respaldo
                algoritmos_respaldo = ["BFS", "DFS", "A*", "IDS"]
                # Elimina el algoritmo actual de la lista de respaldo para no repetirlo
                if self.algoritmo_actual in algoritmos_respaldo:
                    algoritmos_respaldo.remove(self.algoritmo_actual)

                # Prueba cada algoritmo de respaldo hasta encontrar uno que funcione
                for algo_respaldo in algoritmos_respaldo:
                    print(f"Probando algoritmo alternativo: {algo_respaldo}")
                    camino, nodos_generados, nodo_final = elegir_algoritmo(
                        laberinto, self.posicion, laberinto.meta, algo_respaldo
                    )
                    if camino:
                        # Si un algoritmo de respaldo funciona, actualiza el algoritmo actual y el nodo final
                        self.algoritmo_actual = algo_respaldo
                        self.nodo_final = nodo_final
                        print(f"Éxito con algoritmo de respaldo: {algo_respaldo}")
                        # Actualiza la visualización con los resultados del algoritmo de respaldo
                        # Guarda el algoritmo usado para que el visualizador sepa cómo colorear
                        self.visualizador.ultimo_algoritmo = self.algoritmo_actual
                        self.visualizador.construir_arbol_desde_nodo(nodo_final)
                        # Actualiza visitados con los nodos del algoritmo de respaldo
                        for nodo_estado in nodos_generados:
                            estado_a_visitar = nodo_estado.estado if hasattr(nodo_estado, 'estado') else nodo_estado
                            if estado_a_visitar not in self.visitados:
                                self.visitados.append(estado_a_visitar)
                        break # Sale del bucle de respaldo al encontrar un camino

            # Si se encontró un camino (ya sea con el algoritmo principal o uno de respaldo)
            if camino:
                self.ultimo_camino = camino # Actualiza el camino a seguir
                self.indice_camino = 1  # Empieza desde el segundo paso (el primero es la posición actual)
                self.pasos_sin_avance = 0 # Reinicia el contador de pasos sin avance
                self.estado = "Siguiendo camino" # Cambia el estado del agente
                # Considera este nuevo camino como el óptimo encontrado hasta ahora
                self.camino_optimo = camino
            else:
                # Si ningún algoritmo encontró camino, marca como sin solución
                print("No se encontró solución con ningún algoritmo.")
                self.estado = "Sin solución"
                return False # Indica que no se pudo actuar

        # Si el agente está siguiendo un camino válido
        if self.estado == "Siguiendo camino" and self.indice_camino < len(self.ultimo_camino):
            siguiente_pos = self.ultimo_camino[self.indice_camino]

            # Verifica si la siguiente celda en el camino sigue siendo válida (podría haber cambiado el laberinto)
            fila, col = siguiente_pos
            if (0 <= fila < laberinto.filas and 0 <= col < laberinto.columnas and
                laberinto.grid[fila][col] == 0):
                # Si es válida, mueve al agente a la siguiente posición
                self.posicion = siguiente_pos
                self.historial_posiciones.append(siguiente_pos) # Registra el movimiento
                self.indice_camino += 1 # Avanza al siguiente paso del camino
                self.pasos_sin_avance = 0 # Reinicia el contador
            else:
                # Si la siguiente celda ya no es válida, incrementa el contador de pasos sin avance
                # Esto forzará un recálculo en la próxima iteración
                self.pasos_sin_avance += 1
                self.ultimo_camino = None # Invalida el camino actual

        return True # Indica que el agente actuó

    def cambiar_algoritmo(self, nuevo_algoritmo):
        # Permite cambiar manualmente el algoritmo de búsqueda.
        # Verifica que el algoritmo sea uno de los válidos
        if nuevo_algoritmo in ["BFS", "DFS", "A*", "IDS"]:
            self.algoritmo_actual = nuevo_algoritmo
            self.algoritmo_manual = True  # Marca que la selección fue manual (desactiva el cambio automático)
            # Fuerza un recálculo del camino en la próxima llamada a actuar()
            self.ultimo_camino = None
            self.pasos_sin_avance = 3 # Fuerza el recálculo inmediato
            print(f"Algoritmo cambiado manualmente a: {nuevo_algoritmo}")
            return True
        print(f"Error: Algoritmo '{nuevo_algoritmo}' no válido.")
        return False

    def obtener_superficie_arbol(self):
        # Devuelve la superficie de Pygame con la visualización del árbol de búsqueda        # Llama al método del visualizador para obtener la imagen actualizada del árbol
        return self.visualizador.obtener_superficie()
