from core.algoritmos import elegir_algoritmo, agente_atrapado, sugerir_algoritmo
from core.algoritmos import VisualizadorArbol

class Agente:
    def __init__(self, posicion_inicial=(1, 1)):
        self.posicion = posicion_inicial
        self.camino_optimo = []
        self.visitados = []
        self.algoritmo_actual = None  # Iniciar sin algoritmo
        self.algoritmo_manual = False  # Nueva bandera
        self.estado = "Esperando"
        self.pasos_sin_avance = 0
        self.ciclos_atrapado = 0
        self.ultimo_camino = None
        self.indice_camino = 0
        self.historial_posiciones = [posicion_inicial]
        self.nodo_final = None
        self.visualizador = VisualizadorArbol()
    
    def reiniciar(self, posicion_inicial):
        """Reinicia el estado del agente."""
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
        # No reiniciar self.algoritmo_actual ni self.algoritmo_manual
    
    def actuar(self, laberinto):
        """Actúa según el estado actual y el algoritmo seleccionado."""
        if self.estado not in ["Buscando", "Siguiendo camino"]:
            return False  # No hay acción que tomar
        
        # Añadir posición actual a visitados si no está ya
        if self.posicion not in self.visitados:
            self.visitados.append(self.posicion)
        
        # Verificar si llegó a la meta
        if self.posicion == laberinto.meta:
            self.estado = "Meta encontrada"
            return True
        
        # Verificar si necesita recalcular el camino
        if (self.ultimo_camino is None or 
            self.indice_camino >= len(self.ultimo_camino) or 
            self.pasos_sin_avance >= 3):
            
            # El cambio automático de algoritmo solo ocurre si no fue seleccionado manualmente
            if not self.algoritmo_manual:
                # Comprobar si el agente está atrapado
                if agente_atrapado(laberinto, self.posicion):
                    self.ciclos_atrapado += 1
                    # Cambiar de algoritmo si sigue atrapado
                    if self.ciclos_atrapado >= 2:
                        self.algoritmo_actual = sugerir_algoritmo(self.algoritmo_actual, "atrapado")
                        self.ciclos_atrapado = 0
                else:
                    self.ciclos_atrapado = 0
                    # Evaluar la situación del laberinto para elegir el mejor algoritmo
                    situacion = laberinto.calcular_situacion(self.posicion)
                    algoritmo_sugerido = sugerir_algoritmo(self.algoritmo_actual, situacion)
                    if algoritmo_sugerido != self.algoritmo_actual:
                        self.algoritmo_actual = algoritmo_sugerido
            
            # Calcular nuevo camino con el algoritmo actual
            camino, nodos_visitados, nodo_final = elegir_algoritmo(
                laberinto, self.posicion, laberinto.meta, self.algoritmo_actual
            )
            
            # Guardar el nodo final para visualización del árbol
            self.nodo_final = nodo_final
            
            # Actualizar el árbol de búsqueda para visualización
            if nodo_final:
                self.visualizador.construir_arbol_desde_nodo(nodo_final)
            else:
                self.visualizador.construir_arbol_desde_visitados(
                    self.algoritmo_actual, nodos_visitados, camino
                )
            
            # Actualizar visitados con los nodos explorados por el algoritmo
            for nodo in nodos_visitados:
                if nodo not in self.visitados:
                    self.visitados.append(nodo)
            
            # Si no se encontró camino, intentar con otro algoritmo, pero solo si no es una selección manual
            if camino is None and not self.algoritmo_manual:
                algoritmos = ["BFS", "DFS", "A*"]
                algoritmos.remove(self.algoritmo_actual)
                for algo in algoritmos:
                    camino, nodos_visitados, nodo_final = elegir_algoritmo(
                        laberinto, self.posicion, laberinto.meta, algo
                    )
                    if camino:
                        self.algoritmo_actual = algo
                        self.nodo_final = nodo_final
                        # Actualizar visualización
                        if nodo_final:
                            self.visualizador.construir_arbol_desde_nodo(nodo_final)
                        else:
                            self.visualizador.construir_arbol_desde_visitados(
                                self.algoritmo_actual, nodos_visitados, camino
                            )
                        break
            
            # Actualizar el camino y resetear el contador
            if camino:
                self.ultimo_camino = camino
                self.indice_camino = 1  # Empezar desde el siguiente (0 es la posición actual)
                self.pasos_sin_avance = 0
                self.estado = "Siguiendo camino"
                # Guardar el camino calculado como el óptimo actual
                self.camino_optimo = camino
            else:
                # No se encontró camino con ningún algoritmo
                self.estado = "Sin solución"
                return False
        
        # Seguir el camino calculado
        if self.estado == "Siguiendo camino" and self.indice_camino < len(self.ultimo_camino):
            siguiente_pos = self.ultimo_camino[self.indice_camino]
            
            # Verificar si la celda siguiente es válida (puede haber cambiado el laberinto)
            fila, col = siguiente_pos
            if (0 <= fila < laberinto.filas and 0 <= col < laberinto.columnas and 
                laberinto.grid[fila][col] == 0):
                # Mover al siguiente paso
                self.posicion = siguiente_pos
                self.historial_posiciones.append(siguiente_pos)
                self.indice_camino += 1
                self.pasos_sin_avance = 0
            else:
                # El camino ya no es válido, recalcular en la próxima iteración
                self.pasos_sin_avance += 1
                self.ultimo_camino = None
        
        return True
    
    def cambiar_algoritmo(self, nuevo_algoritmo):
        """Cambia el algoritmo de búsqueda manualmente."""
        if nuevo_algoritmo in ["BFS", "DFS", "A*"]:
            self.algoritmo_actual = nuevo_algoritmo
            self.algoritmo_manual = True  # Marcar como selección manual
            # Forzar recálculo de la ruta
            self.ultimo_camino = None
            self.pasos_sin_avance = 0
            return True
        return False
    
    def obtener_superficie_arbol(self):
        """Devuelve la superficie con la visualización del árbol de búsqueda."""
        return self.visualizador.obtener_superficie()
