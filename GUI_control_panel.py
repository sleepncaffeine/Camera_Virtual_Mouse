import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

left_tasks = [
    "None",
    "copy",
    "paste",
    "undo",
    "redo",
    "go back",
    "go forward",
]


class GestureControlPanel:
    def __init__(self):
        self.img_scale_factor = 8

        self.is_running = True  # flag to stop the program
        self.debug = False
        self.show_cam = False
        self.show_command = False
        self.command_button = None
        self.smoothing = 5.0
        self.gesture_p = None  # pinky
        self.gesture_rp = None  # ring pinky
        self.gesture_mrp = None  # middle ring pinky
        self.gesture_imrp = None  # index middle ring pinky

    def load_img(self, img_path, w_factor, h_factor):
        img = Image.open(img_path)
        img = img.resize(
            (self.img_scale_factor * w_factor, self.img_scale_factor * h_factor),
            Image.LANCZOS,
        )
        photo_img = ImageTk.PhotoImage(img)
        return photo_img

    def create_r_gesture_label(self, frame, img_path, text, label_width):
        gesture_label = ttk.Label(frame, width=label_width)
        gesture_label.pack(side="left", padx=15, anchor="center")

        # Load and resize image
        photo_img = self.load_img(img_path, 5, 8)

        # Image Label
        image_label = ttk.Label(gesture_label, image=photo_img, anchor="center")
        image_label.image = photo_img
        image_label.pack()

        # Text Label
        text_label = ttk.Label(gesture_label, text=text, anchor="center")
        text_label.pack()

        return gesture_label

    def create_left_hand_gesture(
        self, parent_frame, img_path, gesture_combo_values, gesture_update_method
    ):
        gesture_frame = ttk.Frame(parent_frame, borderwidth=2)
        gesture_frame.pack(padx=10, side="left")

        # Load and resize image
        photo_img = self.load_img(img_path, 5, 8)

        gesture_label = ttk.Label(gesture_frame, image=photo_img)
        gesture_label.image = photo_img
        gesture_label.pack()

        gesture_combo = ttk.Combobox(
            gesture_frame, values=gesture_combo_values, width=10
        )
        gesture_combo.current(0)
        gesture_combo.pack(pady=5)
        gesture_combo.bind("<<ComboboxSelected>>", gesture_update_method)
        gesture_combo.bind(
            "<Return>", gesture_update_method
        )  # Update on Enter key press
        gesture_combo.bind(
            "<FocusOut>", gesture_update_method
        )  # Update when focus is lost

        return gesture_frame

    def close_window(self):
        self.is_running = False
        self.root.destroy()

    def toggle_debug(self):
        self.debug = not self.debug
        print("Debug mode:", "On" if self.debug else "Off")

    def toggle_show_cam(self):
        self.show_cam = not self.show_cam
        if self.command_button:
            self.command_button.config(
                state=tk.NORMAL if self.show_cam else tk.DISABLED
            )
        print("Show camera:", "On" if self.show_cam else "Off")

    def toggle_show_command(self):
        self.show_command = not self.show_command
        print("Show command:", "On" if self.show_command else "Off")

    def update_smoothing(self, value):
        self.smoothing = float(value)
        self.smoothing_label.config(text=f"Smoothing: {self.smoothing:.1f}")

    def update_gesture_p(self, event):
        self.gesture_p = event.widget.get()
        print(f"Pinky gesture: {self.gesture_p}")

    def update_gesture_rp(self, event):
        self.gesture_rp = event.widget.get()
        print(f"Ring pinky gesture: {self.gesture_rp}")

    def update_gesture_mrp(self, event):
        self.gesture_mrp = event.widget.get()
        print(f"Middle ring pinky gesture: {self.gesture_mrp}")

    def update_gesture_imrp(self, event):
        self.gesture_imrp = event.widget.get()
        print(f"Index middle ring pinky gesture: {self.gesture_imrp}")

    def run(self):
        self.root = ThemedTk(theme="arc")
        self.root.geometry("750x600+100+100")
        self.root.title("Hand Gesture Mouse Control Panel")
        self.root.iconbitmap("imgs/icon.ico")
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        title_label = ttk.Label(
            self.root, text="Hand Gesture Mouse Control Panel", font=("", 20)
        )
        title_label.pack()

        # User manual
        manual_frame = ttk.Frame(self.root, relief="groove", borderwidth=2)
        manual_frame.pack(pady=10, padx=10)

        manual_label = ttk.Label(
            manual_frame,
            text="User Manual\n"
            "1. Hold your hand in front of the camera\n"
            "2. Make the gesture for the desired action\n"
            "3. The action will be performed\n"
            "4. To change the action, select the action for desired gesture\n"
            "5. Or you can type your own hotkeys with '+' as the delimiter",
            justify="left",
        )
        manual_label.pack()

        # right hand commands info
        right_hand_commands_frame = ttk.Frame(self.root, relief="flat", borderwidth=2)
        right_hand_commands_frame.pack(pady=10, padx=10)

        right_hand_commands_label = ttk.Label(
            right_hand_commands_frame,
            text="Right Hand Gestures",
            justify="center",
            anchor="center",
        )
        right_hand_commands_label.pack(pady=5)

        std_label_w = 100

        self.create_r_gesture_label(
            right_hand_commands_frame, "imgs/move.png", "Move", std_label_w
        )

        self.create_r_gesture_label(
            right_hand_commands_frame, "imgs/click.png", "Click", std_label_w
        )

        self.create_r_gesture_label(
            right_hand_commands_frame, "imgs/rclick.png", "R click", std_label_w
        )

        self.create_r_gesture_label(
            right_hand_commands_frame, "imgs/drag.png", "Drag", std_label_w
        )

        self.create_r_gesture_label(
            right_hand_commands_frame, "imgs/scroll.png", "Scroll", std_label_w
        )

        # user key mapping
        ####################################################################
        # using combo box, default:None, options: left_tasks
        gesture_mapping = ttk.Frame(self.root, relief="flat", borderwidth=2)
        gesture_mapping.pack(pady=10, padx=10)

        gesture_mapping_label = ttk.Label(
            gesture_mapping, text="Left Hand Gesture Mapping", justify="left"
        )
        gesture_mapping_label.pack(pady=5)

        # pinky
        self.create_left_hand_gesture(
            gesture_mapping, "imgs/lp.png", left_tasks, self.update_gesture_p
        )

        # ring pinky
        self.create_left_hand_gesture(
            gesture_mapping, "imgs/lrp.png", left_tasks, self.update_gesture_rp
        )

        # middle ring pinky
        self.create_left_hand_gesture(
            gesture_mapping, "imgs/lmrp.png", left_tasks, self.update_gesture_mrp
        )

        # index middle ring pinky
        self.create_left_hand_gesture(
            gesture_mapping, "imgs/limrp.png", left_tasks, self.update_gesture_imrp
        )

        ####################################################################

        # Controls Frame
        control_frame = ttk.Frame(self.root, borderwidth=2)
        control_frame.pack(pady=10, padx=10)

        # Toggle cam
        cam_button = ttk.Checkbutton(
            control_frame,
            text="Toggle Camera",
            command=self.toggle_show_cam,
        )
        cam_button.pack(side="left")

        # Toggle show command
        self.command_button = ttk.Checkbutton(
            control_frame,
            text="Toggle Command",
            command=self.toggle_show_command,
            state="disabled",
        )
        self.command_button.pack(side="left")

        # Toggle debug mode
        debug_button = ttk.Checkbutton(
            control_frame, text="Toggle Debug", command=self.toggle_debug
        )
        debug_button.pack(side="left")

        # Slider for smoothing
        smoothing_frame = ttk.Frame(control_frame, borderwidth=2)
        smoothing_frame.pack(side="left", padx=10)

        self.smoothing_label = ttk.Label(
            smoothing_frame, text=f"Smoothing: {self.smoothing:.1f}"
        )
        self.smoothing_label.pack()

        smoothing_slider = ttk.Scale(
            smoothing_frame,
            from_=1.0,
            to=20.0,
            orient="horizontal",
            command=self.update_smoothing,
        )
        smoothing_slider.pack()

        # Exit button
        exit_button = ttk.Button(
            self.root, text="Exit", command=self.close_window, width=10
        )
        exit_button.pack(pady=10)

        self.root.mainloop()


if __name__ == "__main__":
    GestureControlPanel().run()
