import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from networkx.drawing.nx_agraph import graphviz_layout
import pygame
import numpy as np

class VisualizadorArbol:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.posiciones = None
        self.figura = None
        self.superficie = None
        self.ultimo_algoritmo = None
        self.ancho = 500
        self.alto = 700  # Aumentar la altura para dar más espacio vertical
        self.niveles = {}  # Diccionario para almacenar los niveles de los nodos

    def limpiar(self):
        """Limpia el grafo y reinicia la visualización."""
        self.grafo.clear()
        self.posiciones = None
        self.figura = None
        self.superficie = None
        self.niveles = {}

    def construir_arbol_desde_nodo(self, nodo_final):
        # Construye un árbol de búsqueda a partir del nodo final.
        self.limpiar()

        # Si no hay nodo final, no hay árbol
        if nodo_final is None:
            return

        # Recorrer desde el nodo final hasta el nodo inicial
        pila = [nodo_final]
        visitados = set()
        self.niveles = {}  # Reiniciar niveles
        max_profundidad = 0

        while pila:
            nodo = pila.pop()
            estado_str = f"{nodo.estado[0]},{nodo.estado[1]}"

            if estado_str not in visitados:
                visitados.add(estado_str)

                # Calcular la profundidad del nodo
                profundidad = 0
                p = nodo
                while p.padre:
                    profundidad += 1
                    p = p.padre
                self.niveles[estado_str] = profundidad
                max_profundidad = max(max_profundidad, profundidad)

                # Si tiene padre, agregar la conexión
                if nodo.padre:
                    padre_str = f"{nodo.padre.estado[0]},{nodo.padre.estado[1]}"
                    self.grafo.add_edge(padre_str, estado_str)
                    pila.append(nodo.padre)
                else:
                    # Es el nodo inicial
                    self.grafo.add_node(estado_str)

        # Calcular las posiciones de los nodos
        self.posiciones = graphviz_layout(self.grafo, prog='dot')
    def construir_arbol_desde_nodos(self, algoritmo, nodos, camino=None):
        self.limpiar()
        self.ultimo_algoritmo = algoritmo

        if not nodos:
            return

        for nodo in nodos:
            hijo_str = f"{nodo.estado[0]},{nodo.estado[1]}"
            self.grafo.add_node(hijo_str)

            if nodo.padre:
                padre_str = f"{nodo.padre.estado[0]},{nodo.padre.estado[1]}"
                self.grafo.add_node(padre_str)
                self.grafo.add_edge(padre_str, hijo_str)

        self.niveles = self.calcular_niveles_desde_inicio(nodos[0].estado)

        if camino:
            for i in range(len(camino) - 1):
                estado1 = f"{camino[i][0]},{camino[i][1]}"
                estado2 = f"{camino[i+1][0]},{camino[i+1][1]}"
                if self.grafo.has_edge(estado1, estado2):
                    self.grafo[estado1][estado2]['optimal'] = True

        self.posiciones = graphviz_layout(self.grafo, prog='dot') 

    def construir_arbol_desde_visitados(self, algoritmo, visitados, camino=None):
        # Construye un árbol de búsqueda a partir de los nodos visitados.
        self.limpiar()
        self.ultimo_algoritmo = algoritmo

        if not visitados:
            return

        # Crear nodos para todos los estados visitados
        for i, estado in enumerate(visitados):
            estado_str = f"{estado[0]},{estado[1]}"
            self.grafo.add_node(estado_str)

        # Crear aristas basadas en la secuencia de visitados, asumiendo que están en orden de descubrimiento
        for i in range(len(visitados) - 1):
            estado_actual = f"{visitados[i][0]},{visitados[i][1]}"
            estado_siguiente = f"{visitados[i+1][0]},{visitados[i+1][1]}"
            self.grafo.add_edge(estado_actual, estado_siguiente)
            
        # Calcular niveles de los nodos basado en la distancia al nodo inicial
        self.niveles = self.calcular_niveles_desde_inicio(visitados[0])
        max_profundidad = max(self.niveles.values()) if self.niveles else 0

        # Resaltar el camino óptimo si se proporciona
        if camino:
            for i in range(len(camino) - 1):
                estado1 = camino[i]
                estado2 = camino[i+1]
                estado1_str = f"{estado1[0]},{estado1[1]}"
                estado2_str = f"{estado2[0]},{estado2[1]}"

                # Añadir bordes del camino óptimo
                if not self.grafo.has_edge(estado1_str, estado2_str):
                    self.grafo.add_edge(estado1_str, estado2_str)

                # Marcar los bordes del camino óptimo
                self.grafo[estado1_str][estado2_str]['optimal'] = True

        # Calcular las posiciones de los nodos
        self.posiciones = graphviz_layout(self.grafo, prog='dot')
        
    def calcular_niveles_desde_inicio(self, nodo_inicio):
        
        # Calcula los niveles de los nodos en el grafo desde un nodo de inicio dado.
        # Esto es útil cuando los nodos visitados no forman un árbol perfecto, pero queremos
        # visualizarlos en una estructura basada en niveles.
        
        niveles = {}
        cola = [(nodo_inicio, 0)]  # Tupla: (nodo, nivel)
        visitados = set()
    
        while cola:
            nodo, nivel = cola.pop(0)
            estado_str = f"{nodo[0]},{nodo[1]}"  # Convertir tupla de estado a string
            
            if estado_str in visitados:
                continue
            
            visitados.add(estado_str)
            niveles[estado_str] = nivel
            
            # Encontrar vecinos en el grafo
            for vecino in self.grafo.successors(estado_str):
                # Convertir el vecino de string a tupla para la siguiente iteración
                vecino_estado = tuple(map(int, vecino.split(',')))
                cola.append((vecino_estado, nivel + 1))
        return niveles

    def calcular_posiciones_arbol(self, max_profundidad):
        
        # Calcula las posiciones de los nodos para visualizarlos como un árbol binario.
        # Los nodos se distribuyen por niveles, con el nodo raíz en la parte superior.
    
        posiciones = {}
        
        # Si no hay nodos, retornar un diccionario vacío
        if not self.grafo.nodes:
            return posiciones
        
        # Ancho y alto del espacio de visualización
        ancho = 10  # Ancho lógico para la distribución de nodos
        alto = 10   # Alto lógico para la distribución de nodos
        
        # Calcular el número de nodos en el nivel más ancho para centrar la visualización
        max_nodos_en_nivel = 1
        for nivel in range(max_profundidad + 1):
            nodos_en_nivel = sum(1 for nodo in self.grafo.nodes if self.niveles.get(nodo) == nivel)
            max_nodos_en_nivel = max(max_nodos_en_nivel, nodos_en_nivel)

        # Espacio horizontal disponible por nivel
        espacio_x = ancho / (max_nodos_en_nivel + 1)
        
        # Espacio vertical por nivel
        espacio_y = alto / (max_profundidad + 1)

        for nodo in self.grafo.nodes:
            nivel = self.niveles.get(nodo, 0)  # Obtener el nivel del nodo, 0 por defecto
            nodos_en_este_nivel = [n for n in self.grafo.nodes if self.niveles.get(n) == nivel]
            
            # Calcular la posición x del nodo
            indice_nodo_en_nivel = nodos_en_este_nivel.index(nodo)
            x = (indice_nodo_en_nivel + 1) * espacio_x
            
            # Calcular la posición y del nodo
            y = nivel * espacio_y
            
            posiciones[nodo] = (x, y)
        
        # Convertir las posiciones lógicas a las dimensiones reales de la visualización
        x_factor = self.ancho / ancho
        y_factor = self.alto / alto
        
        posiciones_escaladas = {nodo: (x * x_factor, y * y_factor) for nodo, (x, y) in posiciones.items()}
        
        return posiciones_escaladas
    
    def actualizar_visualizacion(self):
        # Actualiza la visualización del árbol y la convierte en una superficie de pygame.
        if not self.grafo or not self.posiciones:
            # Crear un grafo vacío si no hay datos
            self.figura = plt.figure(figsize=(5, 7), dpi=100)  # Mayor tamaño y relación de aspecto
            ax = self.figura.add_subplot(111)
            ax.text(0.5, 0.5, "No hay datos para visualizar",
                   horizontalalignment='center', verticalalignment='center')
            ax.set_xticks([])
            ax.set_yticks([])
            plt.tight_layout()
        else:
            # Crear figura con mayor tamaño vertical
            self.figura = plt.figure(figsize=(5, 7), dpi=100)  # Ajuste para árboles altos
            ax = self.figura.add_subplot(111)
            
            # Ajustar margen para dar más espacio
            plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
            
            # Determinar el número de nodos para ajustar el tamaño
            num_nodos = len(self.grafo.nodes())
            # Ajustar tamaño de nodo según la cantidad de nodos
            node_size = 600 if num_nodos < 20 else 350 if num_nodos < 50 else 400
            # Ajustar tamaño de fuente según la cantidad de nodos
            font_size = 8 if num_nodos < 20 else 6 if num_nodos < 50 else 5

            # Colores de nodos según el algoritmo
            if self.ultimo_algoritmo == "BFS":
                node_color = 'skyblue'
            elif self.ultimo_algoritmo == "DFS":
                node_color = 'lightgreen'
            else:  # A*
                node_color = 'lightcoral'

            # Dibujar nodos con tamaño ajustado
            nx.draw_networkx_nodes(self.grafo, self.posiciones, node_size=node_size,
                                  node_color=node_color, ax=ax)

            # Dibujar bordes normales
            normal_edges = [(u, v) for u, v, d in self.grafo.edges(data=True)
                            if 'optimal' not in d or not d['optimal']]
            if normal_edges:
                nx.draw_networkx_edges(self.grafo, self.posiciones, edgelist=normal_edges,
                                      width=0.8, alpha=0.7, ax=ax)  # Bordes más delgados

            # Dibujar bordes del camino óptimo
            optimal_edges = [(u, v) for u, v, d in self.grafo.edges(data=True)
                            if 'optimal' in d and d['optimal']]
            if optimal_edges:
                nx.draw_networkx_edges(self.grafo, self.posiciones, edgelist=optimal_edges,
                                      width=2.0, edge_color='red', ax=ax)  # Camino óptimo más destacado

            # Mostrar etiquetas de nodos con tamaño ajustable
            nx.draw_networkx_labels(self.grafo, self.posiciones, font_size=font_size, ax=ax)

            # Título más compacto
            plt.title(f"Árbol - {self.ultimo_algoritmo}", fontsize=10)
            
            # Remover bordes
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            
            plt.tight_layout(pad=0.1)  # Reducir padding

        # Convertir figura a superficie de pygame
        canvas = FigureCanvasAgg(self.figura)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        # Cerrar la figura para liberar memoria
        plt.close(self.figura)

        # Crear surface de pygame
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        # Escalar al tamaño deseado
        self.superficie = pygame.transform.scale(surf, (self.ancho, self.alto))

        return self.superficie

    def obtener_superficie(self):
        """Devuelve la superficie actualizada para dibujar en pygame."""
        if self.superficie is None:
            self.actualizar_visualizacion()
        return self.superficie