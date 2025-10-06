import cv2

def _color_for_conf(conf: float):
    if conf >= 0.8:   return (46, 204, 113)
    if conf >= 0.6:   return (0, 255, 255)
    return (0, 0, 255)

def draw_landmarks_and_labels(frame, landmarks_px, label: str, confidence: float, fps: float):
    if landmarks_px is not None:
        for (x, y) in landmarks_px:
            cv2.circle(frame, (int(x), int(y)), 3, (255, 200, 0), -1)

    color = _color_for_conf(confidence)
    text = f"{label} | conf={confidence:.2f} | FPS={fps:.1f}"
    cv2.rectangle(frame, (10, 10), (10 + 420, 50), (30, 30, 30), -1)
    cv2.putText(frame, text, (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)
