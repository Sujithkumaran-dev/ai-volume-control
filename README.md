# 🎚️ AI Volume Control using Hand Tracking

This project is an AI-based system that allows users to control system volume using hand gestures captured through a webcam.

---

## 🚀 Features
- ✋ Real-time hand tracking
- 📏 Gesture-based volume control (finger distance)
- 🎯 Smooth and accurate control
- 🖥️ Works with system audio
- ⚡ Fast and lightweight

---

## 🛠️ Technologies Used
- Python
- OpenCV
- MediaPipe
- Pycaw
- NumPy

---

## 📌 How It Works
1. Webcam captures live video
2. Hand landmarks are detected using MediaPipe
3. Distance between thumb and index finger is calculated
4. Volume is adjusted based on the distance

---

## ▶️ How to Run

```bash
git clone https://github.com/Sujithkumaran-dev/ai-volume-control.git
cd ai-volume-control
pip install -r requirements.txt
python volume_control.py