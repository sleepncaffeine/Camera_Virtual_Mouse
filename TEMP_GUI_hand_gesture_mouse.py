import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk
from threading import Thread

# import tkinter as tk

smoothing = 5  # Adjustable
debug = False


def run_tkinter():
    root = ThemedTk(theme="arc")  # Specify a theme
    root.geometry("500x400+100+100")
    root.title("Hand Gesture Mouse Control Panel")

    title_label = ttk.Label(root, text="Hand Gesture Mouse Control Panel")
    title_label.pack()

    # User manual
    manual_frame = ttk.Frame(root)

    # Toggle debug mode
    def toggle_debug():
        global debug
        debug = not debug

    debug_button = ttk.Button(root, text="Toggle Debug", command=toggle_debug)
    debug_button.pack()

    root.mainloop()


def run_cam():
    pyautogui.FAILSAFE = True

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
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

        fingers_open = [False, False, False, False, False]

        if results.multi_hand_landmarks:
            for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = (
                    results.multi_handedness[hand_index].classification[0].label
                )
                if handedness != "Left":  # Mirrored image, right hand functional
                    continue

                landmarks = hand_landmarks.landmark

                tip_ids = [
                    mp_hands.HandLandmark.THUMB_TIP,
                    mp_hands.HandLandmark.INDEX_FINGER_TIP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                    mp_hands.HandLandmark.RING_FINGER_TIP,
                    mp_hands.HandLandmark.PINKY_TIP,
                ]
                finger_tips = [landmarks[tip_id] for tip_id in tip_ids]

                # Thumb
                pseudo_fix_key = landmarks[2].x
                if not (
                    landmarks[3].x < pseudo_fix_key and landmarks[4].x < pseudo_fix_key
                ):
                    fingers_open[0] = True

                # Index Finger
                pseudo_fix_key = landmarks[6].y
                if landmarks[7].y < pseudo_fix_key and landmarks[8].y < pseudo_fix_key:
                    fingers_open[1] = True

                # Middle Finger
                pseudo_fix_key = landmarks[10].y
                if (
                    landmarks[11].y < pseudo_fix_key
                    and landmarks[12].y < pseudo_fix_key
                ):
                    fingers_open[2] = True

                # Ring Finger
                pseudo_fix_key = landmarks[14].y
                if (
                    landmarks[15].y < pseudo_fix_key
                    and landmarks[16].y < pseudo_fix_key
                ):
                    fingers_open[3] = True

                # Pinky
                pseudo_fix_key = landmarks[18].y
                if (
                    landmarks[19].y < pseudo_fix_key
                    and landmarks[20].y < pseudo_fix_key
                ):
                    fingers_open[4] = True

                # Gesture recognition
                if fingers_open == [0, 1, 1, 0, 0]:  # V-shape: Cursor-moving state
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                    has_clicked = False  # Reset click state
                    x = int(finger_tips[1].x * screen_width)
                    y = int(finger_tips[1].y * screen_height)

                    # Smoothing formula
                    clocX = plocX + (x - plocX) / smoothing
                    clocY = plocY + (y - plocY) / smoothing

                    pyautogui.moveTo(screen_width - clocX, clocY)
                    plocX, plocY = clocX, clocY

                elif (
                    fingers_open == [0, 0, 1, 0, 0] and not has_clicked
                ):  # Only middle finger open: Left click
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                    pyautogui.click()
                    has_clicked = True  # Set click state to prevent multiple clicks

                elif (
                    fingers_open == [0, 1, 0, 0, 0] and not has_clicked
                ):  # Only index finger open: Right click
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                    pyautogui.rightClick()
                    has_clicked = True  # Set click state to prevent multiple clicks

                # Scroll gesture
                if fingers_open == [0, 0, 1, 1, 1]:
                    scroll_y = (
                        landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
                        * screen_height
                    )
                    if scroll_y > screen_height / 2:
                        pyautogui.scroll(-50)  # Scroll down
                    else:
                        pyautogui.scroll(50)  # Scroll up

                if debug:
                    mp_draw.draw_landmarks(
                        img, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )
                    print(fingers_open)

        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


tkinter_thread = Thread(target=run_tkinter)
tkinter_thread.start()

run_cam()
