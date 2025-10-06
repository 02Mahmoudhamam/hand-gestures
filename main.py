import argparse
import time
import json
from pathlib import Path

import cv2

from gestures.detector import HandDetector
from gestures.rules import classify_gesture
from gestures.smoothing import DecisionSmoother
from gestures.overlay import draw_landmarks_and_labels
from utils.stats import SessionStats


def parse_args():
    parser = argparse.ArgumentParser(description="Hand Gesture Recognition (OpenCV + MediaPipe)")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--min-det", type=float, default=0.7, help="Min detection confidence")
    parser.add_argument("--min-trk", type=float, default=0.6, help="Min tracking confidence")
    parser.add_argument("--smooth", type=int, default=7, help="Window size for decision smoothing")
    parser.add_argument("--width", type=int, default=960, help="Capture width")
    parser.add_argument("--height", type=int, default=540, help="Capture height")
    parser.add_argument("--save", type=str, default="stats/session_stats.json", help="Stats output path on exit")
    return parser.parse_args()


def main():
    args = parse_args()
    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera index {args.camera}")

    detector = HandDetector(min_detection_confidence=args.min_det,
                            min_tracking_confidence=args.min_trk,
                            max_num_hands=1)

    smoother = DecisionSmoother(window_size=max(3, args.smooth))
    stats = SessionStats()

    t0 = time.time()
    fps_ts, fps_cnt, fps_val = time.time(), 0, 0.0
    current_label = "None"
    current_conf = 0.0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # MediaPipe expects RGB, OpenCV gives BGR
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hand = detector.process(rgb)  # returns (landmarks_px, handedness) or None

        if hand is not None:
            landmarks_px, handedness = hand
            # Classify gesture based on landmarks and handedness
            raw_label, raw_conf = classify_gesture(landmarks_px, handedness)

            # Smooth the decision (majority over a window)
            label, conf = smoother.update(raw_label, raw_conf)

            current_label, current_conf = label, conf
            if label not in ("None", "Unknown"):
                stats.bump(label)
        else:
            # When no hand is detected, keep last stabilized label but do not bump stats
            raw_label, raw_conf = "None", 0.0
            label, conf = smoother.update(raw_label, raw_conf)
            current_label, current_conf = label, conf

        # FPS
        fps_cnt += 1
        now = time.time()
        if now - fps_ts >= 0.5:
            fps_val = fps_cnt / (now - fps_ts)
            fps_cnt, fps_ts = 0, now

        # Draw overlays
        draw_landmarks_and_labels(frame,
                                  landmarks_px=None if hand is None else hand[0],
                                  label=current_label,
                                  confidence=current_conf,
                                  fps=fps_val)

        cv2.imshow("Hand Gestures", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

    # Save session stats
    stats.set_duration(int(time.time() - t0))
    out_path = Path(args.save)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(stats.as_dict(), f, indent=2)
    print(f"[INFO] Session stats saved to {out_path}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
