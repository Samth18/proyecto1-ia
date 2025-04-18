import pygame
import time
from core.laberinto import Laberinto
from core.agente import Agente

# Constantes
ANCHO_VENTANA = 1600  # 800 para laberinto + 400 para panel + 400 para árbol
ANCHO_MIN_VENTANA = 1200  # Sin visualización de árbol
ALTO_VENTANA = 800
TAMANO_CELDA = 40
MARGEN = 2

# Colores
COLORES = {
    "pared": (0, 0, 0),          # Negro
    "camino": (224, 224, 224),   # Gris claro
    "agente": (0, 255, 0),       # Verde
    "meta": (255, 0, 0),         # Rojo
    "visitado": (173, 216, 230), # Azul claro
    "ruta": (255, 255, 0),       # Amarillo
    "fondo": (255, 255, 255),    # Blanco
    "panel": (240, 240, 240),    # Gris muy claro
    "borde_arbol": (220, 220, 220)  # Borde para el área del árbol
}

def dibujar_laberinto(ventana, laberinto, agente):
    ventana.fill(COLORES["fondo"])  # Fondo blanco
    
    # Dibujar celdas
    for fila in range(laberinto.filas):
        for col in range(laberinto.columnas):
            x = col * (TAMANO_CELDA + MARGEN)
            y = fila * (TAMANO_CELDA + MARGEN)
            
            if laberinto.grid[fila][col] == 1:
                color = COLORES["pared"]
            elif (fila, col) == laberinto.meta:
                color = COLORES["meta"]
            elif (fila, col) in agente.visitados:
                color = COLORES["visitado"]
            elif (fila, col) in agente.camino_optimo:
                color = COLORES["ruta"]
            else:
                color = COLORES["camino"]
            
            pygame.draw.rect(ventana, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
    
    # Dibujar agente
    agente_x = agente.posicion[1] * (TAMANO_CELDA + MARGEN) + TAMANO_CELDA // 2
    agente_y = agente.posicion[0] * (TAMANO_CELDA + MARGEN) + TAMANO_CELDA // 2
    pygame.draw.circle(ventana, COLORES["agente"], (agente_x, agente_y), TAMANO_CELDA // 4)

def dibujar_panel(ventana, agente, laberinto, pasos, tiempo_inicio, estado, modo_dinamico, contador_dinamico, velocidad, mostrar_arbol):
    panel_x = 800  # Ancho del laberinto
    panel = pygame.Surface((400, ALTO_VENTANA))
    panel.fill(COLORES["panel"])
    
    # Fuentes
    fuente = pygame.font.SysFont("Arial", 24)
    fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
    
    # Título
    texto_titulo = fuente_titulo.render("Panel de Control", True, (0, 0, 0))
    panel.blit(texto_titulo, (100, 20))
    
    # Información
    if estado == "Meta encontrada" and hasattr(agente, 'tiempo_final'):
        tiempo_actual = agente.tiempo_final
    elif tiempo_inicio:
        tiempo_actual = time.time() - tiempo_inicio
    else:
        tiempo_actual = 0   

    texto_algoritmo = fuente.render(f"Algoritmo: {agente.algoritmo_actual}", True, (0, 0, 0))
    texto_pasos = fuente.render(f"Pasos: {pasos}", True, (0, 0, 0))
    texto_tiempo = fuente.render(f"Tiempo: {tiempo_actual:.1f}s", True, (0, 0, 0))
    texto_estado = fuente.render(f"Estado: {agente.estado}", True, (0, 0, 0))
    texto_dinamico = fuente.render(f"Modo Dinámico: {'Activado' if modo_dinamico else 'Desactivado'}", True, (0, 0, 0))
    texto_contador = fuente.render(f"Cambios en: {contador_dinamico}", True, (0, 0, 0) if contador_dinamico > 3 else (255, 0, 0))
    
    # Posicionar textos
    panel.blit(texto_algoritmo, (20, 80))
    panel.blit(texto_pasos, (20, 120))
    panel.blit(texto_tiempo, (20, 160))
    panel.blit(texto_estado, (20, 200))
    panel.blit(texto_dinamico, (20, 240))
    if modo_dinamico:
        panel.blit(texto_contador, (20, 280))
    
    # Botones
    botones = []
    y_offset = 320 if modo_dinamico else 280
    
    # Botón Inicio/Pausa
    boton_inicio = pygame.Rect(50, y_offset, 300, 50)
    pygame.draw.rect(panel, (100, 180, 100), boton_inicio)
    texto_inicio = fuente.render("Iniciar/Pausar", True, (0, 0, 0))
    panel.blit(texto_inicio, (130, y_offset + 15))
    botones.append(("inicio", boton_inicio))
    y_offset += 60
    
    # Botón Reiniciar
    boton_reinicio = pygame.Rect(50, y_offset, 300, 50)
    pygame.draw.rect(panel, (180, 100, 100), boton_reinicio)
    texto_reinicio = fuente.render("Reiniciar", True, (0, 0, 0))
    panel.blit(texto_reinicio, (150, y_offset + 15))
    botones.append(("reinicio", boton_reinicio))
    y_offset += 60
    
    # Botón Mostrar/Ocultar Árbol
    boton_arbol = pygame.Rect(50, y_offset, 300, 50)
    color_arbol = (150, 150, 220) if mostrar_arbol else (200, 200, 200)
    pygame.draw.rect(panel, color_arbol, boton_arbol)
    texto_arbol = fuente.render("Mostrar/Ocultar Árbol", True, (0, 0, 0))
    panel.blit(texto_arbol, (95, y_offset + 15))
    botones.append(("arbol", boton_arbol))
    y_offset += 60
    
    # Botón Modo Dinámico
    boton_dinamico = pygame.Rect(50, y_offset, 300, 50)
    color_dinamico = (150, 150, 220) if modo_dinamico else (200, 200, 200)
    pygame.draw.rect(panel, color_dinamico, boton_dinamico)
    texto_dinamico = fuente.render("Modo Dinámico", True, (0, 0, 0))
    panel.blit(texto_dinamico, (130, y_offset + 15))
    botones.append(("dinamico", boton_dinamico))
    y_offset += 60
    
    # Selección de algoritmo
    texto_seleccion = fuente.render("Seleccionar Algoritmo:", True, (0, 0, 0))
    panel.blit(texto_seleccion, (20, y_offset))
    y_offset += 40
    
    algoritmos = ["BFS", "DFS", "A*"]
    for algo in algoritmos:
        boton_algo = pygame.Rect(50, y_offset, 300, 40)
        if algo == agente.algoritmo_actual:
            pygame.draw.rect(panel, (150, 150, 220), boton_algo)
        else:
            pygame.draw.rect(panel, (200, 200, 200), boton_algo)
        texto_algo = fuente.render(algo, True, (0, 0, 0))
        panel.blit(texto_algo, (180, y_offset + 10))
        botones.append((f"algo_{algo}", boton_algo))
        y_offset += 50
    
    # Control de velocidad
    texto_velocidad = fuente.render("Velocidad:", True, (0, 0, 0))
    panel.blit(texto_velocidad, (20, y_offset))
    y_offset += 40
    
    velocidades = ["Lenta", "Normal", "Rápida"]
    for vel in velocidades:
        boton_vel = pygame.Rect(50, y_offset, 300, 30)
        if vel == velocidad:
            pygame.draw.rect(panel, (150, 150, 220), boton_vel)
        else:
            pygame.draw.rect(panel, (200, 200, 200), boton_vel)
        texto_vel = fuente.render(vel, True, (0, 0, 0))
        panel.blit(texto_vel, (180, y_offset + 5))
        botones.append((f"vel_{vel}", boton_vel))
        y_offset += 40
    
    ventana.blit(panel, (panel_x, 0))
    return botones

def dibujar_arbol_busqueda(ventana, agente):
    """Dibuja el árbol de búsqueda del algoritmo actual."""
    arbol_x = 1200  # Posición después del panel de control
    
    # Dibujar fondo y borde
    pygame.draw.rect(ventana, COLORES["borde_arbol"], pygame.Rect(arbol_x, 0, 400, ALTO_VENTANA))
    
    # Obtener la superficie del árbol desde el agente
    superficie_arbol = agente.obtener_superficie_arbol()
    
    # Título del área
    fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
    titulo = fuente_titulo.render("Árbol de Búsqueda", True, (0, 0, 0))
    ventana.blit(titulo, (arbol_x + 100, 20))
    
    # Dibujar el árbol centrado en su área
    if superficie_arbol:
        ventana.blit(superficie_arbol, (arbol_x + 10, 60))

def obtener_fps_por_velocidad(velocidad):
    """Devuelve los FPS según la velocidad seleccionada."""
    if velocidad == "Lenta":
        return 5
    elif velocidad == "Normal":
        return 10
    elif velocidad == "Rápida":
        return 20
    return 10  # Por defecto

def main():
    pygame.init()
    
    # Variables de control
    mostrar_arbol = True
    ancho_actual = ANCHO_VENTANA if mostrar_arbol else ANCHO_MIN_VENTANA
    
    ventana = pygame.display.set_mode((ancho_actual, ALTO_VENTANA))
    pygame.display.set_caption("Laberinto Dinámico IA")
    
    # Crear laberinto y agente
    laberinto = Laberinto(15, 15, 0.3)
    agente = Agente(laberinto.inicio)
    
    # Variables de control adicionales
    reloj = pygame.time.Clock()
    ejecutando = False
    pasos = 0
    tiempo_inicio = None
    tiempo_final = None  # Para almacenar el tiempo cuando se encuentra la meta
    pasos_finales = 0    # Para almacenar los pasos cuando se encuentra la meta
    modo_dinamico = False
    contador_dinamico = 10
    velocidad = "Normal"
    
    while True:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar clics en botones
                x, y = pygame.mouse.get_pos()
                if x > 800 and x < 1200:  # En el panel de control
                    x_rel, y_rel = x - 800, y
                    for nombre, rect in botones:
                        if rect.collidepoint(x_rel, y_rel):
                            if nombre == "inicio":
                                if agente.estado != "Meta encontrada":  # Solo permitir iniciar/pausar si no ha encontrado la meta
                                    ejecutando = not ejecutando
                                    if ejecutando:
                                        agente.estado = "Buscando"
                                        if tiempo_inicio is None:
                                            tiempo_inicio = time.time()
                                    else:
                                        agente.estado = "Pausado"
                            elif nombre == "reinicio":
                                agente.reiniciar(laberinto.inicio)
                                ejecutando = False
                                pasos = 0
                                tiempo_inicio = None
                                tiempo_final = None
                                pasos_finales = 0
                                contador_dinamico = 10
                            elif nombre == "arbol":
                                mostrar_arbol = not mostrar_arbol
                                ancho_actual = ANCHO_VENTANA if mostrar_arbol else ANCHO_MIN_VENTANA
                                ventana = pygame.display.set_mode((ancho_actual, ALTO_VENTANA))
                            elif nombre == "dinamico":
                                modo_dinamico = not modo_dinamico
                            elif nombre.startswith("algo_"):
                                nuevo_algo = nombre.split("_")[1]
                                if agente.cambiar_algoritmo(nuevo_algo):
                                    if agente.estado == "Esperando":
                                        agente.estado = "Buscando"
                                        if tiempo_inicio is None:
                                            tiempo_inicio = time.time()
                                        ejecutando = True
                            elif nombre.startswith("vel_"):
                                velocidad = nombre.split("_")[1]
        
        # Actualizar estado del juego
        if ejecutando and agente.estado != "Meta encontrada":
            # Actualizar el agente
            agente.actuar(laberinto)
            pasos += 1
            
            # Verificar si encontró la meta
            if agente.estado == "Meta encontrada":
                agente.tiempo_final = time.time() - tiempo_inicio
                pasos_finales = pasos
                ejecutando = False  # Detener la ejecución automática
            
            # Actualizar modo dinámico
            if modo_dinamico and agente.estado != "Meta encontrada":
                contador_dinamico -= 1
                if contador_dinamico <= 0:
                    laberinto.cambiar_paredes_aleatorias(3)
                    contador_dinamico = 10
        
        # Calcular qué valores mostrar (actuales o finales si se encontró la meta)
        if agente.estado == "Meta encontrada":
            tiempo_mostrar = tiempo_final
            pasos_mostrar = pasos_finales
        elif tiempo_inicio is not None:
            tiempo_mostrar = time.time() - tiempo_inicio
            pasos_mostrar = pasos
        else:
            tiempo_mostrar = 0
            pasos_mostrar = pasos

        
        # Dibujar
        dibujar_laberinto(ventana, laberinto, agente)
        botones = dibujar_panel(ventana, agente, laberinto, pasos_mostrar, 
                               tiempo_inicio, 
                               agente.estado, modo_dinamico, contador_dinamico, velocidad, mostrar_arbol)
        if mostrar_arbol:
            dibujar_arbol_busqueda(ventana, agente)
        
        pygame.display.update()
        reloj.tick(obtener_fps_por_velocidad(velocidad))