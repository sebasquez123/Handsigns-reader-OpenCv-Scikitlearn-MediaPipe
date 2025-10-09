

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
    '''Ensure the CSV file has a header row to define feature columns.'''
    
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            header = [f"x{i}" for i in range(21)] + [f"y{i}" for i in range(21)] + [f"z{i}" for i in range(21)] + ["label"]
            writer.writerow(header)

def _collect_gestures():
    '''Collect hand gesture data using MediaPipe and save to CSV file.
    The file is overwritten each time the function is called.'''

    gesture_label = input("👉 Write the name of this gesture (ej: PUNO, MANO, PULGAR): ")
    if not gesture_label:
        raise RuntimeError("Gesture label cannot be empty")
    
    _ensure_header(processPath)
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        raise RuntimeError("Could not open camera")
    
    with mp_hands.Hands(static_image_mode=False,
                        max_num_hands=max_num_hands,
                        min_detection_confidence=min_det_conf,
                        min_tracking_confidence=min_track_conf) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("Could not read frame from camera")
            
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
            cv2.putText(frame, f"Gesture: {gesture_label}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
            cv2.imshow("Gesture Collector", frame)
            key = cv2.waitKey(1) & 0xFF
            
            
            
            if key == ord('q'):
                break
            
            
    cap.release()
    cv2.destroyAllWindows()

def process_images(*args, **kwargs): 
    return _collect_gestures(*args, **kwargs)
