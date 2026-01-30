# 🖐️ Calculadora con Gestos de Manos

Una calculadora interactiva que utiliza reconocimiento de gestos de manos para realizar operaciones matemáticas. ¡Usa tus dedos para seleccionar operaciones y mostrar números!

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.x-orange.svg)

---

## 📋 Descripción

Este programa permite realizar operaciones matemáticas básicas utilizando gestos de las manos detectados por la cámara web:

### **FASE 1 - Selección de Operación** 
Levanta dedos con **una sola mano** para seleccionar la operación:

| Dedos | Operación |
|:-----:|:---------:|
| ☝️ 1 | Suma (+) |
| ✌️ 2 | Resta (-) |
| 🤟 3 | Multiplicación (×) |
| 🖐️ 4 | División (÷) |

> Mantén los dedos levantados durante **2 segundos** para confirmar la operación.

### **FASE 2 - Cálculo con Ambas Manos**
Una vez seleccionada la operación:

- 👈 **Mano izquierda** = Primer número (0-5 dedos)
- 👉 **Mano derecha** = Segundo número (0-5 dedos)
- El resultado se calcula y muestra automáticamente

**Ejemplo:** 
- Izquierda: 3 dedos | Derecha: 2 dedos
- Suma → 3 + 2 = **5**

---

## 🛠️ Requisitos del Sistema

- **Sistema Operativo:** Windows 10/11, macOS, Linux
- **Python:** 3.10 o superior
- **Cámara web:** Requerida

---

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd tu-directorio-de-proyectos
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install opencv-python mediapipe numpy
```

O instalar desde requirements.txt:

```bash
pip install -r requirements.txt
```

---

## 📚 Librerías Utilizadas

| Librería | Versión | Descripción |
|----------|---------|-------------|
| `opencv-python` | >= 4.5.0 | Procesamiento de imágenes y video |
| `mediapipe` | >= 0.10.0 | Detección de manos con IA |
| `numpy` | >= 1.20.0 | Operaciones numéricas |

### Instalar librerías individualmente:

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
```

---

## 🚀 Cómo Ejecutar

### Método 1: Línea de comandos

```bash
# Windows
python calculadora_dedos.py

# macOS/Linux
python3 calculadora_dedos.py
```

### Método 2: Desde VS Code

1. Abre el archivo `calculadora_dedos.py`
2. Presiona `F5` o haz clic en "Run"

### Primera ejecución

El programa descargará automáticamente el modelo de detección de manos (`hand_landmarker.task`) la primera vez que se ejecute.

---

## 🎮 Controles

| Tecla | Acción |
|:-----:|--------|
| `R` | Reiniciar y cambiar operación |
| `Q` | Salir del programa |

---

## 🖥️ Capturas de Pantalla

### Menú de Selección
```
╔═══════════════════════════════════════╗
║     CALCULADORA CON GESTOS            ║
╠═══════════════════════════════════════╣
║  SELECCIONA OPERACIÓN:                ║
║  ● 1 dedo  = SUMA  (+)                ║
║  ● 2 dedos = RESTA (-)                ║
║  ● 3 dedos = MULTI (×)                ║
║  ● 4 dedos = DIVIS (÷)                ║
╚═══════════════════════════════════════╝
```

### Pantalla de Cálculo
```
╔═══════════════════════════════════════╗
║         Operación: SUMA               ║
╠═══════════════════════════════════════╣
║                                       ║
║    (3)        +        (2)            ║
║  IZQUIERDA         DERECHA            ║
║                                       ║
╠═══════════════════════════════════════╣
║         3 + 2 = 5                     ║
╚═══════════════════════════════════════╝
```

---

## ⚠️ Solución de Problemas

### La cámara no se detecta
```bash
# Cambiar el índice de la cámara en el código
cap = cv2.VideoCapture(1)  # Probar con 1, 2, etc.
```

### Error de MediaPipe
```bash
# Reinstalar MediaPipe
pip uninstall mediapipe
pip install mediapipe
```

### Los dedos no se detectan bien
- Asegúrate de tener **buena iluminación**
- Mantén la mano a una distancia de **30-80 cm** de la cámara
- Evita fondos muy claros o con mucho movimiento

