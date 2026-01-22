"""
╔═══════════════════════════════════════════════════════════════╗
║           CALCULADORA CON GESTOS DE MANOS                     ║
║                                                               ║
║  FASE 1: Seleccionar operación con 1 mano (1-4 dedos)         ║
║  FASE 2: Mostrar números con ambas manos para calcular        ║
║                                                               ║
║  Autor: Creado con MediaPipe Tasks API + OpenCV               ║
╚═══════════════════════════════════════════════════════════════╝
"""

import cv2
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import os
import urllib.request

# ============================================
# DESCARGAR MODELO SI NO EXISTE
# ============================================

model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")

if not os.path.exists(model_path):
    print("=" * 60)
    print("  Descargando modelo de detección de manos...")
    print("=" * 60)
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    try:
        urllib.request.urlretrieve(url, model_path)
        print("  ✓ Modelo descargado correctamente!")
    except Exception as e:
        print(f"  ✗ Error al descargar el modelo: {e}")
        print("  Por favor descarga manualmente desde:")
        print(f"  {url}")
        exit(1)

# ============================================
# CONFIGURACIÓN DE MEDIAPIPE TASKS
# ============================================

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=20,  # Aumentado para detectar múltiples manos/personas
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)
hand_detector = vision.HandLandmarker.create_from_options(options)

# ============================================
# CONFIGURACIÓN DE LA CÁMARA
# ============================================

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# ============================================
# VARIABLES DEL PROGRAMA
# ============================================

fase_actual = "seleccion"
operacion_seleccionada = None

operaciones = {
    1: {"nombre": "SUMA", "simbolo": "+", "emoji": "☝️", "color": (50, 205, 50)},
    2: {"nombre": "RESTA", "simbolo": "-", "emoji": "✌️", "color": (255, 165, 0)},
    3: {"nombre": "MULTI", "simbolo": "×", "emoji": "🤟", "color": (186, 85, 211)},
    4: {"nombre": "DIVIS", "simbolo": "÷", "emoji": "🖐️", "color": (30, 144, 255)}
}

dedos_detectados = 0
tiempo_inicio_deteccion = None
TIEMPO_CONFIRMACION = 2.0

# Paleta de colores moderna (BGR)
COLORES = {
    "primario": (255, 87, 51),      # Coral
    "secundario": (50, 205, 50),    # Verde lima
    "acento": (255, 215, 0),        # Dorado
    "texto": (255, 255, 255),       # Blanco
    "sombra": (40, 40, 40),         # Gris oscuro
    "fondo_panel": (30, 30, 30),    # Negro suave
    "exito": (0, 255, 127),         # Verde primavera
    "error": (71, 99, 255),         # Rojo coral
    "cyan": (255, 255, 0),          # Cyan
    "rosa": (203, 192, 255),        # Rosa
}

# Índices de las puntas de los dedos
TIP_IDS = [4, 8, 12, 16, 20]

# ============================================
# FUNCIONES DE DISEÑO
# ============================================

def crear_overlay(img, alpha=0.6):
    """Crea una capa semitransparente sobre la imagen"""
    overlay = img.copy()
    return overlay


def dibujar_panel_redondeado(img, x, y, w, h, color, alpha=0.7, radio=15):
    """Dibuja un panel con esquinas redondeadas y transparencia"""
    overlay = img.copy()
    
    # Dibujar rectángulo principal
    cv2.rectangle(overlay, (x + radio, y), (x + w - radio, y + h), color, -1)
    cv2.rectangle(overlay, (x, y + radio), (x + w, y + h - radio), color, -1)
    
    # Dibujar esquinas redondeadas
    cv2.circle(overlay, (x + radio, y + radio), radio, color, -1)
    cv2.circle(overlay, (x + w - radio, y + radio), radio, color, -1)
    cv2.circle(overlay, (x + radio, y + h - radio), radio, color, -1)
    cv2.circle(overlay, (x + w - radio, y + h - radio), radio, color, -1)
    
    # Aplicar transparencia
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    
    # Borde
    cv2.rectangle(img, (x, y), (x + w, y + h), (80, 80, 80), 1)


