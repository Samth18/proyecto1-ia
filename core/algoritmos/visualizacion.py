import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pygame
import io
import numpy as np

class VisualizadorArbol:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.posiciones = None
        self.figura = None
        self.superficie = None
        self.ultimo_algoritmo = None
        self.ancho = 380
        self.alto = 380
        
    def limpiar(self):
        """Limpia el grafo y reinicia la visualización."""
        self.grafo.clear()
        self.posiciones = None
        self.figura = None
        self.superficie = None
        
    def construir_arbol_desde_nodo(self, nodo_final):
        """Construye un árbol de búsqueda a partir del nodo final."""
        self.limpiar()
        
        # Si no hay nodo final, no hay árbol
        if nodo_final is None:
            return
            
        # Recorrer desde el nodo final hasta el nodo inicial
        pila = [nodo_final]
        visitados = set()
        
        while pila:
            nodo = pila.pop()
            estado_str = f"{nodo.estado[0]},{nodo.estado[1]}"
            
            if estado_str not in visitados:
                visitados.add(estado_str)
                
                # Si tiene padre, agregar la conexión
                if nodo.padre:
                    padre_str = f"{nodo.padre.estado[0]},{nodo.padre.estado[1]}"
                    self.grafo.add_edge(padre_str, estado_str)
                    pila.append(nodo.padre)
                else:
                    # Es el nodo inicial
                    self.grafo.add_node(estado_str)
                    
        # Calcular las posiciones de los nodos
        self.posiciones = nx.spring_layout(self.grafo)
        
    def construir_arbol_desde_visitados(self, algoritmo, visitados, camino=None):
        """Construye un árbol de búsqueda a partir de los nodos visitados."""
        self.limpiar()
        self.ultimo_algoritmo = algoritmo
        
        if not visitados:
            return
            
        # Crear nodos para todos los estados visitados
        for i, estado in enumerate(visitados):
            estado_str = f"{estado[0]},{estado[1]}"
            self.grafo.add_node(estado_str)
            
            # Si no es el primer nodo y hay un camino posible al nodo anterior
            if i > 0:
                prev_estado = visitados[i-1]
                prev_estado_str = f"{prev_estado[0]},{prev_estado[1]}"
                
                # Verificar si son adyacentes (manhattan = 1)
                if abs(estado[0] - prev_estado[0]) + abs(estado[1] - prev_estado[1]) == 1:
                    self.grafo.add_edge(prev_estado_str, estado_str)
        
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
        self.posiciones = nx.spring_layout(self.grafo)
    
    def actualizar_visualizacion(self):
        """Actualiza la visualización del árbol y la convierte en una superficie de pygame."""
        if not self.grafo or not self.posiciones:
            # Crear un grafo vacío si no hay datos
            self.figura = plt.figure(figsize=(4, 4), dpi=100)
            ax = self.figura.add_subplot(111)
            ax.text(0.5, 0.5, "No hay datos para visualizar", 
                   horizontalalignment='center', verticalalignment='center')
            ax.set_xticks([])
            ax.set_yticks([])
            plt.tight_layout()
        else:
            # Crear figura
            self.figura = plt.figure(figsize=(4, 4), dpi=100)
            ax = self.figura.add_subplot(111)
            
            # Colores de nodos según el algoritmo
            if self.ultimo_algoritmo == "BFS":
                node_color = 'skyblue'
            elif self.ultimo_algoritmo == "DFS":
                node_color = 'lightgreen'
            else:  # A*
                node_color = 'lightcoral'
            
            # Dibujar nodos
            nx.draw_networkx_nodes(self.grafo, self.posiciones, node_size=300, 
                                  node_color=node_color, ax=ax)
            
            # Dibujar bordes normales
            normal_edges = [(u, v) for u, v, d in self.grafo.edges(data=True) 
                           if 'optimal' not in d or not d['optimal']]
            if normal_edges:
                nx.draw_networkx_edges(self.grafo, self.posiciones, edgelist=normal_edges, 
                                      width=1.0, alpha=0.7, ax=ax)
            
            # Dibujar bordes del camino óptimo
            optimal_edges = [(u, v) for u, v, d in self.grafo.edges(data=True) 
                            if 'optimal' in d and d['optimal']]
            if optimal_edges:
                nx.draw_networkx_edges(self.grafo, self.posiciones, edgelist=optimal_edges, 
                                      width=2.5, edge_color='red', ax=ax)
            
            # Mostrar etiquetas de nodos
            nx.draw_networkx_labels(self.grafo, self.posiciones, font_size=8, ax=ax)
            
            # Título
            plt.title(f"Árbol de búsqueda - {self.ultimo_algoritmo}")
            plt.tight_layout()
        
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