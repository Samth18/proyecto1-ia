# Paquete de algoritmos de búsqueda
from core.algoritmos.busqueda import bfs, dfs, a_estrella, ids, elegir_algoritmo, agente_atrapado, sugerir_algoritmo
from core.algoritmos.visualizacion import VisualizadorArbol

# def elegir_algoritmo(laberinto, inicio, meta, algoritmo):
#     if algoritmo == "BFS":
#         return bfs(laberinto, inicio, meta)
#     elif algoritmo == "DFS":
#         return dfs(laberinto, inicio, meta)
#     elif algoritmo == "A*":
#         return a_estrella(laberinto, inicio, meta)
#     elif algoritmo == "IDS":
#         print("Ejecutando IDS con límite inicial ...")  # Debug
#         return ids(laberinto, inicio, meta)
#     else:
#         return bfs(laberinto, inicio, meta)
