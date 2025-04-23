import networkx as nx  # Para crear y manipular grafos dirigidos
import matplotlib.pyplot as plt  # Para generar gráficos y visualizaciones
from matplotlib.backends.backend_agg import FigureCanvasAgg  # Para convertir gráficos de matplotlib a superficies de pygame
from networkx.drawing.nx_agraph import graphviz_layout  # Para calcular posiciones de nodos en un grafo usando Graphviz
import pygame  # Para mostrar gráficos en una ventana interactiva
import numpy as np  # Para operaciones matemáticas y de manipulación de datos

class VisualizadorArbol:
    def __init__(self):
        # Inicializa el visualizador con un grafo vacío y configuraciones predeterminadas
        self.grafo = nx.DiGraph()  # Grafo dirigido para representar el árbol de búsqueda
        self.posiciones = None  # Posiciones de los nodos en el grafo
        self.figura = None  # Figura de matplotlib para la visualización
        self.superficie = None  # Superficie de pygame para mostrar el grafo
        self.ultimo_algoritmo = None  # Algoritmo utilizado para generar el grafo
        self.ancho = 500  # Ancho de la visualización
        self.alto = 700  # Alto de la visualización
        self.niveles = {}  # Diccionario para almacenar los niveles de los nodos en el árbol

    def limpiar(self):
        """Limpia el grafo y reinicia la visualización."""
        self.grafo.clear()  # Elimina todos los nodos y aristas del grafo
        self.posiciones = None
        self.figura = None
        self.superficie = None
        self.niveles = {}  # Reinicia los niveles de los nodos

    def construir_arbol_desde_nodo(self, nodo_final):
        # Construye un árbol de búsqueda a partir del nodo final.
        self.limpiar()

        # Si no hay nodo final, no se puede construir el árbol
        if nodo_final is None:
            return

        # Recorrer desde el nodo final hasta el nodo inicial
        pila = [nodo_final]  # Pila para realizar un recorrido en profundidad
        visitados = set()  # Conjunto para evitar procesar nodos repetidos
        self.niveles = {}  # Reiniciar niveles
        max_profundidad = 0  # Variable para rastrear la profundidad máxima del árbol

        while pila:
            nodo = pila.pop()  # Extraer el nodo actual de la pila
            estado_str = f"{nodo.estado[0]},{nodo.estado[1]}"  # Convertir el estado a string para usarlo como clave

            if estado_str not in visitados:
                visitados.add(estado_str)  # Marcar el nodo como visitado

                # Calcular la profundidad del nodo
                profundidad = 0
                p = nodo
                while p.padre:  # Subir por los nodos padres para calcular la profundidad
                    profundidad += 1
                    p = p.padre
                self.niveles[estado_str] = profundidad  # Almacenar el nivel del nodo
                max_profundidad = max(max_profundidad, profundidad)  # Actualizar la profundidad máxima

                # Si tiene padre, agregar la conexión al grafo
                if nodo.padre:
                    padre_str = f"{nodo.padre.estado[0]},{nodo.padre.estado[1]}"
                    self.grafo.add_edge(padre_str, estado_str)  # Agregar arista entre el padre y el nodo actual
                    pila.append(nodo.padre)  # Agregar el padre a la pila para procesarlo
                else:
                    # Es el nodo inicial, agregarlo al grafo
                    self.grafo.add_node(estado_str)

        # Calcular las posiciones de los nodos usando Graphviz
        self.posiciones = graphviz_layout(self.grafo, prog='dot')

    def calcular_posiciones_arbol(self, max_profundidad):
        # Calcula las posiciones de los nodos para visualizarlos como un árbol binario.
        # Los nodos se distribuyen por niveles, con el nodo raíz en la parte superior.
        posiciones = {}
        
        # Si no hay nodos, retornar un diccionario vacío
        if not self.grafo.nodes:
            return posiciones
        
        # Ancho y alto del espacio de visualización (valores lógicos)
        ancho = 10
        alto = 10
        
        # Calcular el número máximo de nodos en un nivel para centrar la visualización
        max_nodos_en_nivel = 1
        for nivel in range(max_profundidad + 1):
            nodos_en_nivel = sum(1 for nodo in self.grafo.nodes if self.niveles.get(nodo) == nivel)
            max_nodos_en_nivel = max(max_nodos_en_nivel, nodos_en_nivel)

        # Espacio horizontal y vertical disponible por nivel
        espacio_x = ancho / (max_nodos_en_nivel + 1)
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
            # AJUSTAMOS EL ANCHO DE LA FIGURA (primer valor en figsize)
            self.figura = plt.figure(figsize=(4.8, 7), dpi=100)
            ax = self.figura.add_subplot(111)
            ax.text(0.5, 0.5, "No hay datos para visualizar",
                   horizontalalignment='center', verticalalignment='center')
            ax.set_xticks([])
            ax.set_yticks([])
            plt.tight_layout()
        else:
            # Crear figura con mayor tamaño vertical
            # AJUSTAMOS EL ANCHO DE LA FIGURA (primer valor en figsize)
            self.figura = plt.figure(figsize=(4.8, 7), dpi=100)
            ax = self.figura.add_subplot(111)
            
            # Ajustar margen para dar más espacio
            plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
            
            # Determinar el número de nodos para ajustar el tamaño
            num_nodos = len(self.grafo.nodes())
            node_size = 600 if num_nodos < 20 else 350 if num_nodos < 50 else 400
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
                                      width=0.8, alpha=0.7, ax=ax)

            # Dibujar bordes del camino óptimo
            optimal_edges = [(u, v) for u, v, d in self.grafo.edges(data=True)
                            if 'optimal' in d and d['optimal']]
            if optimal_edges:
                nx.draw_networkx_edges(self.grafo, self.posiciones, edgelist=optimal_edges,
                                      width=2.0, edge_color='red', ax=ax)

            # Mostrar etiquetas de nodos con tamaño ajustable
            nx.draw_networkx_labels(self.grafo, self.posiciones, font_size=font_size, ax=ax)

            # Título más compacto
            plt.title(f"Árbol - {self.ultimo_algoritmo}", fontsize=10)
            
            # Remover bordes
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            
            plt.tight_layout(pad=0.1)

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
        self.superficie = pygame.transform.scale(surf, (self.ancho, self.alto))

        return self.superficie

    def obtener_superficie(self):
        # Devuelve la superficie actualizada para dibujar en pygame.
        if self.superficie is None:
            self.actualizar_visualizacion()
        return self.superficie
