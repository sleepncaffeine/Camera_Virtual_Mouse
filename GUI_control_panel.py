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
        self.smoothing = 5.0
        self.gesture_p = None  # pinky
        self.gesture_rp = None  # ring pinky
        self.gesture_mrp = None  # middle ring pinky
        self.gesture_imrp = None  # index middle ring pinky

    def toggle_debug(self):
        self.debug = not self.debug
        print("Debug mode:", "On" if self.debug else "Off")

    def update_smoothing(self, value):
        self.smoothing = float(value)
        self.smoothing_value_label.config(text=f"Smoothing: {self.smoothing:.2f}")

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
        root.geometry("1200x400+100+100")
        root.title("Hand Gesture Mouse Control Panel")

        title_label = ttk.Label(root, text="Hand Gesture Mouse Control Panel")
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

        # user key mapping
        # using combo box, default:None, options: left_tasks
        gesture_mapping = ttk.Frame(root, relief="flat", borderwidth=2)
        gesture_mapping.pack(pady=10, padx=10)

        # pinky
        pinky_frame = ttk.Frame(gesture_mapping, borderwidth=2)
        pinky_frame.pack(pady=10, padx=10, side="left")
        pinky_label = ttk.Label(pinky_frame, text="Pinky")
        pinky_label.pack()
        pinky_combo = ttk.Combobox(pinky_frame, values=left_tasks, state="readonly")
        pinky_combo.current(0)
        pinky_combo.pack()
        pinky_combo.bind("<<ComboboxSelected>>", self.update_gesture_p)

        # ring pinky
        ring_pinky_frame = ttk.Frame(gesture_mapping, borderwidth=2)
        ring_pinky_frame.pack(pady=10, padx=10, side="left")
        ring_pinky_label = ttk.Label(ring_pinky_frame, text="Ring Pinky")
        ring_pinky_label.pack()
        ring_pinky_combo = ttk.Combobox(
            ring_pinky_frame, values=left_tasks, state="readonly"
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
            middle_ring_pinky_frame, values=left_tasks, state="readonly"
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
            index_middle_ring_pinky_frame, values=left_tasks, state="readonly"
        )
        index_middle_ring_pinky_combo.current(0)
        index_middle_ring_pinky_combo.pack()
        index_middle_ring_pinky_combo.bind(
            "<<ComboboxSelected>>", self.update_gesture_imrp
        )

        # Toggle debug mode
        debug_button = ttk.Button(root, text="Toggle Debug", command=self.toggle_debug)
        debug_button.pack()

        # Slider for smoothing
        smoothing_label = ttk.Label(root, text="Smoothing Slider:")
        smoothing_label.pack()

        smoothing_slider = ttk.Scale(
            root,
            from_=1.0,
            to=20.0,
            orient="horizontal",
            command=self.update_smoothing,
        )
        smoothing_slider.pack()

        self.smoothing_value_label = ttk.Label(
            root, text=f"Smoothing: {self.smoothing:.2f}"
        )
        self.smoothing_value_label.pack()

        root.mainloop()


if __name__ == "__main__":
    GestureControlPanel().run()
