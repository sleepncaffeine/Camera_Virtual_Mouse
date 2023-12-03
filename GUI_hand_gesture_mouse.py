import cv2
import mediapipe as mp
import pyautogui
from GUI_control_panel import GestureControlPanel
from threading import Thread


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


# //TODO: Add custom function
def do_custom_function(keys):
    keys = keys.split("+").strip()
    pyautogui.hotkey(*keys)


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

control_panel = GestureControlPanel()


def run_cam():
    pyautogui.FAILSAFE = True

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    is_dragging = False
    has_clicked = False  # Track if click has been performed
    has_gestured = False  # Track if gesture has been performed

    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
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
                    clocX = plocX + (x - plocX) / control_panel.smoothing
                    clocY = plocY + (y - plocY) / control_panel.smoothing

                    pyautogui.moveTo(screen_width - clocX, clocY)
                    plocX, plocY = clocX, clocY
                    if control_panel.show_command:
                        cv2.putText(
                            img,
                            "Moving",
                            (10, 70),
                            font,
                            3,
                            (0, 0, 255),
                            2,
                            cv2.LINE_AA,
                        )

                elif (
                    fingers_open == [0, 1, 0, 0] and not has_clicked
                ):  # Only middle finger open: Left click
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                    pyautogui.click()
                    has_clicked = True  # Set click state to prevent multiple clicks
                    if control_panel.show_command:
                        cv2.putText(
                            img,
                            "Left Click",
                            (10, 70),
                            font,
                            3,
                            (0, 0, 255),
                            2,
                            cv2.LINE_AA,
                        )

                elif (
                    fingers_open == [1, 0, 0, 0] and not has_clicked
                ):  # Only index finger open: Right click
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                    pyautogui.rightClick()
                    has_clicked = True  # Set click state to prevent multiple clicks
                    if control_panel.show_command:
                        cv2.putText(
                            img,
                            "Right Click",
                            (10, 70),
                            font,
                            3,
                            (0, 0, 255),
                            2,
                            cv2.LINE_AA,
                        )

                # Index finger closed: Scroll
                elif fingers_open == [0, 1, 1, 1]:
                    scroll_y = (
                        landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
                        * screen_height
                    )
                    if scroll_y > screen_height / 2:
                        pyautogui.scroll(-120)  # Scroll down
                        if control_panel.show_command:
                            cv2.putText(
                                img,
                                "Scroll Down",
                                (10, 70),
                                font,
                                3,
                                (0, 0, 255),
                                2,
                                cv2.LINE_AA,
                            )
                    else:
                        pyautogui.scroll(120)  # Scroll up
                        if control_panel.show_command:
                            cv2.putText(
                                img,
                                "Scroll Up",
                                (10, 70),
                                font,
                                3,
                                (0, 0, 255),
                                2,
                                cv2.LINE_AA,
                            )

                # Only ring finger closed: Drag
                elif fingers_open == [0, 0, 0, 0]:
                    if not is_dragging:
                        pyautogui.mouseDown()
                        is_dragging = True
                    x = int(finger_tips[1].x * screen_width)
                    y = int(finger_tips[1].y * screen_height)
                    pyautogui.moveTo(screen_width - x, y)
                    has_clicked = False  # Reset click state
                    if control_panel.show_command:
                        cv2.putText(
                            img,
                            "Drag",
                            (10, 70),
                            font,
                            3,
                            (0, 0, 255),
                            2,
                            cv2.LINE_AA,
                        )
                else:
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                    has_clicked = False

                if control_panel.debug:
                    print("R:", thumb_open, fingers_open)
                    if control_panel.show_cam:
                        mp_draw.draw_landmarks(
                            img, hand_landmarks, mp_hands.HAND_CONNECTIONS
                        )

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

                # L_tip_ids = [
                #     mp_hands.HandLandmark.THUMB_TIP,
                #     mp_hands.HandLandmark.INDEX_FINGER_TIP,
                #     mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                #     mp_hands.HandLandmark.RING_FINGER_TIP,
                #     mp_hands.HandLandmark.PINKY_TIP,
                # ]
                # L_finger_tips = [L_landmarks[tip_id] for tip_id in L_tip_ids]

                # Thumb
                L_pseudo_fix_key = L_landmarks[2].x
                if (
                    L_landmarks[3].x < L_pseudo_fix_key
                    and L_landmarks[4].x < L_pseudo_fix_key
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

                # gesture_p  [1, 1, 1, 0]
                if L_fingers_open == [1, 1, 1, 0]:
                    if control_panel.gesture_p in function_map and not has_gestured:
                        function_map[control_panel.gesture_p]()
                        has_gestured = True
                        if control_panel.debug:
                            print(control_panel.gesture_p)
                        if control_panel.show_command:
                            cv2.putText(
                                img,
                                control_panel.gesture_p,
                                (10, 150),
                                font,
                                3,
                                (0, 255, 0),
                                2,
                                cv2.LINE_AA,
                            )

                # gesture_rp  [1, 1, 0, 0]
                if L_fingers_open == [1, 1, 0, 0]:
                    if control_panel.gesture_rp in function_map and not has_gestured:
                        function_map[control_panel.gesture_rp]()
                        has_gestured = True
                        if control_panel.debug:
                            print(control_panel.gesture_rp)
                        if control_panel.show_command:
                            cv2.putText(
                                img,
                                control_panel.gesture_rp,
                                (10, 150),
                                font,
                                3,
                                (0, 255, 0),
                                2,
                                cv2.LINE_AA,
                            )

                # gesture_mrp [1, 0, 0, 0]
                elif L_fingers_open == [1, 0, 0, 0]:
                    if control_panel.gesture_mrp in function_map and not has_gestured:
                        function_map[control_panel.gesture_mrp]()
                        has_gestured = True
                        if control_panel.debug:
                            print(control_panel.gesture_mrp)
                        if control_panel.show_command:
                            cv2.putText(
                                img,
                                control_panel.gesture_mrp,
                                (10, 150),
                                font,
                                3,
                                (0, 255, 0),
                                2,
                                cv2.LINE_AA,
                            )

                # gesture_imrp [0, 0, 0, 0]
                elif L_fingers_open == [0, 0, 0, 0]:
                    if control_panel.gesture_imrp in function_map and not has_gestured:
                        function_map[control_panel.gesture_imrp]()
                        has_gestured = True
                        if control_panel.debug:
                            print(control_panel.gesture_imrp)
                        if control_panel.show_command:
                            cv2.putText(
                                img,
                                control_panel.gesture_imrp,
                                (10, 150),
                                font,
                                3,
                                (0, 255, 0),
                                2,
                                cv2.LINE_AA,
                            )

                else:
                    has_gestured = False

                if control_panel.debug:
                    print("L:", L_thumb_open, L_fingers_open)
                    if control_panel.show_cam:
                        mp_draw.draw_landmarks(
                            img,
                            L_hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_draw.DrawingSpec(color=(0, 255, 0)),
                        )

        if control_panel.show_cam:
            cv2.imshow("Hand Tracking", img)
        if not control_panel.show_cam and cv2.getWindowProperty(
            "Hand Tracking", cv2.WND_PROP_VISIBLE
        ):
            cv2.destroyWindow("Hand Tracking")

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if control_panel.is_running == False:
            break

    cap.release()
    cv2.destroyAllWindows()
    exit()


# Start Control panel GUI
tkinter_thread = Thread(target=control_panel.run)
tkinter_thread.start()

# Start camera
run_cam()

tkinter_thread.join()  # Wait for control panel to close