def dibujar_texto_con_sombra(img, texto, posicion, escala=1, color=(255, 255, 255), grosor=2):
    """Dibuja texto con efecto de sombra suave"""
    x, y = posicion
    fuente = cv2.FONT_HERSHEY_SIMPLEX
    
    # Sombra
    cv2.putText(img, texto, (x + 2, y + 2), fuente, escala, (0, 0, 0), grosor + 1, cv2.LINE_AA)
    # Texto principal
    cv2.putText(img, texto, (x, y), fuente, escala, color, grosor, cv2.LINE_AA)


def dibujar_texto_centrado(img, texto, y, escala=1, color=(255, 255, 255), grosor=2):
    """Dibuja texto centrado horizontalmente"""
    fuente = cv2.FONT_HERSHEY_SIMPLEX
    (ancho, _), _ = cv2.getTextSize(texto, fuente, escala, grosor)
    x = (img.shape[1] - ancho) // 2
    dibujar_texto_con_sombra(img, texto, (x, y), escala, color, grosor)


def dibujar_barra_progreso(img, x, y, ancho, alto, progreso, color_fondo, color_barra):
    """Dibuja una barra de progreso elegante"""
    # Fondo de la barra
    cv2.rectangle(img, (x, y), (x + ancho, y + alto), color_fondo, -1)
    cv2.rectangle(img, (x, y), (x + ancho, y + alto), (100, 100, 100), 2)
    
    # Progreso
    progreso_ancho = int(ancho * progreso)
    if progreso_ancho > 0:
        # Gradiente simulado
        for i in range(progreso_ancho):
            ratio = i / ancho
            b = int(color_barra[0] * (1 - ratio * 0.3))
            g = int(color_barra[1] * (1 - ratio * 0.3))
            r = int(color_barra[2] * (1 - ratio * 0.3))
            cv2.line(img, (x + i, y), (x + i, y + alto), (b, g, r), 1)
    
    # Borde brillante
    cv2.rectangle(img, (x, y), (x + progreso_ancho, y + alto), (255, 255, 255), 1)


