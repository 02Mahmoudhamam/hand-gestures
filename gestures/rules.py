import numpy as np

# MediaPipe hand landmarks index
TIPS = {"thumb": 4, "index": 8, "middle": 12, "ring": 16, "pinky": 20}
PIPS = {"thumb": 3, "index": 6, "middle": 10, "ring": 14, "pinky": 18}
IPS  = {"thumb": 2}

def _is_finger_extended(landmarks, finger: str) -> bool:
    """For non-thumb fingers: tip.y < pip.y means extended."""
    tip = landmarks[TIPS[finger]]
    pip = landmarks[PIPS[finger]]
    return tip[1] < pip[1]

def _is_thumb_extended(landmarks, handedness: str) -> bool:
    tip = landmarks[TIPS["thumb"]]
    ip  = landmarks[IPS["thumb"]]
    return tip[0] > ip[0] if handedness == "Right" else tip[0] < ip[0]

def _thumb_up_direction(landmarks) -> bool:
    tip = landmarks[TIPS["thumb"]]
    ip  = landmarks[IPS["thumb"]]
    return tip[1] < ip[1]

def _ok_circle(landmarks, tol_ratio=0.06) -> bool:
    thumb_tip = landmarks[TIPS["thumb"]]
    index_tip = landmarks[TIPS["index"]]
    xs = landmarks[:, 0]; ys = landmarks[:, 1]
    w = xs.max() - xs.min() + 1
    h = ys.max() - ys.min() + 1
    diag = (w**2 + h**2) ** 0.5
    dist = np.linalg.norm(thumb_tip - index_tip)
    return dist <= tol_ratio * diag

def finger_states(landmarks, handedness: str):
    return {
        "thumb": _is_thumb_extended(landmarks, handedness),
        "index": _is_finger_extended(landmarks, "index"),
        "middle": _is_finger_extended(landmarks, "middle"),
        "ring": _is_finger_extended(landmarks, "ring"),
        "pinky": _is_finger_extended(landmarks, "pinky"),
    }

def classify_gesture(landmarks, handedness: str):
    states = finger_states(landmarks, handedness)

    rules = [
        ("Hello", all(states.values()), 5),
        ("Stop", not any(states.values()), 5),
        ("Peace", states["index"] and states["middle"] and not states["ring"] and not states["pinky"], 4),
        ("Like", _thumb_up_direction(landmarks) and not states["index"] and not states["middle"] and not states["ring"] and not states["pinky"], 5),
        ("Okay", _ok_circle(landmarks) and (states["middle"] or states["ring"] or states["pinky"]), 2),
    ]

    best_label, best_score = "Unknown", 0.0
    for label, condition, total in rules:
        score = 1.0 if condition else 0.0
        if score > best_score:
            best_label, best_score = label, score

    return best_label, float(best_score)
