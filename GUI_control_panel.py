import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import PhotoImage
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

    def create_r_gesture_label(self, frame, img_path, text, label_width):
        gesture_label = ttk.Label(frame, width=label_width)
        gesture_label.pack(side="left", padx=15, anchor="center")

        # Load and resize image
        img = Image.open(img_path)
        scale_factor = 8
        icons_w = 5 * scale_factor
        icons_h = 8 * scale_factor
        img = img.resize((icons_w, icons_h), Image.LANCZOS)
        photo_img = ImageTk.PhotoImage(img)

        # Image Label
        image_label = ttk.Label(gesture_label, image=photo_img, anchor="center")
        image_label.image = photo_img
        image_label.pack()

        # Text Label
        text_label = ttk.Label(gesture_label, text=text, anchor="center")
        text_label.pack()

        return gesture_label

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

        scale_factor = 8
        icons_w = 5 * scale_factor
        icons_h = 8 * scale_factor
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
        pinky_frame = ttk.Frame(gesture_mapping, borderwidth=2)
        pinky_frame.pack(padx=10, side="left")
        pinky_img = Image.open("imgs/lp.png")
        pinky_img = pinky_img.resize((icons_w, icons_h), Image.LANCZOS)
        pinky_image = ImageTk.PhotoImage(pinky_img)
        pinky_label = ttk.Label(pinky_frame, image=pinky_image)
        pinky_label.pack()
        pinky_combo = ttk.Combobox(pinky_frame, values=left_tasks, width=10)
        pinky_combo.current(0)
        pinky_combo.pack(pady=5)
        pinky_combo.bind("<<ComboboxSelected>>", self.update_gesture_p)
        pinky_combo.bind("<Return>", self.update_gesture_p)  # Update on Enter key press
        pinky_combo.bind(
            "<FocusOut>", self.update_gesture_p
        )  # Update when focus is lost

        # ring pinky
        ring_pinky_frame = ttk.Frame(gesture_mapping, borderwidth=2)
        ring_pinky_frame.pack(padx=10, side="left")
        ring_pinky_img = Image.open("imgs/lrp.png")
        ring_pinky_img = ring_pinky_img.resize((icons_w, icons_h), Image.LANCZOS)
        ring_pinky_image = ImageTk.PhotoImage(ring_pinky_img)
        ring_pinky_label = ttk.Label(ring_pinky_frame, image=ring_pinky_image)
        ring_pinky_label.pack()
        ring_pinky_combo = ttk.Combobox(ring_pinky_frame, values=left_tasks, width=10)
        ring_pinky_combo.current(0)
        ring_pinky_combo.pack(pady=5)
        ring_pinky_combo.bind("<<ComboboxSelected>>", self.update_gesture_rp)
        ring_pinky_combo.bind("<Return>", self.update_gesture_rp)
        ring_pinky_combo.bind("<FocusOut>", self.update_gesture_rp)

        # middle ring pinky
        middle_ring_pinky_frame = ttk.Frame(gesture_mapping, borderwidth=2)
        middle_ring_pinky_frame.pack(padx=10, side="left")
        middle_ring_pinky_img = Image.open("imgs/lmrp.png")
        middle_ring_pinky_img = middle_ring_pinky_img.resize(
            (icons_w, icons_h), Image.LANCZOS
        )
        middle_ring_pinky_image = ImageTk.PhotoImage(middle_ring_pinky_img)
        middle_ring_pinky_label = ttk.Label(
            middle_ring_pinky_frame,
            image=middle_ring_pinky_image,
        )
        middle_ring_pinky_label.pack()
        middle_ring_pinky_combo = ttk.Combobox(
            middle_ring_pinky_frame, values=left_tasks, width=10
        )
        middle_ring_pinky_combo.current(0)
        middle_ring_pinky_combo.pack(pady=5)
        middle_ring_pinky_combo.bind("<<ComboboxSelected>>", self.update_gesture_mrp)
        middle_ring_pinky_combo.bind("<Return>", self.update_gesture_mrp)
        middle_ring_pinky_combo.bind("<FocusOut>", self.update_gesture_mrp)

        # index middle ring pinky
        index_middle_ring_pinky_frame = ttk.Frame(gesture_mapping, borderwidth=2)
        index_middle_ring_pinky_frame.pack(padx=10, side="left")
        index_middle_ring_pinky_img = Image.open("imgs/limrp.png")
        index_middle_ring_pinky_img = index_middle_ring_pinky_img.resize(
            (icons_w, icons_h), Image.LANCZOS
        )
        index_middle_ring_pinky_image = ImageTk.PhotoImage(index_middle_ring_pinky_img)
        index_middle_ring_pinky_label = ttk.Label(
            index_middle_ring_pinky_frame,
            image=index_middle_ring_pinky_image,
        )
        index_middle_ring_pinky_label.pack()
        index_middle_ring_pinky_combo = ttk.Combobox(
            index_middle_ring_pinky_frame, values=left_tasks, width=10
        )
        index_middle_ring_pinky_combo.current(0)
        index_middle_ring_pinky_combo.pack(pady=5)
        index_middle_ring_pinky_combo.bind(
            "<<ComboboxSelected>>", self.update_gesture_imrp
        )
        index_middle_ring_pinky_combo.bind("<Return>", self.update_gesture_imrp)
        index_middle_ring_pinky_combo.bind("<FocusOut>", self.update_gesture_imrp)

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