---

## 📁 Estructura del Proyecto

```
📂 calculadora-gestos/
├── 📄 calculadora_dedos.py    # Programa principal
├── 📄 hand_landmarker.task    # Modelo de IA (se descarga automático)
├── 📄 README.md               # Este archivo
└── 📄 requirements.txt        # Dependencias
```

---

## 🧠 Cómo Funciona

1. **Captura de video:** OpenCV captura frames de la cámara web
2. **Detección de manos:** MediaPipe detecta hasta 2 manos y sus 21 landmarks
3. **Conteo de dedos:** Se analizan las posiciones de las puntas de los dedos
4. **Clasificación:** Las manos se clasifican por su posición X (izquierda/derecha)
5. **Cálculo:** Se aplica la operación matemática seleccionada
6. **Visualización:** Se dibuja el resultado con efectos visuales

---

## 💻 Explicación Completa del Código

### 📦 Estructura General del Programa

El programa está organizado en las siguientes secciones:

#### **1. Importación de Librerías y Descarga del Modelo**

```python
import cv2
import mediapipe as mp
import numpy as np
```

**¿Qué hace esta sección?**

- Al iniciar, el programa verifica si existe el archivo `hand_landmarker.task` (modelo de IA para detectar manos)
- Si no existe, **lo descarga automáticamente** desde los servidores de Google MediaPipe
- Esto asegura que el programa funcione desde la primera ejecución sin configuración manual

```python
if not os.path.exists(model_path):
    urllib.request.urlretrieve(url, model_path)
```

---

#### **2. Configuración de MediaPipe Hand Landmarker**

```python
options = vision.HandLandmarkerOptions(
    num_hands=20,
    min_hand_detection_confidence=0.5
)
hand_detector = vision.HandLandmarker.create_from_options(options)
```

**¿Qué hace MediaPipe?**

- Utiliza **inteligencia artificial** para detectar manos en tiempo real
- Identifica **21 puntos clave (landmarks)** por cada mano:
  - Punta de cada dedo (5 puntos)
  - Articulaciones de los dedos (16 puntos)
  - Base de la muñeca (1 punto)
- Puede detectar hasta **20 manos simultáneamente** en el frame
- Clasifica cada mano como **"Left"** o **"Right"**

**Landmarks de una mano:**
```
        8   12  16  20
        |   |   |   |
    4   |   |   |   |
    |   |   |   |   |
    |   |   |   |   |
  [Pulgar][Índice][Medio][Anular][Meñique]
        \   |   |   /
         \  |  |  /
          \ | | /
            [0] ← Muñeca
```

---

#### **3. Sistema de Estados (Máquina de Estados)**

El programa funciona con **2 fases** principales:

```python
fase_actual = "seleccion"  # o "calculo"
```

| Fase | Función | Entrada |
|------|---------|---------|
| **seleccion** | Elegir la operación matemática | 1-4 dedos de una mano |
| **calculo** | Realizar operaciones con ambas manos | Dedos de mano izquierda y derecha |

---

### 🔍 Funciones Principales del Código

#### **A) `contar_dedos(hand_landmarks, handedness, img_width, img_height)`**

**Propósito:** Determinar cuántos dedos están levantados.

**Algoritmo:**

1. **Para el pulgar:**
   ```python
   # Detecta según la orientación horizontal
   if handedness == "Right":
       if thumb_tip['x'] > thumb_ip['x'] + 20:
           dedos.append(1)  # Pulgar levantado
   ```
   - Compara la posición X de la punta vs la articulación
   - Mano derecha: pulgar levantado si punta está más a la DERECHA
   - Mano izquierda: pulgar levantado si punta está más a la IZQUIERDA

2. **Para los otros 4 dedos:**
   ```python
   # Detecta según la posición vertical
   if tip['y'] < pip['y'] - umbral:
       dedos.append(1)  # Dedo levantado
   ```
   - Compara la posición Y (altura) de la punta con la articulación media
   - Dedo levantado = punta más ARRIBA que articulación
   - Usa un umbral dinámico (30% de la distancia entre articulaciones)

**Retorna:** Número total de dedos levantados (0-5)