def dibujar_circulo_numero(img, x, y, numero, color, radio=60):
    """Dibuja un círculo grande con un número dentro"""
    # Sombra del círculo
    cv2.circle(img, (x + 3, y + 3), radio, (20, 20, 20), -1)
    # Círculo principal
    cv2.circle(img, (x, y), radio, color, -1)
    # Borde brillante
    cv2.circle(img, (x, y), radio, (255, 255, 255), 3)
    cv2.circle(img, (x, y), radio - 5, color, 2)
    
    # Número centrado
    texto = str(numero)
    fuente = cv2.FONT_HERSHEY_SIMPLEX
    escala = 2.5
    (tw, th), _ = cv2.getTextSize(texto, fuente, escala, 4)
    tx = x - tw // 2
    ty = y + th // 2
    cv2.putText(img, texto, (tx + 2, ty + 2), fuente, escala, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(img, texto, (tx, ty), fuente, escala, (255, 255, 255), 4, cv2.LINE_AA)


def dibujar_linea_divisora(img):
    """Dibuja una línea divisora vertical sutil en el centro de la pantalla"""
    h, w, _ = img.shape
    centro_x = w // 2
    
    # Línea punteada muy sutil con baja opacidad
    color_linea = (80, 80, 80)  # Gris oscuro sutil
    
    # Dibujar línea punteada (segmentos pequeños)
    segmento_largo = 15
    espacio = 20
    y = 0
    while y < h:
        y_fin = min(y + segmento_largo, h)
        cv2.line(img, (centro_x, y), (centro_x, y_fin), color_linea, 1, cv2.LINE_AA)
        y += segmento_largo + espacio


def dibujar_landmarks(img, hand_landmarks, handedness):
    """Dibuja los landmarks de la mano con estilo mejorado"""
    h, w, _ = img.shape
    
    puntos = []
    for landmark in hand_landmarks:
        px = int(landmark.x * w)
        py = int(landmark.y * h)
        puntos.append((px, py))
    
    conexiones = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (0, 9), (9, 10), (10, 11), (11, 12),
        (0, 13), (13, 14), (14, 15), (15, 16),
        (0, 17), (17, 18), (18, 19), (19, 20),
        (5, 9), (9, 13), (13, 17)
    ]
    
    # Dibujar conexiones con gradiente
    for conexion in conexiones:
        pt1 = puntos[conexion[0]]
        pt2 = puntos[conexion[1]]
        cv2.line(img, pt1, pt2, COLORES["cyan"], 3, cv2.LINE_AA)
        cv2.line(img, pt1, pt2, (255, 255, 255), 1, cv2.LINE_AA)
    
    # Dibujar puntos
    for i, punto in enumerate(puntos):
        if i in TIP_IDS:
            cv2.circle(img, punto, 10, COLORES["error"], -1)
            cv2.circle(img, punto, 10, (255, 255, 255), 2)
        else:
            cv2.circle(img, punto, 6, COLORES["secundario"], -1)
            cv2.circle(img, punto, 6, (255, 255, 255), 1)
    
    # Bounding box elegante
    x_coords = [p[0] for p in puntos]
    y_coords = [p[1] for p in puntos]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    
    padding = 25
    # Esquinas decorativas
    largo = 20
    cv2.line(img, (x_min - padding, y_min - padding), (x_min - padding + largo, y_min - padding), COLORES["acento"], 3)
    cv2.line(img, (x_min - padding, y_min - padding), (x_min - padding, y_min - padding + largo), COLORES["acento"], 3)
    
    cv2.line(img, (x_max + padding, y_min - padding), (x_max + padding - largo, y_min - padding), COLORES["acento"], 3)
    cv2.line(img, (x_max + padding, y_min - padding), (x_max + padding, y_min - padding + largo), COLORES["acento"], 3)
    
    cv2.line(img, (x_min - padding, y_max + padding), (x_min - padding + largo, y_max + padding), COLORES["acento"], 3)
    cv2.line(img, (x_min - padding, y_max + padding), (x_min - padding, y_max + padding - largo), COLORES["acento"], 3)
    
    cv2.line(img, (x_max + padding, y_max + padding), (x_max + padding - largo, y_max + padding), COLORES["acento"], 3)
    cv2.line(img, (x_max + padding, y_max + padding), (x_max + padding, y_max + padding - largo), COLORES["acento"], 3)


def contar_dedos(hand_landmarks, handedness, img_width, img_height):
    """
    Cuenta cuántos dedos están levantados usando un algoritmo mejorado.
    Compara la posición de las puntas con las articulaciones intermedias.
    """
    dedos = []
    
    # Convertir landmarks a coordenadas de píxeles
    landmarks = []
    for lm in hand_landmarks:
        landmarks.append({
            'x': lm.x * img_width,
            'y': lm.y * img_height,
            'z': lm.z
        })
    
    # ===== PULGAR =====
    # El pulgar se detecta comparando la distancia horizontal
    # Punto 4 (punta) vs Punto 3 (articulación) vs Punto 2 (base)
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]  # Articulación intermedia
    thumb_mcp = landmarks[2]  # Base del pulgar
    wrist = landmarks[0]  # Muñeca
    
    # Calcular si el pulgar está extendido
    # Comparamos la distancia de la punta al centro de la palma
    palm_center_x = (landmarks[0]['x'] + landmarks[9]['x']) / 2
    
    # Para mano derecha (en imagen volteada aparece como Left en la detección)
    if handedness == "Right":
        # El pulgar está arriba si la punta está más a la derecha que la articulación
        if thumb_tip['x'] > thumb_ip['x'] + 20:  # Margen de 20 píxeles
            dedos.append(1)
        else:
            dedos.append(0)
    else:  # Left
        # El pulgar está arriba si la punta está más a la izquierda que la articulación
        if thumb_tip['x'] < thumb_ip['x'] - 20:
            dedos.append(1)
        else:
            dedos.append(0)
    
    # ===== OTROS 4 DEDOS (índice, medio, anular, meñique) =====
    # Se detectan comparando la posición Y de la punta con la articulación PIP
    # Índices: 8,12,16,20 (puntas) vs 6,10,14,18 (PIP - articulación media)
    
    dedos_indices = [
        (8, 6, 5),   # Índice: punta, PIP, MCP
        (12, 10, 9), # Medio: punta, PIP, MCP
        (16, 14, 13),# Anular: punta, PIP, MCP
        (20, 18, 17) # Meñique: punta, PIP, MCP
    ]
    
    for tip_id, pip_id, mcp_id in dedos_indices:
        tip = landmarks[tip_id]
        pip = landmarks[pip_id]
        mcp = landmarks[mcp_id]
        
        # El dedo está levantado si la punta está significativamente más arriba que PIP
        # Usamos un umbral proporcional a la distancia entre articulaciones
        distancia_ref = abs(pip['y'] - mcp['y'])
        umbral = max(distancia_ref * 0.3, 15)  # Al menos 15 píxeles o 30% de la distancia
        
        if tip['y'] < pip['y'] - umbral:
            dedos.append(1)
        else:
            dedos.append(0)
    
    return sum(dedos)


