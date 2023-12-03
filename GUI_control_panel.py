import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

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
        self.debug = False
        self.show_cam = False
        self.show_command = False
        self.command_button = None
        self.smoothing = 5.0
        self.gesture_p = None  # pinky
        self.gesture_rp = None  # ring pinky
        self.gesture_mrp = None  # middle ring pinky
        self.gesture_imrp = None  # index middle ring pinky

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
        root = ThemedTk(theme="arc")
        root.geometry("800x550+100+100")
        root.title("Hand Gesture Mouse Control Panel")
        root.iconbitmap("imgs/icon.ico")

        title_label = ttk.Label(
            root, text="Hand Gesture Mouse Control Panel", font=("", 20)
        )
        title_label.pack()

        # User manual
        manual_frame = ttk.Frame(root, relief="groove", borderwidth=2)
        manual_frame.pack(pady=10, padx=10)

        manual_label = ttk.Label(
            manual_frame,
            text="User Manual\n"
            "1. Hold your hand in front of the camera\n"
            "2. Make the gesture for the desired action\n"
            "3. The action will be performed\n"
            "4. To change the action, click on the button for the desired finger\n"
            "5. Then click on the button for the desired action",
            justify="left",
        )
        manual_label.pack()

        # right hand commands info
        right_hand_commands_frame = ttk.Frame(root, relief="flat", borderwidth=2)
        right_hand_commands_frame.pack(pady=10, padx=10)

        right_hand_commands_label = ttk.Label(
            right_hand_commands_frame,
            text="Right Hand Commands",
            justify="center",
            anchor="center",
        )
        right_hand_commands_label.grid(row=0, column=0, columnspan=6)

        move_cursor_label = ttk.Label(
            right_hand_commands_frame,
            text="Move Cursor\nIndex and Middle finger Open",
            justify="center",
            anchor="center",
        )
        move_cursor_label.grid(row=1, column=0, columnspan=2, padx=5)

        left_click_label = ttk.Label(
            right_hand_commands_frame,
            text="Left Click\nClose Index finger while moving",
            justify="center",
            anchor="center",
        )
        left_click_label.grid(row=1, column=2, columnspan=2, padx=5)

        right_click_label = ttk.Label(
            right_hand_commands_frame,
            text="Right Click\nClose Middle finger while moving",
            justify="center",
            anchor="center",
        )
        right_click_label.grid(row=1, column=4, columnspan=2, padx=5)

        drag_label = ttk.Label(
            right_hand_commands_frame,
            text="Drag\nClose Index and Middle finger while moving",
            justify="center",
            anchor="center",
        )
        drag_label.grid(row=2, column=0, columnspan=3, padx=5)

        scroll_label = ttk.Label(
            right_hand_commands_frame,
            text="Scroll\nClose all fingers except Index finger",
            justify="center",
            anchor="center",
        )
        scroll_label.grid(row=2, column=4, columnspan=3, padx=5)

        # user key mapping
        ####################################################################
        # using combo box, default:None, options: left_tasks
        gesture_mapping = ttk.Frame(root, relief="flat", borderwidth=2)
        gesture_mapping.pack(pady=10, padx=10)

        gesture_mapping_label = ttk.Label(
            gesture_mapping, text="Left Hand Gesture Mapping", justify="left"
        )
        gesture_mapping_label.pack()

        # pinky
        pinky_frame = ttk.Frame(gesture_mapping, borderwidth=2)
        pinky_frame.pack(pady=10, padx=10, side="left")
        pinky_label = ttk.Label(pinky_frame, text="Pinky")
        pinky_label.pack()
        pinky_combo = ttk.Combobox(
            pinky_frame, values=left_tasks, state="readonly", width=10
        )
        pinky_combo.current(0)
        pinky_combo.pack()
        pinky_combo.bind("<<ComboboxSelected>>", self.update_gesture_p)

        # ring pinky
        ring_pinky_frame = ttk.Frame(gesture_mapping, borderwidth=2)
        ring_pinky_frame.pack(pady=10, padx=10, side="left")
        ring_pinky_label = ttk.Label(ring_pinky_frame, text="Ring Pinky")
        ring_pinky_label.pack()
        ring_pinky_combo = ttk.Combobox(
            ring_pinky_frame, values=left_tasks, state="readonly", width=10
        )
        ring_pinky_combo.current(0)
        ring_pinky_combo.pack()
        ring_pinky_combo.bind("<<ComboboxSelected>>", self.update_gesture_rp)

        # middle ring pinky
        middle_ring_pinky_frame = ttk.Frame(gesture_mapping, borderwidth=2)
        middle_ring_pinky_frame.pack(pady=10, padx=10, side="left")
        middle_ring_pinky_label = ttk.Label(
            middle_ring_pinky_frame, text="Middle Ring Pinky"
        )
        middle_ring_pinky_label.pack()
        middle_ring_pinky_combo = ttk.Combobox(
            middle_ring_pinky_frame, values=left_tasks, state="readonly", width=10
        )
        middle_ring_pinky_combo.current(0)
        middle_ring_pinky_combo.pack()
        middle_ring_pinky_combo.bind("<<ComboboxSelected>>", self.update_gesture_mrp)

        # index middle ring pinky
        index_middle_ring_pinky_frame = ttk.Frame(gesture_mapping, borderwidth=2)
        index_middle_ring_pinky_frame.pack(pady=10, padx=10, side="left")
        index_middle_ring_pinky_label = ttk.Label(
            index_middle_ring_pinky_frame, text="Index Middle Ring Pinky"
        )
        index_middle_ring_pinky_label.pack()
        index_middle_ring_pinky_combo = ttk.Combobox(
            index_middle_ring_pinky_frame, values=left_tasks, state="readonly", width=10
        )
        index_middle_ring_pinky_combo.current(0)
        index_middle_ring_pinky_combo.pack()
        index_middle_ring_pinky_combo.bind(
            "<<ComboboxSelected>>", self.update_gesture_imrp
        )

        ####################################################################

        # Controls Frame
        control_frame = ttk.Frame(root, borderwidth=2)
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
            root, text="Exit", command=root.destroy, width=20, padding=5
        )
        exit_button.pack(pady=10)

        root.mainloop()


if __name__ == "__main__":
    GestureControlPanel().run()
