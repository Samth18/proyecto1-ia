# Importa pygame para la creación de la interfaz gráfica y manejo de eventos
import pygame
# Importa time para medir el tiempo de ejecución
import time
# Importa os para interactuar con el sistema operativo (rutas de archivos)
import os
# Importa la clase Laberinto desde el módulo core
from core.laberinto import Laberinto
# Importa la clase Agente desde el módulo core
from core.agente import Agente

# --- Constantes de Configuración ---
ANCHO_PANEL = 400 # Ancho del panel de control lateral
ALTO_PANEL = 1000 # Alto del panel (puede ser mayor que la ventana si hay scroll)
TAMANO_CELDA = 40 # Tamaño de cada celda del laberinto en píxeles
MARGEN = 2 # Margen entre celdas
ANCHO_LABERINTO = 900 # Ancho reservado para dibujar el laberinto
ANCHO_ARBOL = 520 # Ancho reservado para dibujar el árbol de búsqueda
ALTO_VENTANA = 800 # Altura inicial de la ventana

# --- Paleta de Colores ---
COLORES = {
    "pared": (0, 0, 0),          # Negro
    "camino": (224, 224, 224),   # Gris claro
    "agente": (0, 255, 0),       # Verde (usado como fallback si no hay imagen)
    "meta": (255, 0, 0),         # Rojo (usado como fallback si no hay imagen)
    "visitado": (173, 216, 230), # Azul claro para celdas exploradas
    "ruta": (255, 255, 0),       # Amarillo para el camino óptimo encontrado
    "fondo": (255, 255, 255),    # Blanco para el fondo general
    "panel": (240, 240, 240),    # Gris muy claro para el panel de control
    "borde_arbol": (220, 220, 220) # Borde para separar el área del árbol
}

