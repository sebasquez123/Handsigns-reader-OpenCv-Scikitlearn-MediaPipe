

import cv2
import mediapipe as mp
import csv
import os

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

processPath = "data/gestures.csv"
camera_index = 0
max_num_hands = 1
min_det_conf = 0.7
min_track_conf= 0.7



def _ensure_header(csv_path: str):
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            header = [f"x{i}" for i in range(21)] + [f"y{i}" for i in range(21)] + [f"z{i}" for i in range(21)] + ["label"]
            writer.writerow(header)

def recolectar_gestos():

    gesture_label = input("👉 Escribe el nombre de este gesto (ej: PUNO, MANO, PULGAR): ")
    if not gesture_label:
        raise RuntimeError("No se proporcionó una etiqueta para el gesto.")
    _ensure_header(processPath)
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara")
    print("[INFO] Recolección iniciada. q=salir")
    with mp_hands.Hands(static_image_mode=False,
                        max_num_hands=max_num_hands,
                        min_detection_confidence=min_det_conf,
                        min_tracking_confidence=min_track_conf) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    data = []
                    for lm in hand_landmarks.landmark:
                        data.extend([lm.x, lm.y, lm.z])
                    with open(processPath, "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(data + [gesture_label])
            cv2.putText(frame, f"Gesto: {gesture_label}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
            cv2.imshow("Recolector de Gestos", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

def procesar_imagenes(*args, **kwargs): 
    return recolectar_gestos(*args, **kwargs)
