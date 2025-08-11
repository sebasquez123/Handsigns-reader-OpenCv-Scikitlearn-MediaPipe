import cv2
import numpy as np
import pyzbar.pyzbar as qr

cap = cv2.VideoCapture(1)
font = cv2.FONT_HERSHEY_COMPLEX

# Ancho físico real del QR (cm)
QR_REAL_WIDTH = 8.5
# Longitud focal calibrada (px) (ajusta si cambia cámara / resolución)
FOCAL_LENGTH = 1411
# Distancia máxima para dibujar (cm)
MAX_DISTANCE_CM = 60.0

# (Opcional) Suavizado exponencial de distancia para reducir jitter
USE_SMOOTHING = True
SMOOTH_ALPHA = 0.3  # 0=no cambia, 1=sin suavizado
_smooth_distance = None  # para distancia (puedes eliminar si no quieres suavizado)

_camera_matrix = None
_dist_coeffs = np.zeros((5,1), dtype=np.float32)

def _order_square_points(pts_img):
    """Ordena 4 puntos (x,y) a un orden consistente: top-left, top-right, bottom-right, bottom-left."""
    pts = np.array(pts_img, dtype=np.float32)
    # sumar y restar para heuristica
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1).reshape(-1)
    ordered = np.zeros((4,2), dtype=np.float32)
    ordered[0] = pts[np.argmin(s)]  # top-left
    ordered[2] = pts[np.argmax(s)]  # bottom-right
    ordered[1] = pts[np.argmin(diff)]  # top-right
    ordered[3] = pts[np.argmax(diff)]  # bottom-left
    return ordered

def _rotation_matrix_to_euler_xyz(R):
    """Convierte matriz de rotación a euler XYZ (roll, pitch, yaw)."""
    sy = np.sqrt(R[0,0]*R[0,0] + R[1,0]*R[1,0])
    singular = sy < 1e-6
    if not singular:
        roll = np.degrees(np.arctan2(R[2,1], R[2,2]))      # X
        pitch = np.degrees(np.arctan2(-R[2,0], sy))        # Y
        yaw = np.degrees(np.arctan2(R[1,0], R[0,0]))       # Z
    else:
        roll = np.degrees(np.arctan2(-R[1,2], R[1,1]))
        pitch = np.degrees(np.arctan2(-R[2,0], sy))
        yaw = 0.0
    return roll, pitch, yaw

def _compute_pitch_deg(polygon_points, frame_shape):
    """Calcula la inclinación (pitch) de la cámara respecto al plano del QR.
    Pitch ~ rotación vertical: cámara mirando hacia arriba/abajo relative al QR.
    Requiere 4 puntos. Devuelve pitch en grados (0 ~ perpendicular)."""
    global _camera_matrix
    if polygon_points is None or len(polygon_points) < 4:
        return None
    pts = np.array([[p.x, p.y] for p in polygon_points], dtype=np.float32)
    if pts.shape[0] != 4:
        return None
    h, w = frame_shape[:2]
    if _camera_matrix is None:
        cx, cy = w/2.0, h/2.0
        _camera_matrix = np.array([[FOCAL_LENGTH, 0, cx], [0, FOCAL_LENGTH, cy], [0,0,1]], dtype=np.float32)
    img_pts = _order_square_points(pts)
    # Definir plano QR (z=0). Usamos QR_REAL_WIDTH para X y Y.
    obj_pts = np.array([
        [0, 0, 0],
        [QR_REAL_WIDTH, 0, 0],
        [QR_REAL_WIDTH, QR_REAL_WIDTH, 0],
        [0, QR_REAL_WIDTH, 0]
    ], dtype=np.float32)
    ok, rvec, tvec = cv2.solvePnP(obj_pts, img_pts, _camera_matrix, _dist_coeffs, flags=cv2.SOLVEPNP_IPPE_SQUARE)
    if not ok:
        return None
    R, _ = cv2.Rodrigues(rvec)
    roll, pitch, yaw = _rotation_matrix_to_euler_xyz(R)
    
    return pitch

def demo():
    global _smooth_distance
    while True:
        ret, cuadro = cap.read()
        if not ret:
            break
        detectedQr = qr.decode(cuadro)

        for obj in detectedQr:
            data_str = obj.data.decode('utf-8') if obj.data else ''
            qr_width_in_px = max(1, obj.rect.width)
            raw_distance = (QR_REAL_WIDTH * FOCAL_LENGTH) / qr_width_in_px

            if USE_SMOOTHING:
                if _smooth_distance is None:
                    _smooth_distance = raw_distance
                else:
                    _smooth_distance = SMOOTH_ALPHA * raw_distance + (1 - SMOOTH_ALPHA) * _smooth_distance
                distance_cm = _smooth_distance
            else:
                distance_cm = raw_distance

            pitch_deg = _compute_pitch_deg(obj.polygon, cuadro.shape)

            if distance_cm <= MAX_DISTANCE_CM:
                
                cv2.rectangle(
                    cuadro,
                    (obj.rect.left, obj.rect.top),
                    (obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height),
                    (0, 255, 0),
                    3
                )
                cv2.putText(cuadro, data_str, (obj.rect.left, max(15, obj.rect.top - 10)), font, 1, (0, 255, 0), 2)
                cv2.putText(cuadro, f"Dist: {distance_cm:.1f} cm", (obj.rect.left, obj.rect.top + obj.rect.height + 20), font, 1, (0, 255, 0), 2)
                if pitch_deg is not None:
                    cv2.putText(cuadro, f"Pitch: {pitch_deg:.1f} g", (obj.rect.left, obj.rect.top + 50), font, 0.6, (0, 255, 0), 2)
            else:
                cv2.rectangle(cuadro,(obj.rect.left, obj.rect.top),(obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height),(0, 0, 255),3)
                cv2.putText(cuadro, "Fuera de rango", (obj.rect.left, max(15, obj.rect.top - 10)), font, 1, (0, 0, 255), 2)


        cv2.imshow("QR Code Scanner", cuadro)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()