def obtener_centro_mano(hand_landmarks, img_width, img_height):
    """Obtiene el centro de la mano"""
    landmark = hand_landmarks[9]
    return int(landmark.x * img_width), int(landmark.y * img_height)


def procesar_manos(detection_result, img):
    """Procesa el resultado de la detección de manos"""
    manos = []
    h, w, _ = img.shape
    
    if detection_result.hand_landmarks:
        for i, hand_landmarks in enumerate(detection_result.hand_landmarks):
            handedness = detection_result.handedness[i][0].category_name
            num_dedos = contar_dedos(hand_landmarks, handedness, w, h)
            centro = obtener_centro_mano(hand_landmarks, w, h)
            dibujar_landmarks(img, hand_landmarks, handedness)
            
            manos.append({
                "handedness": handedness,
                "dedos": num_dedos,
                "centro_x": centro[0],
                "centro_y": centro[1],
                "landmarks": hand_landmarks
            })
    
    return manos


def dibujar_menu(img):
    """Dibuja el menú de selección en el lateral izquierdo"""
    h, w, _ = img.shape
    
    # Panel lateral izquierdo con título y opciones
    panel_w = 280
    dibujar_panel_redondeado(img, 10, 10, panel_w, 280, (20, 20, 20), 0.75)
    
    # Título
    dibujar_texto_con_sombra(img, "CALCULADORA", (25, 45), 0.8, COLORES["acento"], 2)
    dibujar_texto_con_sombra(img, "CON GESTOS", (25, 75), 0.7, COLORES["texto"], 1)
    
    # Línea separadora
    cv2.line(img, (25, 90), (panel_w - 15, 90), (80, 80, 80), 1)
    
    # Subtítulo
    dibujar_texto_con_sombra(img, "Selecciona:", (25, 115), 0.55, COLORES["rosa"], 1)
    
    opciones = [
        ("1 = SUMA  +", operaciones[1]["color"]),
        ("2 = RESTA -", operaciones[2]["color"]),
        ("3 = MULTI x", operaciones[3]["color"]),
        ("4 = DIVIS /", operaciones[4]["color"])
    ]
    
    y_inicio = 145
    for i, (texto, color) in enumerate(opciones):
        cv2.circle(img, (35, y_inicio + i * 32), 6, color, -1)
        cv2.circle(img, (35, y_inicio + i * 32), 6, (255, 255, 255), 1)
        dibujar_texto_con_sombra(img, texto, (50, y_inicio + i * 32 + 5), 0.5, (255, 255, 255), 1)
    
    # Instrucción en la parte inferior del panel
    cv2.line(img, (25, 265), (panel_w - 15, 265), (80, 80, 80), 1)
    dibujar_texto_con_sombra(img, "Manten 2 seg", (25, 285), 0.45, (150, 150, 150), 1)


