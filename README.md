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