---

#### **B) `clasificar_manos_por_posicion(manos, ancho_pantalla)`**

**Propósito:** Separar las manos detectadas en lado izquierdo y derecho de la pantalla.

```python
centro = ancho_pantalla // 2  # Línea divisoria vertical

for mano in manos:
    if mano["centro_x"] < centro:
        dedos_izquierda += mano["dedos"]
    else:
        dedos_derecha += mano["dedos"]
```

**¿Por qué es importante?**

- Permite usar **múltiples manos simultáneamente**
- Si detecta 3 manos a la izquierda y 2 a la derecha, **SUMA** todos los dedos de cada lado
- Ejemplo: 2 manos izquierdas con 3 dedos cada una = **6 dedos totales** en el lado izquierdo

**Retorna:** `(dedos_izquierda, dedos_derecha)`

---

#### **C) `realizar_operacion(num_izq, num_der, operacion)`**

**Propósito:** Ejecutar la operación matemática seleccionada.

```python
if operacion == 1:      # SUMA
    return num_izq + num_der
elif operacion == 2:    # RESTA
    return num_izq - num_der
elif operacion == 3:    # MULTIPLICACIÓN
    return num_izq * num_der
elif operacion == 4:    # DIVISIÓN
    if num_der == 0:
        return "Error!"  # Manejo de división por cero
    else:
        return round(num_izq / num_der, 2)
```

**Características:**
- Maneja **división por cero** mostrando "Error!"
- Redondea divisiones a **2 decimales** para legibilidad
- Soporta 4 operaciones básicas

---

### 🎨 Sistema de Interfaz Gráfica

#### **Funciones de Dibujo**

El programa utiliza múltiples funciones para crear una interfaz visual profesional:

| Función | Descripción |
|---------|-------------|
| `dibujar_panel_redondeado()` | Crea paneles con esquinas redondeadas y transparencia |
| `dibujar_texto_con_sombra()` | Dibuja texto con efecto de sombra para mejor legibilidad |
| `dibujar_barra_progreso()` | Muestra la barra de confirmación de 2 segundos |
| `dibujar_circulo_numero()` | Dibuja círculos grandes con números para los dedos |
| `dibujar_landmarks()` | Visualiza los 21 puntos de la mano con líneas conectoras |

#### **Esquema de Colores**

```python
COLORES = {
    "primario": (255, 87, 51),      # Coral
    "secundario": (50, 205, 50),    # Verde lima
    "acento": (255, 215, 0),        # Dorado
    "exito": (0, 255, 127),         # Verde primavera
    "error": (71, 99, 255),         # Rojo coral
    "cyan": (255, 255, 0),          # Cyan
    "rosa": (203, 192, 255),        # Rosa
}
```

**Nota:** Los colores están en formato **BGR** (Blue-Green-Red) usado por OpenCV.

---

### 🔄 Bucle Principal del Programa

```python
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Espejado horizontal
    
    # Detectar manos con MediaPipe
    detection_result = hand_detector.detect(mp_image)
    manos = procesar_manos(detection_result, img)
    
    # FASE 1: Selección de operación
    if fase_actual == "seleccion":
        # Detectar 1-4 dedos por 2 segundos
        if tiempo_transcurrido >= 2.0:
            operacion_seleccionada = total_dedos
            fase_actual = "calculo"
    
    # FASE 2: Realizar cálculos
    elif fase_actual == "calculo":
        num_izq, num_der = clasificar_manos_por_posicion(manos, w)
        resultado = realizar_operacion(num_izq, num_der, operacion_seleccionada)
        dibujar_pantalla_calculo(img, operacion_seleccionada, num_izq, num_der, resultado)
    
    cv2.imshow("Calculadora con Gestos", img)
```

**Flujo de ejecución:**

1. **Captura frame** de la cámara → `cap.read()`
2. **Espeja la imagen** para efecto espejo → `cv2.flip()`
3. **Detecta manos** con MediaPipe → `hand_detector.detect()`
4. **Procesa detección** y cuenta dedos → `procesar_manos()`
5. **Ejecuta lógica** según la fase actual
6. **Muestra resultado** en pantalla → `cv2.imshow()`
7. **Espera teclas** (Q para salir, R para reiniciar)

