import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

print("🚀 Program Started")

# -------------------- VOLUME SETUP --------------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Volume range
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# -------------------- MEDIAPIPE SETUP --------------------
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# -------------------- CAMERA --------------------
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        print("❌ Camera not working")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []

            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            # Thumb tip (4) and Index tip (8)
            x1, y1 = lmList[4]
            x2, y2 = lmList[8]

            # Draw points
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            # Distance
            length = math.hypot(x2 - x1, y2 - y1)

            # Convert to volume
            vol = np.interp(length, [30, 200], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)

            # Volume bar
            volBar = np.interp(length, [30, 200], [400, 150])
            volPer = np.interp(length, [30, 200], [0, 100])

            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)} %', (40, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Volume Control", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()