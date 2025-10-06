import mediapipe as mp
import numpy as np

class HandDetector:
    """Thin wrapper around MediaPipe Hands. Returns pixel coordinates for 21 landmarks."""
    def __init__(self, min_detection_confidence=0.7, min_tracking_confidence=0.6, max_num_hands=1):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=1
        )

    def process(self, rgb_frame):
        """Return (landmarks_px, handedness) or None."""
        h, w = rgb_frame.shape[:2]
        res = self.hands.process(rgb_frame)
        if not res.multi_hand_landmarks:
            return None
        hand_landmarks = res.multi_hand_landmarks[0]
        handedness = res.multi_handedness[0].classification[0].label  # 'Right' or 'Left'
        pts = []
        for lm in hand_landmarks.landmark:
            x = int(lm.x * w)
            y = int(lm.y * h)
            pts.append((x, y))
        landmarks_px = np.array(pts, dtype=np.int32)
        return landmarks_px, handedness