---

### ⏱️ Sistema de Confirmación por Tiempo

```python
TIEMPO_CONFIRMACION = 2.0  # segundos

if total_dedos == dedos_detectados:
    tiempo_transcurrido = time.time() - tiempo_inicio_deteccion
    progreso = min(tiempo_transcurrido / TIEMPO_CONFIRMACION, 1.0)
    dibujar_barra_progreso(img, x, y, w, h, progreso, color_fondo, color_barra)
```

**¿Cómo funciona?**

1. Detecta cuántos dedos estás mostrando
2. **Inicia un temporizador** cuando detecta 1-4 dedos
3. **Si cambias** el número de dedos → reinicia el temporizador
4. **Si mantienes** la misma cantidad por 2 segundos → confirma la selección
5. **Barra de progreso** muestra el avance visual (0-100%)

**Ventaja:** Evita selecciones accidentales y da feedback visual claro.

---

### 🎯 Detección Multi-Mano

El programa soporta **múltiples manos** en cada lado de la pantalla:

```python
# Ejemplo: 3 personas mostrando manos a la vez
# Lado izquierdo: Mano 1 (2 dedos) + Mano 2 (3 dedos) = 5 dedos totales
# Lado derecho: Mano 3 (4 dedos) = 4 dedos totales
# Resultado: 5 + 4 = 9 (si operación es SUMA)
```

**Configuración:**
```python
num_hands=20  # Detecta hasta 20 manos simultáneamente
```

---

### 🖼️ Procesamiento de Imagen

#### **Conversión de Color**

```python
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

- **OpenCV** usa formato **BGR** (Blue-Green-Red)
- **MediaPipe** requiere formato **RGB** (Red-Green-Blue)
- La conversión es necesaria para que MediaPipe funcione correctamente

#### **Efecto Espejo**

```python
img = cv2.flip(img, 1)
```

- Espeja la imagen horizontalmente
- Hace que la interacción sea más natural (como verse en un espejo)
- Sin esto, levantar tu mano derecha aparecería en el lado izquierdo de la pantalla

---

### 🧮 Ejemplos de Cálculo Paso a Paso

#### **Ejemplo 1: Suma de 3 + 2**

1. **Selección:** Levantas 1 dedo por 2 segundos → Selecciona SUMA
2. **Cálculo:**
   - Mano izquierda: 3 dedos
   - Mano derecha: 2 dedos
   - Resultado: `3 + 2 = 5`

#### **Ejemplo 2: División de 4 ÷ 2**

1. **Selección:** Levantas 4 dedos por 2 segundos → Selecciona DIVISIÓN
2. **Cálculo:**
   - Mano izquierda: 4 dedos
   - Mano derecha: 2 dedos
   - Resultado: `4 ÷ 2 = 2.0`

#### **Ejemplo 3: División por cero**

1. **Selección:** División
2. **Cálculo:**
   - Mano izquierda: 5 dedos
   - Mano derecha: 0 dedos (puño cerrado)
   - Resultado: `"Error!"` (evita división por cero)

---

### 🔧 Parámetros Configurables

```python
# Cámara
cap.set(3, 1280)  # Ancho: 1280 píxeles
cap.set(4, 720)   # Alto: 720 píxeles

# Detección de manos
min_hand_detection_confidence=0.5  # Confianza mínima: 50%
min_tracking_confidence=0.5        # Seguimiento mínimo: 50%

# Confirmación
TIEMPO_CONFIRMACION = 2.0  # Segundos para confirmar

# Umbral de detección de dedos
umbral = max(distancia_ref * 0.3, 15)  # 30% o 15 píxeles
```

---

### 🎮 Teclas de Control

| Tecla | Código | Acción |
|:-----:|--------|--------|
| **Q** | `ord('q')` | Salir del programa |
| **R** | `ord('r')` | Reiniciar (volver a selección de operación) |

```python
key = cv2.waitKey(1) & 0xFF

if key == ord('q') or key == ord('Q'):
    break  # Salir
    
if key == ord('r') or key == ord('R'):
    fase_actual = "seleccion"  # Reiniciar
