import pygame
import time
import os
from core.laberinto import Laberinto
from core.agente import Agente

# Constantes
ANCHO_PANEL = 400
ALTO_PANEL = 1000
TAMANO_CELDA = 40
MARGEN = 2
ANCHO_LABERINTO = 900  # Ancho reservado para el laberinto
ANCHO_ARBOL = 520  # Ancho reservado para el árbol
ALTO_VENTANA = 800  # Altura de la ventana

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
    # No llenamos toda la ventana con fondo blanco, solo el área del laberinto
    area_laberinto = pygame.Rect(ANCHO_PANEL, 0, ANCHO_LABERINTO, ALTO_VENTANA)
    pygame.draw.rect(ventana, COLORES["fondo"], area_laberinto)
    
    # Dibujar celdas
    for fila in range(laberinto.filas):
        for col in range(laberinto.columnas):
            x = ANCHO_PANEL + col * (TAMANO_CELDA + MARGEN)  # Desplazar a la derecha
            y = fila * (TAMANO_CELDA + MARGEN)
            
            if laberinto.grid[fila][col] == 1:
                color = COLORES["pared"]
            elif (fila, col) == laberinto.meta:
                color = COLORES["camino"]  # Usar fondo de camino para la meta (imagen irá encima)
            elif (fila, col) in agente.visitados:
                color = COLORES["visitado"]
            elif (fila, col) in agente.camino_optimo:
                color = COLORES["ruta"]
            else:
                color = COLORES["camino"]
            
            pygame.draw.rect(ventana, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
            
            # Dibujar la meta con imagen
            if (fila, col) == laberinto.meta:
                if 'IMG_META' in globals() and IMG_META is not None:
                    try:
                        # Redimensionar imagen para ajustarse a la celda
                        img_escalada = pygame.transform.scale(IMG_META, (TAMANO_CELDA - 4, TAMANO_CELDA - 4))
                        # Centrar imagen en la celda
                        img_rect = img_escalada.get_rect(center=(x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2))
                        ventana.blit(img_escalada, img_rect)
                    except Exception as e:
                        print(f"Error al dibujar meta: {e}")
                        # Dibujar representación alternativa
                        pygame.draw.rect(ventana, COLORES["meta"], (x, y, TAMANO_CELDA, TAMANO_CELDA))
                else:
                    # Si no hay imagen, usar el cuadrado rojo
                    pygame.draw.rect(ventana, COLORES["meta"], (x, y, TAMANO_CELDA, TAMANO_CELDA))
    
    # Dibujar agente con imagen
    agente_x = ANCHO_PANEL + agente.posicion[1] * (TAMANO_CELDA + MARGEN) + TAMANO_CELDA // 2
    agente_y = agente.posicion[0] * (TAMANO_CELDA + MARGEN) + TAMANO_CELDA // 2
    
    if 'IMG_AGENTE' in globals() and IMG_AGENTE is not None:
        try:
            # Redimensionar imagen para ajustarse a la celda
            img_escalada = pygame.transform.scale(IMG_AGENTE, (TAMANO_CELDA - 4, TAMANO_CELDA - 4))
            # Centrar imagen en la celda
            img_rect = img_escalada.get_rect(center=(agente_x, agente_y))
            ventana.blit(img_escalada, img_rect)
        except Exception as e:
            print(f"Error al dibujar agente: {e}")
            # Dibujar representación alternativa
            pygame.draw.circle(ventana, COLORES["agente"], (agente_x, agente_y), TAMANO_CELDA // 4)
    else:
        # Usar círculo si la imagen no está disponible
        pygame.draw.circle(ventana, COLORES["agente"], (agente_x, agente_y), TAMANO_CELDA // 4)

def dibujar_panel(ventana, agente, laberinto, pasos, tiempo_inicio, estado, modo_dinamico, contador_dinamico, velocidad, mostrar_arbol, tiempo_final=None):
    panel_x = 0  # Panel en el borde izquierdo
    panel = pygame.Surface((ANCHO_PANEL, ALTO_PANEL))
    panel.fill(COLORES["panel"])
    
    # Fuentes
    fuente = pygame.font.SysFont("Arial", 24)
    fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
    
    # Título
    texto_titulo = fuente_titulo.render("Panel de Control", True, (0, 0, 0))
    panel.blit(texto_titulo, (100, 20))
    
    # Información
    if tiempo_final is not None:
        # Si hay un tiempo final (meta encontrada), usar ese
        tiempo_actual = tiempo_final
    else:
        # Si no, calcularlo normalmente
        tiempo_actual = time.time() - tiempo_inicio if tiempo_inicio else 0
    
    texto_algoritmo = fuente.render(f"Algoritmo: {agente.algoritmo_actual}", True, (0, 0, 0))
    texto_pasos = fuente.render(f"Pasos: {pasos}", True, (0, 0, 0))
    texto_tiempo = fuente.render(f"Tiempo: {tiempo_actual:.1f}s", True, (0, 0, 0))
    texto_estado = fuente.render(f"Estado: {agente.estado}", True, (0, 0, 0))
    texto_dinamico = fuente.render(f"Modo Dinámico: {'Activado' if modo_dinamico else 'Desactivado'}", True, (0, 0, 0))
    texto_contador = fuente.render(f"Cambios en: {contador_dinamico}", True, (0, 0, 0) if contador_dinamico > 3 else (255, 0, 0))
    
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
    botones.append(("inicio", boton_inicio.move(panel_x, 0)))  # Ajustar coordenadas absolutas
    y_offset += 60
    
    # Botón Reiniciar
    boton_reinicio = pygame.Rect(50, y_offset, 300, 50)
    pygame.draw.rect(panel, (180, 100, 100), boton_reinicio)
    texto_reinicio = fuente.render("Reiniciar", True, (0, 0, 0))
    panel.blit(texto_reinicio, (150, y_offset + 15))
    botones.append(("reinicio", boton_reinicio.move(panel_x, 0)))
    y_offset += 60
    
    # Botón Mostrar/Ocultar Árbol
    boton_arbol = pygame.Rect(50, y_offset, 300, 50)
    color_arbol = (150, 150, 220) if mostrar_arbol else (200, 200, 200)
    pygame.draw.rect(panel, color_arbol, boton_arbol)
    texto_arbol = fuente.render("Mostrar/Ocultar Árbol", True, (0, 0, 0))
    panel.blit(texto_arbol, (95, y_offset + 15))
    botones.append(("arbol", boton_arbol.move(panel_x, 0)))
    y_offset += 60
    
    # Botón Modo Dinámico
    boton_dinamico = pygame.Rect(50, y_offset, 300, 50)
    color_dinamico = (150, 150, 220) if modo_dinamico else (200, 200, 200)
    pygame.draw.rect(panel, color_dinamico, boton_dinamico)
    texto_dinamico = fuente.render("Modo Dinámico", True, (0, 0, 0))
    panel.blit(texto_dinamico, (130, y_offset + 15))
    botones.append(("dinamico", boton_dinamico.move(panel_x, 0)))
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
        botones.append((f"algo_{algo}", boton_algo.move(panel_x, 0)))
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
        botones.append((f"vel_{vel}", boton_vel.move(panel_x, 0)))
        y_offset += 40
    
    ventana.blit(panel, (panel_x, 0))
    return botones

def dibujar_arbol_busqueda(ventana, agente):
    """Dibuja el árbol de búsqueda del algoritmo actual."""
    arbol_x = ANCHO_PANEL + ANCHO_LABERINTO  # Posición después del laberinto
    
    # Dibujar fondo y borde
    pygame.draw.rect(ventana, COLORES["borde_arbol"], pygame.Rect(arbol_x, 0, ANCHO_ARBOL, ALTO_VENTANA))
    
    # Título del área
    fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
    titulo = fuente_titulo.render("Árbol de Búsqueda", True, (0, 0, 0))
    ventana.blit(titulo, (arbol_x + 100, 20))
    
    # Dibujar el árbol centrado en su área
    superficie_arbol = agente.obtener_superficie_arbol()
    if superficie_arbol:
        ventana.blit(superficie_arbol, (arbol_x + 10, 60))

def obtener_fps_por_velocidad(velocidad):
    """Devuelve los FPS según la velocidad seleccionada."""
    if velocidad == "Lenta":
        return 3
    elif velocidad == "Normal":
        return 8
    elif velocidad == "Rápida":
        return 15
    return 12  # Por defecto

def main():
    pygame.init()
    
    # Variables para las imágenes
    global IMG_AGENTE, IMG_META
    IMG_AGENTE = None
    IMG_META = None
    
    # Cargar imágenes para el agente y la meta - con mejor diagnóstico
    try:
        # Ruta a la carpeta de assets
        RUTA_ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        print(f"Buscando imágenes en: {RUTA_ASSETS}")
        
        # Verificar si los archivos existen
        ruta_agente = os.path.join(RUTA_ASSETS, "agente.png")
        ruta_meta = os.path.join(RUTA_ASSETS, "meta.png")
        
        print(f"¿Existe archivo agente? {os.path.isfile(ruta_agente)}")
        print(f"¿Existe archivo meta? {os.path.isfile(ruta_meta)}")
        
        if not os.path.isfile(ruta_agente) or not os.path.isfile(ruta_meta):
            raise FileNotFoundError("No se encontraron los archivos de imagen")
        
        # Cargar imágenes
        img_agente = pygame.image.load(ruta_agente)
        img_meta = pygame.image.load(ruta_meta)
        
        # Convertir a formato con alpha para transparencia
        IMG_AGENTE = img_agente.convert_alpha()
        IMG_META = img_meta.convert_alpha()
        
        print("Imágenes cargadas correctamente")
        print(f"Dimensiones de imagen agente: {IMG_AGENTE.get_size()}")
        print(f"Dimensiones de imagen meta: {IMG_META.get_size()}")
    except Exception as e:
        print(f"Error al cargar imágenes: {e}")
        print(f"Detalles del error: {type(e).__name__}")
        # Las variables globales ya están inicializadas como None
    
    # Obtener dimensiones de la pantalla
    pantalla_info = pygame.display.Info()
    ANCHO_VENTANA = pantalla_info.current_w
    ALTO_VENTANA = pantalla_info.current_h
    
    # Calcular dimensiones relativas
    ANCHO_PANEL = int(ANCHO_VENTANA * 0.2)  # 20% del ancho
    ANCHO_ARBOL = int(ANCHO_VENTANA * 0.2)  # 20% del ancho
    ANCHO_LABERINTO = ANCHO_VENTANA - ANCHO_PANEL - ANCHO_ARBOL
    
    # Ajustar tamaño de celda dinámicamente
    FILAS = 10
    COLUMNAS = 10
    TAMANO_CELDA = (ALTO_VENTANA // FILAS) - MARGEN
    if TAMANO_CELDA < 10:  # Tamaño mínimo
        TAMANO_CELDA = 10
    
    # Configurar ventana en modo fullscreen
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.FULLSCREEN)
    
    # Crear laberinto con dimensiones ajustadas
    laberinto = Laberinto(FILAS, COLUMNAS, 0.4)
    
    # Usar un tamaño de ventana fijo para evitar problemas en pantalla completa
    ANCHO_VENTANA = ANCHO_PANEL + ANCHO_LABERINTO + ANCHO_ARBOL
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Laberinto Dinámico IA")
    
    # Crear laberinto y agente
    laberinto = Laberinto(17, 17, 0.8) #Hay que cambiar la densidad de las paredes dependiendo del tamaño del laberinto
    agente = Agente(laberinto.inicio)  
    
    # Variables de control
    reloj = pygame.time.Clock()
    ejecutando = False
    pasos = 0
    tiempo_inicio = None
    tiempo_final = None  # Añadir una variable para almacenar el tiempo final cuando se encuentra la meta
    modo_dinamico = False
    contador_dinamico = 10 
    velocidad = "Normal"
    mostrar_arbol = True    
    
    while True:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar que sea un clic izquierdo (botón 1)
                if evento.button == 1:  # 1 es el botón izquierdo
                    x, y = pygame.mouse.get_pos()
                    
                    # Crear una lista para almacenar todos los botones que fueron pulsados
                    botones_pulsados = []
                    
                    # Verificar todos los botones pulsados
                    for nombre, rect in botones:
                        if rect.collidepoint(x, y):
                            botones_pulsados.append(nombre)
                    
                    # Dar prioridad a los botones de algoritmo en orden inverso (A* primero)
                    algoritmos_rev = ["A*", "DFS", "BFS"]
                    for algoritmo in algoritmos_rev:
                        algo_nombre = f"algo_{algoritmo}"
                        if algo_nombre in botones_pulsados:
                            nuevo_algo = algoritmo
                            # Asegurarnos de que el algoritmo se cambia correctamente
                            agente.algoritmo_actual = nuevo_algo  # Establecer directamente
                            agente.cambiar_algoritmo(nuevo_algo)  # Y también llamar al método
                            
                            # Reiniciar el agente con el nuevo algoritmo para evitar comportamientos residuales
                            agente.reiniciar(laberinto.inicio)
                            
                            # Actualizar el estado visual
                            pasos = 0
                            tiempo_inicio = None
                            
                            # Mensaje de confirmación en la consola (opcional, para debugging)
                            print(f"Algoritmo cambiado a: {nuevo_algo}")
                            break
                    
                    # Procesar otros botones si no se seleccionó ningún algoritmo
                    for nombre in botones_pulsados:
                        if nombre == "inicio":
                            # Verificar que se haya seleccionado un algoritmo primero
                            if agente.algoritmo_actual is None:
                                # Mostrar mensaje o indicación visual de que debe seleccionar un algoritmo
                                print("Por favor seleccione un algoritmo primero")
                            else:
                                ejecutando = not ejecutando
                                if ejecutando:
                                    # Asegurarnos de que el algoritmo seleccionado se use
                                    print(f"Iniciando ejecución con algoritmo: {agente.algoritmo_actual}")
                                    agente.estado = "Buscando"
                                    if tiempo_inicio is None:
                                        tiempo_inicio = time.time()
                                else:
                                    agente.estado = "Pausado"
                            break
                        elif nombre == "reinicio":
                            agente.reiniciar(laberinto.inicio)
                            ejecutando = False
                            pasos = 0
                            tiempo_inicio = None
                            tiempo_final = None  # Reiniciar el tiempo final también
                            contador_dinamico = 10  
                        elif nombre == "arbol":
                            mostrar_arbol = not mostrar_arbol
                            break
                        elif nombre == "dinamico":
                            modo_dinamico = not modo_dinamico
                            break
                        elif nombre.startswith("vel_"):
                            velocidad = nombre.split("_")[1]
                            break
        
        # Actualizar estado del juego
        if ejecutando:
            # Verificar si el agente ya llegó a la meta para pausar el tiempo
            if agente.estado == "Meta encontrada":
                ejecutando = False
                # Guardar el tiempo final si no se ha guardado ya
                if tiempo_final is None and tiempo_inicio is not None:
                    tiempo_final = time.time() - tiempo_inicio
            else:
                # Solo actualizar si no ha llegado a la meta
                agente.actuar(laberinto)
                pasos += 1
                
                if modo_dinamico:
                    contador_dinamico -= 1
                    if contador_dinamico <= 0:
                        laberinto.cambiar_paredes_aleatorias(3)
                        contador_dinamico = 10 
        
        # Dibujar
        ventana.fill(COLORES["fondo"])  # Limpiar toda la ventana
        dibujar_laberinto(ventana, laberinto, agente)
        botones = dibujar_panel(ventana, agente, laberinto, pasos, tiempo_inicio, 
                               agente.estado, modo_dinamico, contador_dinamico, velocidad, mostrar_arbol, tiempo_final)
        if mostrar_arbol:
            dibujar_arbol_busqueda(ventana, agente)
        
        pygame.display.update()
        reloj.tick(obtener_fps_por_velocidad(velocidad))

if __name__ == "__main__":
    main()
