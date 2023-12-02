import cv2
import math
import mediapipe as mp
import pyautogui
import tkinter as tk
import tkinter.ttk as ttk

pyautogui.FAILSAFE = True

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothing = 5  # Adjustable
is_dragging = False
has_clicked = False  # Track if click has been performed

cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()
while True:
    success, img = cap.read()
    if not success:
        continue

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[hand_index].classification[0].label
            if handedness != "Left":  # Mirrored image, right hand functional
                continue

            landmarks = hand_landmarks.landmark
            tip_ids = [
                mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP,
            ]
            finger_tips = [landmarks[tip_id] for tip_id in tip_ids]

            fingers_open = [
                tip.y < landmarks[tip_ids[i] - 2].y for i, tip in enumerate(finger_tips)
            ]

            # Gesture recognition
            if fingers_open == [
                True,
                True,
                False,
                False,
            ]:  # V-shape: Cursor-moving state
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False
                has_clicked = False  # Reset click state
                x = int(finger_tips[0].x * screen_width)
                y = int(finger_tips[0].y * screen_height)

                # Smoothing formula
                clocX = plocX + (x - plocX) / smoothing
                clocY = plocY + (y - plocY) / smoothing

                pyautogui.moveTo(screen_width - clocX, clocY)
                plocX, plocY = clocX, clocY

            elif (
                fingers_open == [False, True, False, False] and not has_clicked
            ):  # Only middle finger open: Left click
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False
                pyautogui.click()
                has_clicked = True  # Set click state to prevent multiple clicks

            elif (
                fingers_open == [True, False, False, False] and not has_clicked
            ):  # Only index finger open: Right click
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False
                pyautogui.rightClick()
                has_clicked = True  # Set click state to prevent multiple clicks

            """elif not any(fingers_open):  # All fingers closed: Drag state
                if not is_dragging:
                    pyautogui.mouseDown()
                    is_dragging = True
                x = int(finger_tips[0].x * screen_width)
                y = int(finger_tips[0].y * screen_height)
                pyautogui.moveTo(screen_width - x, y)
                has_clicked = False  # Reset click state

            else:
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False
                has_clicked = False  # Reset click state"""

            # Scroll gesture
            if fingers_open == [False, True, True, True]:
                scroll_y = (
                    landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * screen_height
                )
                if scroll_y > screen_height / 2:
                    pyautogui.scroll(-50)  # Scroll down
                else:
                    pyautogui.scroll(50)  # Scroll up

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            print(fingers_open)

    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