```

**`cv2.waitKey(1)`**: Espera 1 milisegundo por una tecla presionada (mantiene el programa corriendo a ~60 FPS).

---

### 📊 Diagrama de Flujo del Programa

```
┌─────────────────┐
│  Inicializar    │
│  - Cámara       │
│  - MediaPipe    │
│  - Variables    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  BUCLE INFINITO │◄──────────────┐
└────────┬────────┘               │
         │                        │
         ▼                        │
┌─────────────────┐               │
│ Capturar Frame  │               │
│ Detectar Manos  │               │
└────────┬────────┘               │
         │                        │
         ▼                        │
    ¿Qué fase?                   │
         │                        │
    ┌────┴────┐                  │
    │         │                  │
    ▼         ▼                  │
┌─────┐   ┌─────┐               │
│SELEC│   │CALCUL│              │
│CIÓN │   │O     │              │
└──┬──┘   └──┬──┘               │
   │         │                  │
   │         ▼                  │
   │    ┌─────────┐             │
   │    │Clasificar│            │
   │    │ Manos    │            │
   │    │Realizar  │            │
   │    │Operación │            │
   │    └────┬─────┘            │
   │         │                  │
   └─────────┴──────────────────┘
         │
         ▼
    ¿Tecla Q?
         │
        Sí
         │
         ▼
   ┌──────────┐
   │  Salir   │
   └──────────┘
```

---

### 🔬 Detalles Técnicos Avanzados

#### **1. Coordenadas Normalizadas**

MediaPipe devuelve coordenadas **normalizadas** (0.0 a 1.0):

```python
# Convertir a píxeles
px = int(landmark.x * img_width)
py = int(landmark.y * img_height)
```

**Ventaja:** Funciona con cualquier resolución de cámara.

#### **2. Transparencia de Paneles**

```python
cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
```

- **overlay:** Panel con color sólido
- **alpha:** Nivel de transparencia (0.7 = 70% opaco)
- **img:** Imagen original
- **Resultado:** Panel semitransparente sobre el video

#### **3. Detección del Pulgar**

El pulgar es el **dedo más complicado** de detectar porque:

- Se mueve **horizontalmente** (no verticalmente como otros dedos)
- Su orientación cambia según la mano (izquierda vs derecha)
- Requiere **detección de lateralidad** (handedness)

```python
# Mano derecha: pulgar va hacia la derecha
if handedness == "Right":
    if thumb_tip['x'] > thumb_ip['x'] + 20:
        dedos.append(1)
```

#### **4. Landmarks IDs Importantes**

```python
TIP_IDS = [4, 8, 12, 16, 20]  # Puntas de los 5 dedos
```

| ID | Dedo | Descripción |
|----|------|-------------|
| 0  | Muñeca | Base de la mano |
| 4  | Pulgar | Punta del pulgar |
| 8  | Índice | Punta del índice |
| 12 | Medio | Punta del dedo medio |
| 16 | Anular | Punta del anular |
| 20 | Meñique | Punta del meñique |

---

### 💡 Optimizaciones y Mejoras

El código incluye varias optimizaciones:

1. **Umbral adaptativo** para detección de dedos
2. **Sistema de confirmación** para evitar errores
3. **Clasificación automática** por posición
4. **Suma de múltiples manos** del mismo lado
5. **Manejo de errores** (división por cero)
6. **Interfaz visual** con paneles informativos
7. **Barra de progreso** para feedback inmediato

---

## 📝 Características Técnicas

- ✅ Detección de hasta **2 manos** simultáneamente
- ✅ Clasificación por posición (izquierda/derecha)
- ✅ Conteo de dedos usando **landmarks** de MediaPipe
- ✅ Manejo de **división por cero**
- ✅ Interfaz visual con **paneles semitransparentes**
- ✅ **Barra de progreso** para confirmación
- ✅ Descarga automática del modelo de IA

---

## 👨‍💻 Autor

Creado con ❤️ usando:
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/)
- [Python](https://python.org/)

---

## 📄 Licencia

Este proyecto es de uso libre para fines educativos.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras un bug o tienes una mejora, no dudes en crear un issue o pull request.