def dibujar_laberinto(ventana, laberinto, agente):
    """Dibuja el estado actual del laberinto y el agente."""
    # Dibuja el fondo solo en el área del laberinto
    area_laberinto = pygame.Rect(ANCHO_PANEL, 0, ANCHO_LABERINTO, ALTO_VENTANA)
    pygame.draw.rect(ventana, COLORES["fondo"], area_laberinto)

    # Itera sobre cada celda del grid del laberinto
    for fila in range(laberinto.filas):
        for col in range(laberinto.columnas):
            # Calcula las coordenadas de dibujo, desplazadas por el panel
            x = ANCHO_PANEL + col * (TAMANO_CELDA + MARGEN)
            y = fila * (TAMANO_CELDA + MARGEN)

            # Determina el color de la celda según su estado
            if laberinto.grid[fila][col] == 1:
                color = COLORES["pared"]
            elif (fila, col) == laberinto.meta:
                color = COLORES["camino"] # Fondo para la imagen de la meta
            elif (fila, col) in agente.visitados:
                color = COLORES["visitado"]
            elif (fila, col) in agente.camino_optimo: # Resalta el camino óptimo
                color = COLORES["ruta"]
            else:
                color = COLORES["camino"]

            # Dibuja el rectángulo de la celda
            pygame.draw.rect(ventana, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))

            # Dibuja la imagen de la meta si está disponible
            if (fila, col) == laberinto.meta:
                if 'IMG_META' in globals() and IMG_META is not None:
                    try:
                        # Escala la imagen para que quepa en la celda
                        img_escalada = pygame.transform.scale(IMG_META, (TAMANO_CELDA - 4, TAMANO_CELDA - 4))
                        # Centra la imagen dentro de la celda
                        img_rect = img_escalada.get_rect(center=(x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2))
                        ventana.blit(img_escalada, img_rect)
                    except Exception as e: # Manejo de errores si falla la carga/dibujo
                        print(f"Error al dibujar meta: {e}")
                        pygame.draw.rect(ventana, COLORES["meta"], (x, y, TAMANO_CELDA, TAMANO_CELDA)) # Fallback a color sólido
                else:
                    pygame.draw.rect(ventana, COLORES["meta"], (x, y, TAMANO_CELDA, TAMANO_CELDA)) # Fallback si no hay imagen

    # Dibuja la imagen del agente si está disponible
    agente_x_centro = ANCHO_PANEL + agente.posicion[1] * (TAMANO_CELDA + MARGEN) + TAMANO_CELDA // 2
    agente_y_centro = agente.posicion[0] * (TAMANO_CELDA + MARGEN) + TAMANO_CELDA // 2

    if 'IMG_AGENTE' in globals() and IMG_AGENTE is not None:
        try:
            img_escalada = pygame.transform.scale(IMG_AGENTE, (TAMANO_CELDA - 4, TAMANO_CELDA - 4))
            img_rect = img_escalada.get_rect(center=(agente_x_centro, agente_y_centro))
            ventana.blit(img_escalada, img_rect)
        except Exception as e: # Manejo de errores
            print(f"Error al dibujar agente: {e}")
            pygame.draw.circle(ventana, COLORES["agente"], (agente_x_centro, agente_y_centro), TAMANO_CELDA // 4) # Fallback a círculo
    else:
        pygame.draw.circle(ventana, COLORES["agente"], (agente_x_centro, agente_y_centro), TAMANO_CELDA // 4) # Fallback si no hay imagen

def dibujar_panel(ventana, agente, laberinto, pasos, tiempo_inicio, estado, modo_dinamico,
                 contador_dinamico, velocidad, mostrar_arbol, tiempo_final=None,
                 modo_dinamico_algoritmos=False):
    """Dibuja el panel lateral con información y controles."""
    panel_x = 0 # El panel se dibuja en el borde izquierdo
    panel = pygame.Surface((ANCHO_PANEL, ALTO_PANEL)) # Crea una superficie para el panel
    panel.fill(COLORES["panel"]) # Rellena con color de fondo

    # Configuración de fuentes
    fuente = pygame.font.SysFont("Arial", 24)
    fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
    fuente_pequeña = pygame.font.SysFont("Arial", 20)

    # Dibuja el título del panel
    texto_titulo = fuente_titulo.render("Panel de Control", True, (0, 0, 0))
    panel.blit(texto_titulo, (100, 20)) # Posición relativa al panel

    # Calcula el tiempo transcurrido o muestra el tiempo final
    if tiempo_final is not None:
        tiempo_actual = tiempo_final # Usa el tiempo registrado al encontrar la meta
    else:
        tiempo_actual = time.time() - tiempo_inicio if tiempo_inicio else 0 # Calcula tiempo en vivo

    # Renderiza la información del estado actual
    texto_algoritmo = fuente.render(f"Algoritmo: {agente.algoritmo_actual}", True, (0, 0, 0))
    texto_pasos = fuente.render(f"Pasos: {pasos}", True, (0, 0, 0))
    texto_tiempo = fuente.render(f"Tiempo: {tiempo_actual:.1f}s", True, (0, 0, 0))
    texto_estado = fuente.render(f"Estado: {agente.estado}", True, (0, 0, 0))
    texto_dinamico = fuente.render(f"Modo Dinámico: {'Activado' if modo_dinamico else 'Desactivado'}", True, (0, 0, 0))
    texto_dinamico_algo = fuente.render(f"Algoritmos Dinámicos: {'Activado' if modo_dinamico_algoritmos else 'Desactivado'}", True, (0, 0, 0))
    # Muestra el contador regresivo para cambios dinámicos, en rojo si está cerca
    texto_contador = fuente.render(f"Cambios en: {contador_dinamico}", True, (0, 0, 0) if contador_dinamico > 1 else (255, 0, 0))

    # Dibuja la información en el panel
    panel.blit(texto_algoritmo, (20, 80))
    panel.blit(texto_pasos, (20, 120))
    panel.blit(texto_tiempo, (20, 160))
    panel.blit(texto_estado, (20, 200))
    panel.blit(texto_dinamico, (20, 240))
    panel.blit(texto_dinamico_algo, (20, 280))

    # Muestra el contador solo si algún modo dinámico está activo
    if modo_dinamico or modo_dinamico_algoritmos:
        panel.blit(texto_contador, (20, 320))

    # --- Dibuja los Botones ---
    botones = [] # Lista para almacenar las áreas de los botones y sus nombres
    y_offset = 360 if (modo_dinamico or modo_dinamico_algoritmos) else 320 # Ajusta la posición inicial de los botones

    # Botón Inicio/Pausa
    boton_inicio = pygame.Rect(50, y_offset, 300, 50)
    pygame.draw.rect(panel, (100, 180, 100), boton_inicio) # Color verde
    texto_inicio = fuente.render("Iniciar/Pausar", True, (0, 0, 0))
    panel.blit(texto_inicio, (130, y_offset + 15)) # Centra el texto
    botones.append(("inicio", boton_inicio.move(panel_x, 0))) # Guarda el botón con coordenadas absolutas
    y_offset += 60 # Incrementa la posición Y para el siguiente botón

    # Botón Reiniciar
    boton_reinicio = pygame.Rect(50, y_offset, 300, 50)
    pygame.draw.rect(panel, (180, 100, 100), boton_reinicio) # Color rojo
    texto_reinicio = fuente.render("Reiniciar", True, (0, 0, 0))
    panel.blit(texto_reinicio, (150, y_offset + 15))
    botones.append(("reinicio", boton_reinicio.move(panel_x, 0)))
    y_offset += 60

    # Botón Mostrar/Ocultar Árbol
    boton_arbol = pygame.Rect(50, y_offset, 300, 50)
    color_arbol = (150, 150, 220) if mostrar_arbol else (200, 200, 200) # Cambia color si está activo
    pygame.draw.rect(panel, color_arbol, boton_arbol)
    texto_arbol = fuente.render("Mostrar/Ocultar Árbol", True, (0, 0, 0))
    panel.blit(texto_arbol, (95, y_offset + 15))
    botones.append(("arbol", boton_arbol.move(panel_x, 0)))
    y_offset += 60

    # Botón Modo Dinámico (cambia paredes y meta)
    boton_dinamico = pygame.Rect(50, y_offset, 300, 50)
    color_dinamico = (150, 150, 220) if modo_dinamico else (200, 200, 200)
    pygame.draw.rect(panel, color_dinamico, boton_dinamico)
    texto_dinamico_btn = fuente.render("Modo Dinámico", True, (0, 0, 0)) # Renombrado para evitar conflicto
    panel.blit(texto_dinamico_btn, (130, y_offset + 15))
    botones.append(("dinamico", boton_dinamico.move(panel_x, 0)))
    y_offset += 60

    # Botón Modo Dinámico con Algoritmos (sugiere algoritmos)
    boton_dinamico_algo = pygame.Rect(50, y_offset, 300, 50)
    color_dinamico_algo = (100, 200, 150) if modo_dinamico_algoritmos else (200, 200, 200)
    pygame.draw.rect(panel, color_dinamico_algo, boton_dinamico_algo)
    texto_dinamico_algo_btn = fuente.render("Algoritmos Dinámicos", True, (0, 0, 0)) # Renombrado
    panel.blit(texto_dinamico_algo_btn, (110, y_offset + 15))
    botones.append(("dinamico_algo", boton_dinamico_algo.move(panel_x, 0)))
    y_offset += 60

    # Sección para seleccionar el algoritmo manualmente
    texto_seleccion = fuente.render("Seleccionar Algoritmo:", True, (0, 0, 0))
    panel.blit(texto_seleccion, (20, y_offset))
    y_offset += 40

    algoritmos = ["BFS", "DFS", "A*", "IDS"]
    for algo in algoritmos:
        boton_algo = pygame.Rect(50, y_offset, 300, 40)
        # Resalta el botón del algoritmo actualmente seleccionado
        if algo == agente.algoritmo_actual:
            pygame.draw.rect(panel, (150, 150, 220), boton_algo) # Color azul claro
        else:
            pygame.draw.rect(panel, (200, 200, 200), boton_algo) # Color gris
        texto_algo = fuente.render(algo, True, (0, 0, 0))
        panel.blit(texto_algo, (180, y_offset + 10)) # Centra el texto del algoritmo
        botones.append((f"algo_{algo}", boton_algo.move(panel_x, 0))) # Guarda el botón con prefijo "algo_"
        y_offset += 50

    # Sección para controlar la velocidad de ejecución
    texto_velocidad = fuente.render("Velocidad:", True, (0, 0, 0))
    panel.blit(texto_velocidad, (20, y_offset))
    y_offset += 40

    velocidades = ["Lenta", "Normal"] # Opciones de velocidad
    x_vel = 50 # Posición X inicial para los botones de velocidad
    for vel in velocidades:
        boton_vel = pygame.Rect(x_vel, y_offset, 140, 40) # Ancho ajustado
        # Resalta el botón de la velocidad actual
        color_vel = (150, 220, 150) if vel == velocidad else (200, 200, 200)
        pygame.draw.rect(panel, color_vel, boton_vel)
        texto_vel = fuente_pequeña.render(vel, True, (0, 0, 0))
        # Centra el texto dentro del botón de velocidad
        panel.blit(texto_vel, (x_vel + 70 - texto_vel.get_width()//2, y_offset + 10))
        botones.append((f"vel_{vel}", boton_vel.move(panel_x, 0))) # Guarda el botón con prefijo "vel_"
        x_vel += 160 # Incrementa la posición X para el siguiente botón

    # Dibuja el panel completo sobre la ventana principal
    ventana.blit(panel, (panel_x, 0))
    return botones # Devuelve la lista de botones para la detección de clics

def dibujar_arbol_busqueda(ventana, agente):
    """Dibuja la visualización del árbol de búsqueda generado por el agente."""
    # Calcula la posición X donde empieza el área del árbol
    arbol_x = ANCHO_PANEL + ANCHO_LABERINTO

    # Dibuja un rectángulo de fondo y borde para el área del árbol
    pygame.draw.rect(ventana, COLORES["borde_arbol"], pygame.Rect(arbol_x, 0, ANCHO_ARBOL, ALTO_VENTANA))

    # Dibuja el título del área del árbol
    fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
    titulo = fuente_titulo.render("Árbol de Búsqueda", True, (0, 0, 0))
    ventana.blit(titulo, (arbol_x + 100, 20)) # Posición relativa al área del árbol

    # Obtiene la superficie (imagen) del árbol desde el visualizador del agente
    superficie_arbol = agente.obtener_superficie_arbol()
    if superficie_arbol:
        # Dibuja la superficie del árbol en la ventana
        ventana.blit(superficie_arbol, (arbol_x, 60)) # Con un pequeño margen

def obtener_fps_por_velocidad(velocidad):
    """Devuelve la tasa de fotogramas por segundo (FPS) según la velocidad seleccionada."""
    if velocidad == "Lenta":
        return 3 # Ejecución más lenta
    elif velocidad == "Normal":
        return 8 # Ejecución normal
    return 12 # Valor por defecto (no usado actualmente)

def main():
    """Función principal que inicializa y ejecuta el bucle del juego."""
    pygame.init() # Inicializa todos los módulos de pygame

    # Variables globales para almacenar las imágenes cargadas
    global IMG_AGENTE, IMG_META
    IMG_AGENTE = None
    IMG_META = None

    # Obtiene las dimensiones de la pantalla para ajustar la ventana
    pantalla_info = pygame.display.Info()
    ANCHO_VENTANA_TOTAL = pantalla_info.current_w
    ALTO_VENTANA_TOTAL = pantalla_info.current_h

    # Calcula dimensiones relativas de los paneles y el laberinto
    ANCHO_PANEL_CALC = int(ANCHO_VENTANA_TOTAL * 0.21)
    # REDUCIMOS LA PROPORCIÓN PARA EL ÁRBOL
    ANCHO_ARBOL_CALC = int(ANCHO_VENTANA_TOTAL * 0.27)
    ANCHO_LABERINTO_CALC = ANCHO_VENTANA_TOTAL - ANCHO_PANEL_CALC - ANCHO_ARBOL_CALC

    # Define el tamaño del laberinto (filas y columnas)
    FILAS = 10
    COLUMNAS = 10
    # Calcula el tamaño de celda óptimo basado en la altura disponible
    TAMANO_CELDA_CALC = int(((ALTO_VENTANA_TOTAL // FILAS) - MARGEN)/ 1.1)
    if TAMANO_CELDA_CALC < 8: # Asegura un tamaño mínimo de celda (ajustado si es necesario)
        TAMANO_CELDA_CALC = 8

    # Actualiza las constantes globales con los valores calculados
    global ANCHO_PANEL, ANCHO_LABERINTO, ANCHO_ARBOL, TAMANO_CELDA, ALTO_VENTANA
    ANCHO_PANEL = ANCHO_PANEL_CALC
    ANCHO_LABERINTO = ANCHO_LABERINTO_CALC
    ANCHO_ARBOL = ANCHO_ARBOL_CALC
    TAMANO_CELDA = TAMANO_CELDA_CALC
    ALTO_VENTANA = ALTO_VENTANA_TOTAL # Usa la altura total de la pantalla

    # Configura la ventana principal (inicialmente en pantalla completa, luego se ajusta)
    # ventana = pygame.display.set_mode((ANCHO_VENTANA_TOTAL, ALTO_VENTANA_TOTAL), pygame.FULLSCREEN)
    # Se usa un tamaño fijo después para evitar problemas con coordenadas
    ANCHO_VENTANA_FINAL = ANCHO_PANEL + ANCHO_LABERINTO + ANCHO_ARBOL
    ventana = pygame.display.set_mode((ANCHO_VENTANA_FINAL, ALTO_VENTANA))
    pygame.display.set_caption("Laberinto Dinámico IA") # Título de la ventana

    # --- Carga de Imágenes ---
    try:
        # Obtiene la ruta absoluta del script actual (gui.py)
        script_path = os.path.abspath(__file__)
        # Obtiene el directorio que contiene el script (interfaz)
        script_dir = os.path.dirname(script_path)
        # Construye la ruta a la carpeta 'assets' dentro del directorio 'interfaz'
        RUTA_ASSETS = os.path.join(script_dir, "assets")

        print(f"Buscando imágenes en: {RUTA_ASSETS}") # Mensaje de depuración

        # Construye las rutas completas a los archivos de imagen
        ruta_agente = os.path.join(RUTA_ASSETS, "agente.png")
        ruta_meta = os.path.join(RUTA_ASSETS, "meta.png")

        # Verifica si los archivos existen antes de intentar cargarlos
        print(f"¿Existe archivo agente? {os.path.isfile(ruta_agente)}")
        print(f"¿Existe archivo meta? {os.path.isfile(ruta_meta)}")

        if not os.path.isfile(ruta_agente) or not os.path.isfile(ruta_meta):
            raise FileNotFoundError("No se encontraron los archivos de imagen en la ruta esperada.")

        # Carga las imágenes desde los archivos
        img_agente = pygame.image.load(ruta_agente)
        img_meta = pygame.image.load(ruta_meta)

        # Convierte las imágenes a un formato con canal alfa (transparencia) para mejor rendimiento
        IMG_AGENTE = img_agente.convert_alpha()
        IMG_META = img_meta.convert_alpha()

        print("Imágenes cargadas correctamente") # Mensaje de éxito
        print(f"Dimensiones de imagen agente: {IMG_AGENTE.get_size()}")
        print(f"Dimensiones de imagen meta: {IMG_META.get_size()}")
    except Exception as e: # Captura cualquier error durante la carga
        print(f"Error al cargar imágenes: {e}")
        print(f"Detalles del error: {type(e).__name__}")
        # Las variables IMG_AGENTE e IMG_META permanecerán como None

    # --- Inicialización del Laberinto y Agente ---
    # Crea una instancia del laberinto con las dimensiones calculadas y densidad de paredes
    laberinto = Laberinto(FILAS, COLUMNAS, 0.4) # Densidad 0.4 = 40% de paredes
    # Crea una instancia del agente, iniciando en la posición inicial del laberinto
    agente = Agente(laberinto.inicio)

    # --- Variables de Control del Bucle Principal ---
    reloj = pygame.time.Clock() # Objeto para controlar los FPS
    ejecutando = False # Indica si la simulación está corriendo o pausada
    pasos = 0 # Contador de pasos del agente
    tiempo_inicio = None # Marca de tiempo cuando se inicia la ejecución
    tiempo_final = None # Marca de tiempo cuando se encuentra la meta
    modo_dinamico = False # Controla si el laberinto cambia paredes y meta
    contador_dinamico = 5 # Contador regresivo para activar cambios dinámicos
    velocidad = "Normal" # Velocidad inicial de ejecución
    mostrar_arbol = True # Controla si se muestra el árbol de búsqueda
    modo_dinamico_algoritmos = False # Controla si se sugieren algoritmos dinámicamente

    # --- Bucle Principal del Juego ---
    while True:
        # --- Manejo de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # Evento de cerrar la ventana
                pygame.quit()
                return # Termina la ejecución
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: # Tecla Escape para salir
                    pygame.quit()
                    return
            elif evento.type == pygame.MOUSEBUTTONDOWN: # Evento de clic del ratón
                if evento.button == 1: # Botón izquierdo del ratón
                    x, y = pygame.mouse.get_pos() # Obtiene las coordenadas del clic

                    # Verifica qué botón(es) fueron presionados
                    botones_pulsados = []
                    for nombre, rect in botones: # Itera sobre los botones dibujados
                        if rect.collidepoint(x, y): # Comprueba si el clic está dentro del área del botón
                            botones_pulsados.append(nombre)

                    # --- Lógica de Botones ---
                    # Prioriza la selección de algoritmo si se hizo clic en uno
                    algoritmo_seleccionado = False
                    algoritmos_rev = ["A*", "DFS", "BFS", "IDS"] # Orden para probar (A* primero)
                    for algoritmo in algoritmos_rev:
                        algo_nombre = f"algo_{algoritmo}"
                        if algo_nombre in botones_pulsados:
                            nuevo_algo = algoritmo
                            agente.cambiar_algoritmo(nuevo_algo) # Llama al método del agente para cambiar
                            agente.reiniciar(laberinto.inicio) # Reinicia estado del agente
                            # Reinicia contadores y estado de ejecución
                            ejecutando = False
                            pasos = 0
                            tiempo_inicio = None
                            tiempo_final = None
                            print(f"Algoritmo cambiado manualmente a: {nuevo_algo}")
                            algoritmo_seleccionado = True
                            break # Sale del bucle una vez que se selecciona un algoritmo

                    # Si no se seleccionó un algoritmo, procesa otros botones
                    if not algoritmo_seleccionado:
                        for nombre in botones_pulsados:
                            if nombre == "inicio":
                                if agente.algoritmo_actual is None: # Requiere seleccionar algoritmo primero
                                    print("Por favor seleccione un algoritmo primero")
                                else:
                                    ejecutando = not ejecutando # Alterna entre iniciar y pausar
                                    if ejecutando:
                                        agente.estado = "Buscando" # Inicia la búsqueda
                                        if tiempo_inicio is None: # Inicia el temporizador si no estaba corriendo
                                            tiempo_inicio = time.time()
                                    else:
                                        agente.estado = "Pausado" # Pausa la búsqueda
                                break # Sale después de procesar inicio/pausa
                            elif nombre == "reinicio":
                                agente.reiniciar(laberinto.inicio) # Reinicia el agente
                                laberinto.generar_laberinto() # Genera un nuevo laberinto
                                # Reinicia variables de estado
                                ejecutando = False
                                pasos = 0
                                tiempo_inicio = None
                                tiempo_final = None
                                contador_dinamico = 5 # Reinicia contador dinámico
                                break
                            elif nombre == "arbol":
                                mostrar_arbol = not mostrar_arbol # Alterna la visibilidad del árbol
                                break
                            elif nombre == "dinamico":
                                modo_dinamico = not modo_dinamico # Alterna modo dinámico (paredes/meta)
                                # Desactiva el otro modo dinámico si este se activa
                                if modo_dinamico and modo_dinamico_algoritmos:
                                    modo_dinamico_algoritmos = False
                                    laberinto.modo_dinamico_algoritmos = False # Sincroniza con laberinto
                                contador_dinamico = 5 # Reinicia contador
                                break
                            elif nombre == "dinamico_algo":
                                modo_dinamico_algoritmos = not modo_dinamico_algoritmos # Alterna modo dinámico (algoritmos)
                                laberinto.cambiar_modo_dinamico_algoritmos() # Llama al método del laberinto
                                # Desactiva el otro modo dinámico si este se activa
                                if modo_dinamico_algoritmos and modo_dinamico:
                                    modo_dinamico = False
                                contador_dinamico = 5 # Reinicia contador
                                break
                            elif nombre.startswith("vel_"): # Si se hizo clic en un botón de velocidad
                                velocidad = nombre.split("_")[1] # Extrae el nombre de la velocidad
                                break

        # --- Actualización del Estado del Juego ---
        if ejecutando:
            # Si el agente ya encontró la meta, detiene la ejecución y registra el tiempo final
            if agente.estado == "Meta encontrada":
                ejecutando = False
                if tiempo_final is None and tiempo_inicio is not None:
                    tiempo_final = time.time() - tiempo_inicio
            else:
                # Si no ha llegado a la meta, el agente actúa
                agente.actuar(laberinto)
                pasos += 1 # Incrementa el contador de pasos

                # Lógica para el modo dinámico (cambio de paredes y meta)
                if modo_dinamico:
                    contador_dinamico -= 1 # Decrementa el contador en cada paso
                    if contador_dinamico <= 0:
                        print("Modo dinámico: Cambiando laberinto y meta...")
                        laberinto.cambiar_paredes_aleatorias(8) # Cambia más paredes
                        laberinto.randomizar_meta(agente.posicion) # Mueve la meta aleatoriamente
                        # Reinicia parcialmente el agente para que recalcule desde su posición actual
                        agente.ultimo_camino = None
                        agente.estado = "Buscando"
                        tiempo_final = None # Resetea tiempo final si la meta cambió
                        contador_dinamico = 5 # Reinicia el contador

                # Lógica para el modo dinámico de algoritmos
                elif modo_dinamico_algoritmos:
                    # Decrementa el contador usando el método del laberinto
                    if laberinto.decrementar_contador_dinamico():
                        print("Modo Algoritmos Dinámicos: Evaluando situación...")
                        # Pide al laberinto que actualice y sugiera un algoritmo
                        cambios = laberinto.actualizar_dinamico_con_algoritmos(agente.posicion)

                        # Si se sugiere un nuevo algoritmo y es diferente al actual, lo cambia
                        if cambios['algoritmo_sugerido'] and cambios['algoritmo_sugerido'] != agente.algoritmo_actual:
                            nuevo_algo = cambios['algoritmo_sugerido']
                            print(f"Cambiando algoritmo de {agente.algoritmo_actual} a {nuevo_algo}")
                            agente.cambiar_algoritmo(nuevo_algo) # Cambia el algoritmo en el agente

                        # Si la meta cambió, fuerza al agente a recalcular
                        if cambios['meta_cambiada']:
                            print(f"Meta cambiada a {laberinto.meta}")
                            agente.estado = "Buscando"
                            agente.ultimo_camino = None
                            tiempo_final = None # Resetea tiempo final

                        # El contador se reinicia dentro de decrementar_contador_dinamico

                    # Actualiza el contador local para mostrarlo en el panel
                    contador_dinamico = laberinto.contador_dinamico


        # --- Dibujado ---
        ventana.fill(COLORES["fondo"]) # Limpia la pantalla en cada fotograma
        dibujar_laberinto(ventana, laberinto, agente) # Dibuja el laberinto y el agente
        # Dibuja el panel y obtiene las áreas de los botones actualizadas
        botones = dibujar_panel(ventana, agente, laberinto, pasos, tiempo_inicio,
                               agente.estado, modo_dinamico, contador_dinamico,
                               velocidad, mostrar_arbol, tiempo_final,
                               modo_dinamico_algoritmos)
        if mostrar_arbol: # Dibuja el árbol solo si está activado
            dibujar_arbol_busqueda(ventana, agente)

        pygame.display.update() # Actualiza la pantalla para mostrar los cambios
        # Controla los FPS según la velocidad seleccionada
        reloj.tick(obtener_fps_por_velocidad(velocidad))

# Punto de entrada del programa: si se ejecuta este script directamente, llama a main()
if __name__ == "__main__":
    main()
