```markdown
# Hand Gesture Recognition (OpenCV + MediaPipe)

Real-time hand gesture recognition using **OpenCV** for video capture and **MediaPipe Hands** for hand landmark detection.  
The application displays hand landmarks, classifies gestures, overlays labels with confidence scores and FPS, and saves session statistics upon exit.

---

## 🧠 Features

- **MediaPipe Hands** integration (21 landmarks) with OpenCV video pipeline  
- **Rule-based gesture recognition**:
  - 🖐️ `Hello` (open palm)  
  - ✊ `Stop` (closed fist)  
  - ✌️ `Peace` (V sign)  
  - 👍 `Like` (thumb up)  
  - 👌 `Okay` (thumb + index circle)
- **Decision smoothing:** majority vote over a sliding window to reduce prediction jitter
- **Dynamic visualization:** overlay colors change based on confidence levels  
  - Green ≥ 0.80  
  - Yellow 0.60–0.79  
  - Red < 0.60
- **Session analytics:** gesture counts and duration saved in `stats/session_stats.json`

---

## 🗂 Project Structure

```
hand-gestures/
├─ main.py                     # Entry point (video loop, smoothing, overlay, stats)
├─ gestures/
│  ├─ detector.py              # MediaPipe wrapper (21 hand landmarks)
│  ├─ rules.py                 # Gesture classification logic
│  ├─ smoothing.py             # Decision smoothing algorithm
│  └─ overlay.py               # Visualization (landmarks + labels + FPS)
├─ utils/
│  └─ stats.py                 # Session statistics tracking
├─ requirements.txt
└─ README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Create and activate virtual environment

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

---

### 2️⃣ Install dependencies

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

> 💡 **Note:** If you encounter *"externally-managed-environment"* errors (PEP 668) on Ubuntu/Debian:
> ```bash
> ./venv/bin/python -m pip install -r requirements.txt --break-system-packages
> ```

---

### 3️⃣ Run the application

```bash
python main.py --camera 0 --width 960 --height 540 --smooth 7 --min-det 0.7 --min-trk 0.6
```

Press **`q`** or **`Esc`** to exit.  
Session statistics are automatically saved to `stats/session_stats.json`.

---

## 🧩 Command-Line Options

| Flag        | Default                  | Description                              |
|-------------|--------------------------|------------------------------------------|
| `--camera`  | 0                        | Camera device index (0, 1, 2...)         |
| `--width`   | 960                      | Capture frame width                      |
| `--height`  | 540                      | Capture frame height                     |
| `--min-det` | 0.7                      | Minimum detection confidence threshold   |
| `--min-trk` | 0.6                      | Minimum tracking confidence threshold    |
| `--smooth`  | 7                        | Smoothing window size (frames)           |
| `--save`    | stats/session_stats.json | Output path for session statistics       |

---

## 🔍 How It Works

1. **Video Capture:** OpenCV captures frames from the camera
2. **Landmark Detection:** MediaPipe Hands detects 21 landmarks per hand
3. **Gesture Classification:** Rule-based logic in `rules.py` classifies gestures using landmark geometry
4. **Smoothing:** Majority voting over a sliding window eliminates prediction jitter
5. **Visualization:** Colored overlays display gesture labels, confidence scores, and FPS
6. **Analytics:** Session statistics track gesture recognition counts and duration

---

## 🛠 Troubleshooting

### 🚫 "Cannot open camera index 0"

* **Camera in use:** Close applications like Zoom, Teams, or OBS
* **Try different index:**
  ```bash
  python main.py --camera 1
  ```
* **Linux permissions:**
  ```bash
  ls -l /dev/video*
  sudo usermod -aG video $USER && newgrp video
  ```

---

### ⚫ Black window or empty frames

* **Use MJPG format:**
  ```bash
  python main.py --width 640 --height 480
  ```
* If all camera applications show black frames, check camera hardware and drivers

---

### ❌ Missing module errors

```bash
python -m pip install opencv-python mediapipe numpy
```

---

## 🤖 Gesture Definitions

| Gesture       | Description                        | Label |
|---------------|------------------------------------|-------|
| 🖐️ Open palm | All fingers extended               | Hello |
| ✊ Fist       | All fingers closed                 | Stop  |
| ✌️ V-sign    | Index and middle fingers extended  | Peace |
| 👍 Thumb up  | Thumb vertical, other fingers down | Like  |
| 👌 OK sign   | Thumb and index finger touching    | Okay  |

---

## 🧾 Example Output

**Console/Overlay:**
```
Hello | conf=0.92 | FPS=29.7
```

Color bar is green since confidence ≥ 0.8.

**Session Statistics (`stats/session_stats.json`):**
```json
{
  "Hello": 10,
  "Stop": 4,
  "Peace": 6,
  "Like": 2,
  "Okay": 3,
  "duration_sec": 142
}
```

---

## 🧪 System Requirements

* **Python:** 3.8 or higher
* **OpenCV:** 4.8 or higher
* **MediaPipe:** 0.10 or higher
* **NumPy:** 1.24 or higher

---

## 🪪 License

MIT License — free for use, modification, and distribution.  
Hand landmark detection powered by Google's **MediaPipe**.

---

## 🧭 Future Enhancements

* Additional gesture definitions
* Per-gesture smoothing parameters
* Screenshot/video recording functionality
* CSV export for dataset creation and training

---

## ✨ Author

**Mahmoud Ahmad Hamam**  
📧 Email: [mahmoudhamam892@gmail.com](mailto:mahmoudhamam892@gmail.com)  
🔗 GitHub: [@02Mahmoudhamam](https://github.com/02Mahmoudhamam)

---

## 🧰 Quick Reference

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\Activate.ps1  # Windows

# Run application
python main.py --camera 0 --width 960 --height 540 --smooth 7

# Exit: Press 'q' or 'Esc'
# Statistics saved to: stats/session_stats.json
```

---

**Made with ❤️ using OpenCV and MediaPipe**
```