def dibujar_confirmacion(img, dedos, progreso):
    """Dibuja la confirmación en el lateral derecho"""
    h, w, _ = img.shape
    
    if dedos in operaciones:
        op = operaciones[dedos]
        
        # Panel en esquina inferior derecha
        panel_x = w - 290
        panel_y = h - 130
        dibujar_panel_redondeado(img, panel_x, panel_y, 280, 120, (40, 40, 40), 0.85)
        
        # Texto de operación
        dibujar_texto_con_sombra(img, "Detectando:", (panel_x + 15, panel_y + 30), 0.5, (180, 180, 180), 1)
        dibujar_texto_con_sombra(img, op['nombre'], (panel_x + 15, panel_y + 60), 0.9, op["color"], 2)
        
        # Barra de progreso
        dibujar_barra_progreso(img, panel_x + 15, panel_y + 75, 250, 18, progreso, (60, 60, 60), COLORES["exito"])
        
        # Porcentaje
        porcentaje = int(progreso * 100)
        dibujar_texto_con_sombra(img, f"{porcentaje}%", (panel_x + 120, panel_y + 110), 0.5, (255, 255, 255), 1)


def dibujar_pantalla_calculo(img, operacion, num_izq, num_der, resultado):
    """Dibuja la pantalla de cálculo con UI en los laterales"""
    h, w, _ = img.shape
    op = operaciones[operacion]
    
    # Línea divisoria central sutil punteada
    dibujar_linea_divisora(img)
    
    # ===== PANEL IZQUIERDO =====
    panel_izq_x = 10
    dibujar_panel_redondeado(img, panel_izq_x, 10, 150, 180, (20, 20, 20), 0.75)
    
    # Etiqueta izquierda
    dibujar_texto_con_sombra(img, "IZQUIERDA", (panel_izq_x + 15, 40), 0.5, COLORES["cyan"], 1)
    cv2.line(img, (panel_izq_x + 15, 50), (panel_izq_x + 135, 50), (80, 80, 80), 1)
    
    # Número grande izquierdo
    dibujar_circulo_numero(img, panel_izq_x + 75, 120, num_izq, COLORES["cyan"], 45)
    
    # ===== PANEL DERECHO =====
    panel_der_x = w - 160
    dibujar_panel_redondeado(img, panel_der_x, 10, 150, 180, (20, 20, 20), 0.75)
    
    # Etiqueta derecha
    dibujar_texto_con_sombra(img, "DERECHA", (panel_der_x + 25, 40), 0.5, COLORES["secundario"], 1)
    cv2.line(img, (panel_der_x + 15, 50), (panel_der_x + 135, 50), (80, 80, 80), 1)
    
    # Número grande derecho
    dibujar_circulo_numero(img, panel_der_x + 75, 120, num_der, COLORES["secundario"], 45)
    
    # ===== PANEL INFERIOR - RESULTADO =====
    panel_res_w = 350
    panel_res_x = w//2 - panel_res_w//2
    dibujar_panel_redondeado(img, panel_res_x, h - 90, panel_res_w, 80, (30, 30, 30), 0.85)
    
    # Operación seleccionada
    dibujar_texto_con_sombra(img, f"Operacion: {op['nombre']}", (panel_res_x + 15, h - 65), 0.5, op["color"], 1)
    
    # Resultado
    resultado_texto = f"{num_izq} {op['simbolo']} {num_der} = {resultado}"
    dibujar_texto_con_sombra(img, resultado_texto, (panel_res_x + 15, h - 30), 1.0, COLORES["acento"], 2)
    
    # ===== CONTROLES - Esquina inferior derecha =====
    dibujar_panel_redondeado(img, w - 200, h - 40, 190, 35, (20, 20, 20), 0.7)
    dibujar_texto_con_sombra(img, "[R] Reset [Q] Salir", (w - 190, h - 18), 0.45, (150, 150, 150), 1)


def realizar_operacion(num_izq, num_der, operacion):
    """Realiza la operación matemática seleccionada"""
    if operacion == 1:
        return num_izq + num_der
    elif operacion == 2:
        return num_izq - num_der
    elif operacion == 3:
        return num_izq * num_der
    elif operacion == 4:
        if num_der == 0:
            return "Error!"
        else:
            return round(num_izq / num_der, 2)
    return 0


def clasificar_manos_por_posicion(manos, ancho_pantalla):
    """Clasifica las manos según su posición X y suma todos los dedos de cada lado"""
    if len(manos) == 0:
        return 0, 0
    
    centro = ancho_pantalla // 2
    dedos_izquierda = 0
    dedos_derecha = 0
    
    # Sumar todos los dedos de las manos en cada lado
    for mano in manos:
        if mano["centro_x"] < centro:
            dedos_izquierda += mano["dedos"]
        else:
            dedos_derecha += mano["dedos"]
    
    return dedos_izquierda, dedos_derecha


