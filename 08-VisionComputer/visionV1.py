import os
# Silenciar mensajes de diagnóstico interno de TensorFlow / Abseil en la terminal
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["GLOG_minloglevel"] = "2"

import urllib.request
import cv2
import mediapipe as mp

# Importamos las herramientas de la API moderna de MediaPipe Tasks
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    GestureRecognizer,
    GestureRecognizerOptions,
    RunningMode,
    drawing_utils,
    HandLandmarksConnections,
)

# =============================================================================
# PASO 1: DESCARGA AUTOMÁTICA DEL MODELO PRE-ENTRENADO DE IA
# =============================================================================
# Un modelo de Deep Learning necesita un archivo de "pesos" (.task) ya entrenado
# con millones de imágenes de manos. Si no existe en la carpeta, lo descargamos.
MODEL_NAME = "gesture_recognizer.task"
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_NAME)
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"

if not os.path.exists(MODEL_PATH):
    print("[*] Descargando modelo pre-entrenado desde Google...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("[+] Modelo listo para usarse.\n")

# =============================================================================
# PASO 2: CONFIGURACIÓN E INICIALIZACIÓN DEL MODELO
# =============================================================================
# Parámetros del detector:
# - base_options: Ruta al archivo del modelo neuronal.
# - running_mode: Modo IMAGE (procesa fotograma por fotograma de forma síncrona).
# - num_hands: Cantidad máxima de manos a buscar simultáneamente (ej. hasta 2).
# - min_hand_detection_confidence: Umbral de seguridad mínimo (50%) para decir "hay una mano".
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.5,
)

# Creamos el objeto detector
detector = GestureRecognizer.create_from_options(options)

# =============================================================================
# PASO 3: INICIALIZACIÓN DE LA CÁMARA WEB CON OPENCV
# =============================================================================
# El número 0 representa la cámara web predeterminada del equipo.
cap = cv2.VideoCapture(0)

# Configuramos una resolución estándar (640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("[!] ERROR: No se pudo abrir la cámara web.")
    print("    Asegúrate de que no esté siendo utilizada por otra aplicación.")
    exit(1)

print("=" * 65)
print("  [Versión 1] Detección Básica de Manos y Lateralidad")
print("  Muestra tu mano frente a la cámara")
print("  Presiona 'ESC' o 'q' para salir")
print("=" * 65)

# =============================================================================
# PASO 4: BUCLE PRINCIPAL (FRAME A FRAME EN TIEMPO REAL)
# =============================================================================
try:
    while cap.isOpened():
        # Leemos el fotograma actual de la cámara
        ret, frame = cap.read()
        if not ret:
            print("[!] No se pudo recibir la imagen de la cámara.")
            break

        # Efecto espejo horizontal (flip): para que mover la mano derecha en la
        # vida real se mueva a la derecha en la pantalla (comportamiento natural).
        frame = cv2.flip(frame, 1)
        alto, ancho, _ = frame.shape

        # OpenCV captura en formato BGR (Azul-Verde-Rojo), pero los modelos de IA
        # trabajan en el estándar RGB (Rojo-Verde-Azul).
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convertimos la imagen de OpenCV al formato nativo de MediaPipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        # ---------------------------------------------------------------------
        # INFERENCIA: La red neuronal busca manos en la imagen
        # ---------------------------------------------------------------------
        resultados = detector.recognize(mp_image)

        # Verificamos cuántas manos fueron detectadas
        num_manos = len(resultados.hand_landmarks)

        # ---------------------------------------------------------------------
        # SI HAY MANOS: Procesamos cada una de ellas
        # ---------------------------------------------------------------------
        if num_manos > 0:
            for idx, landmarks in enumerate(resultados.hand_landmarks):
                # 1. Dibujar los 21 puntos anatómicos (articulaciones y falanges)
                drawing_utils.draw_landmarks(
                    frame,
                    landmarks,
                    HandLandmarksConnections.HAND_CONNECTIONS,
                )

                # 2. Calcular la Caja Delimitadora (Bounding Box):
                # El modelo entrega coordenadas relativas (0.0 a 1.0).
                # Las multiplicamos por el tamaño real de la imagen en píxeles.
                x_coords = [int(lm.x * ancho) for lm in landmarks]
                y_coords = [int(lm.y * alto) for lm in landmarks]

                # Añadimos un pequeño margen de 15 píxeles alrededor de la mano
                x_min = max(0, min(x_coords) - 15)
                x_max = min(ancho, max(x_coords) + 15)
                y_min = max(0, min(y_coords) - 15)
                y_max = min(alto, max(y_coords) + 15)

                # Dibujamos el rectángulo de detección (Bounding Box) en color verde
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                # 3. Determinar la Lateralidad (¿Es Mano Izquierda o Mano Derecha?):
                texto_mano = "Mano Detectada"
                if idx < len(resultados.handedness) and resultados.handedness[idx]:
                    lado = resultados.handedness[idx][0].category_name
                    # 'Left' es Mano Izquierda, 'Right' es Mano Derecha
                    texto_mano = "Mano Izquierda" if lado == "Left" else "Mano Derecha"

                # 4. Dibujar la etiqueta identificadora sobre la caja
                pos_y = max(25, y_min - 10)
                # Fondo oscuro para leer el texto fácilmente
                cv2.rectangle(frame, (x_min, pos_y - 20), (x_min + 180, pos_y + 5), (0, 0, 0), -1)
                cv2.putText(
                    frame,
                    texto_mano,
                    (x_min + 5, pos_y - 3),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

        # ---------------------------------------------------------------------
        # Mensaje de estado general en la parte superior
        # ---------------------------------------------------------------------
        mensaje_general = f"Manos detectadas: {num_manos}"
        color_texto = (0, 255, 0) if num_manos > 0 else (0, 0, 255)
        cv2.putText(
            frame,
            mensaje_general,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color_texto,
            2,
            cv2.LINE_AA,
        )

        cv2.putText(
            frame,
            "Presiona 'ESC' o 'q' para salir",
            (20, alto - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (200, 200, 200),
            1,
            cv2.LINE_AA,
        )

        # Mostramos la ventana gráfica
        cv2.imshow("Vision V1: Deteccion de Manos (Clase IA)", frame)

        # Salir si el usuario presiona la tecla ESC (código 27) o la letra 'q'
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == 27 or tecla == ord("q"):
            print("\n[+] Saliendo de la aplicación...")
            break

finally:
    # =========================================================================
    # PASO 5: LIBERACIÓN DE RECURSOS DEL SISTEMA
    # =========================================================================
    cap.release()
    cv2.destroyAllWindows()
    detector.close()
    print("[+] Recursos liberados correctamente.\n")
