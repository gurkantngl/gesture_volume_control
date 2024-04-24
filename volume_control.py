import cv2 
import mediapipe as mp
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


x1 = y1 = x2 = y2 = 0
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

def set_volume(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = cast(interface, POINTER(IAudioEndpointVolume))

    # 0-100 aralığından -65.25-0.0 aralığına dönüştür
    new_volume = -65.25 + (volume / 100 * 65.25)

    # ses seviyesini ayarla
    volume_interface.SetMasterVolumeLevel(new_volume, None)

while True:
    _, image = webcam.read()
    image = cv2.flip(image,1)
    frame_height, frame_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=image, center=(x,y), radius=8, color=(0,255,255), thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv2.circle(img=image, center=(x,y), radius=8, color=(0,0,255), thickness=3)
                    x2 = x
                    y2 = y
        dist = ((x2-x1)**2 + (y2-y1)**2)**0.5//4
        cv2.line(image, (x1, y1), (x2, y2), (0,255,0),5)
        if dist > 100:
            dist = 100
        set_volume(dist)
                    
    cv2.imshow("MediaPipe Hand", image)
    key = cv2.waitKey(1)
    if key == 27:
        break
webcam.release()
cv2.destroyAllWindows()