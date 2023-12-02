import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk
from threading import Thread

# global var
smoothing = 5  # Adjustable
debug = False
gesture_RP = None


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

    # Slider for smoothing
    """def update_smoothing(value):
        global smoothing
        smoothing = float(value)
        smoothing_value_label.config(text=f"Smoothing: {smoothing:.2f}")

    smoothing_label = ttk.Label(root, text="Smoothing Slider:")
    smoothing_label.pack()

    smoothing_slider = ttk.Scale(
        root, from_=1, to=10, orient="horizontal", command=update_smoothing 
    )
    smoothing_slider.set(smoothing)
    smoothing_slider.pack()

    smoothing_value_label = ttk.Label(root, text=f"Smoothing: {smoothing:.2f}")
    smoothing_value_label.pack()"""

    root.mainloop()


def do_copy():
    pyautogui.hotkey("ctrl", "c")


def do_paste():
    pyautogui.hotkey("ctrl", "v")


def do_undo():
    pyautogui.hotkey("ctrl", "z")


def do_redo():
    pyautogui.hotkey("ctrl", "y")


def do_go_back():
    pyautogui.hotkey("alt", "left")


def do_go_forward():
    pyautogui.hotkey("alt", "right")


left_tasks = [
    "copy",
    "paste",
    "undo",
    "redo",
    "go back",
    "go forward",
]

function_map = {
    "copy": do_copy,
    "paste": do_paste,
    "undo": do_undo,
    "redo": do_redo,
    "go back": do_go_back,
    "go forward": do_go_forward,
}


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

        ########################################
        # For Right Hand
        ########################################
        if results.multi_hand_landmarks:
            for L_hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = (
                    results.multi_handedness[L_hand_index].classification[0].label
                )
                if handedness != "Left":  # Mirrored image, right hand functional
                    continue

                landmarks = hand_landmarks.landmark

                fingers_open = [False, False, False, False]
                thumb_open = False

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
                    thumb_open = True

                # Index Finger
                pseudo_fix_key = landmarks[6].y
                if landmarks[7].y < pseudo_fix_key and landmarks[8].y < pseudo_fix_key:
                    fingers_open[0] = True

                # Middle Finger
                pseudo_fix_key = landmarks[10].y
                if (
                    landmarks[11].y < pseudo_fix_key
                    and landmarks[12].y < pseudo_fix_key
                ):
                    fingers_open[1] = True

                # Ring Finger
                pseudo_fix_key = landmarks[14].y
                if (
                    landmarks[15].y < pseudo_fix_key
                    and landmarks[16].y < pseudo_fix_key
                ):
                    fingers_open[2] = True

                # Pinky
                pseudo_fix_key = landmarks[18].y
                if (
                    landmarks[19].y < pseudo_fix_key
                    and landmarks[20].y < pseudo_fix_key
                ):
                    fingers_open[3] = True

                # Gesture recognition
                # V-shape: Cursor-moving state
                if fingers_open == [1, 1, 0, 0]:  # Ignored thumb for anlge issue
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
                    fingers_open == [0, 1, 0, 0] and not has_clicked
                ):  # Only middle finger open: Left click
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                    pyautogui.click()
                    has_clicked = True  # Set click state to prevent multiple clicks

                elif (
                    fingers_open == [1, 0, 0, 0] and not has_clicked
                ):  # Only index finger open: Right click
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                    pyautogui.rightClick()
                    has_clicked = True  # Set click state to prevent multiple clicks

                # Index finger closed: Scroll
                if fingers_open == [0, 1, 1, 1]:
                    scroll_y = (
                        landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
                        * screen_height
                    )
                    if scroll_y > screen_height / 2:
                        pyautogui.scroll(-60)  # Scroll down
                    else:
                        pyautogui.scroll(60)  # Scroll up

                # All fingers closed: Drag
                if fingers_open == [0, 0, 0, 0] and not thumb_open:
                    if not is_dragging:
                        pyautogui.mouseDown()
                        is_dragging = True
                    x = int(finger_tips[1].x * screen_width)
                    y = int(finger_tips[1].y * screen_height)
                    pyautogui.moveTo(screen_width - x, y)
                    has_clicked = False  # Reset click state
                else:
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                    has_clicked = False

                if debug:
                    mp_draw.draw_landmarks(
                        img, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )
                    print(thumb_open, fingers_open)

        ########################################
        # For Left Hand
        ########################################
        if results.multi_hand_landmarks:
            for L_hand_index, L_hand_landmarks in enumerate(
                results.multi_hand_landmarks
            ):
                L_handedness = (
                    results.multi_handedness[L_hand_index].classification[0].label
                )
                if L_handedness != "Right":  # Mirrored image, left hand functional
                    continue

                L_landmarks = L_hand_landmarks.landmark

                L_fingers_open = [False, False, False, False]
                L_thumb_open = False

                L_tip_ids = [
                    mp_hands.HandLandmark.THUMB_TIP,
                    mp_hands.HandLandmark.INDEX_FINGER_TIP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                    mp_hands.HandLandmark.RING_FINGER_TIP,
                    mp_hands.HandLandmark.PINKY_TIP,
                ]
                L_finger_tips = [L_landmarks[tip_id] for tip_id in L_tip_ids]

                # Thumb
                L_pseudo_fix_key = L_landmarks[2].x
                if not (
                    L_landmarks[3].x < pseudo_fix_key
                    and L_landmarks[4].x < pseudo_fix_key
                ):
                    L_thumb_open = True

                # Index Finger
                L_pseudo_fix_key = L_landmarks[6].y
                if (
                    L_landmarks[7].y < L_pseudo_fix_key
                    and L_landmarks[8].y < L_pseudo_fix_key
                ):
                    L_fingers_open[0] = True

                # Middle Finger
                L_pseudo_fix_key = L_landmarks[10].y
                if (
                    L_landmarks[11].y < L_pseudo_fix_key
                    and L_landmarks[12].y < L_pseudo_fix_key
                ):
                    L_fingers_open[1] = True

                # Ring Finger
                L_pseudo_fix_key = L_landmarks[14].y
                if (
                    L_landmarks[15].y < L_pseudo_fix_key
                    and L_landmarks[16].y < L_pseudo_fix_key
                ):
                    L_fingers_open[2] = True

                # Pinky
                L_pseudo_fix_key = L_landmarks[18].y
                if (
                    L_landmarks[19].y < L_pseudo_fix_key
                    and L_landmarks[20].y < L_pseudo_fix_key
                ):
                    L_fingers_open[3] = True

                # Gesture recognition
                # gesture_rp 1, [1, 1, 0, 0]
                if L_fingers_open == [1, 1, 0, 0]:
                    if gesture_RP in function_map:
                        function_map[gesture_RP]()

                mp_draw.draw_landmarks(
                    img,
                    L_hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0)),
                )

        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


tkinter_thread = Thread(target=run_tkinter)
tkinter_thread.start()

run_cam()