# ============================================
# BUCLE PRINCIPAL
# ============================================

print()
print("╔" + "═" * 50 + "╗")
print("║" + " CALCULADORA CON GESTOS DE MANOS ".center(50) + "║")
print("╠" + "═" * 50 + "╣")
print("║" + " Controles:".ljust(50) + "║")
print("║" + "   [R] - Reiniciar / Cambiar operación".ljust(50) + "║")
print("║" + "   [Q] - Salir del programa".ljust(50) + "║")
print("╚" + "═" * 50 + "╝")
print()

while True:
    success, img = cap.read()
    
    if not success:
        print("  ✗ Error: No se puede acceder a la cámara")
        break
    
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    
    # Convertir para MediaPipe
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    
    # Detectar manos
    detection_result = hand_detector.detect(mp_image)
    manos = procesar_manos(detection_result, img)
    
    # FASE 1: SELECCIÓN
    if fase_actual == "seleccion":
        dibujar_menu(img)
        
        if manos:
            total_dedos = manos[0]["dedos"]
            
            if 1 <= total_dedos <= 4:
                if total_dedos == dedos_detectados:
                    if tiempo_inicio_deteccion is not None:
                        tiempo_transcurrido = time.time() - tiempo_inicio_deteccion
                        progreso = min(tiempo_transcurrido / TIEMPO_CONFIRMACION, 1.0)
                        dibujar_confirmacion(img, total_dedos, progreso)
                        
                        if tiempo_transcurrido >= TIEMPO_CONFIRMACION:
                            operacion_seleccionada = total_dedos
                            fase_actual = "calculo"
                            print(f"  ✓ Operación seleccionada: {operaciones[total_dedos]['nombre']}")
                    else:
                        tiempo_inicio_deteccion = time.time()
                else:
                    dedos_detectados = total_dedos
                    tiempo_inicio_deteccion = time.time()
            else:
                dedos_detectados = 0
                tiempo_inicio_deteccion = None
                if total_dedos == 0:
                    # Mensaje en panel lateral derecho
                    dibujar_panel_redondeado(img, w - 290, h - 80, 280, 40, (60, 40, 40), 0.8)
                    dibujar_texto_con_sombra(img, "Levanta 1-4 dedos", (w - 275, h - 55), 0.55, COLORES["error"], 1)
                elif total_dedos == 5:
                    dibujar_panel_redondeado(img, w - 290, h - 80, 280, 40, (60, 40, 40), 0.8)
                    dibujar_texto_con_sombra(img, "Maximo 4 dedos", (w - 260, h - 55), 0.55, COLORES["error"], 1)
        else:
            dedos_detectados = 0
            tiempo_inicio_deteccion = None
            # Mensaje en panel lateral derecho
            dibujar_panel_redondeado(img, w - 290, h - 80, 280, 40, (40, 60, 40), 0.8)
            dibujar_texto_con_sombra(img, "Muestra tu mano", (w - 260, h - 55), 0.55, COLORES["exito"], 1)
    
    # FASE 2: CÁLCULO
    elif fase_actual == "calculo":
        num_izq, num_der = clasificar_manos_por_posicion(manos, w)
        resultado = realizar_operacion(num_izq, num_der, operacion_seleccionada)
        dibujar_pantalla_calculo(img, operacion_seleccionada, num_izq, num_der, resultado)
    
    # Mostrar imagen
    cv2.imshow("Calculadora con Gestos", img)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q') or key == ord('Q'):
        print("  → Saliendo del programa...")
        break
    
    if key == ord('r') or key == ord('R'):
        fase_actual = "seleccion"
        operacion_seleccionada = None
        dedos_detectados = 0
        tiempo_inicio_deteccion = None
        print("  → Reiniciando - Selecciona nueva operación")

# ============================================
# LIMPIEZA
# ============================================
cap.release()
cv2.destroyAllWindows()
print("  ✓ Programa finalizado correctamente")
print()
