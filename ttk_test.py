import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

smoothing = 5  # Adjustable
debug = False


root = ThemedTk(theme="arc")  # Specify a theme
root.geometry("500x400+100+100")
root.title("Hand Gesture Mouse Control Panel")

title_label = ttk.Label(root, text="Hand Gesture Mouse Control Panel")
title_label.pack()

# User manual
manual_frame = ttk.Frame(root, relief="groove", borderwidth=2)
manual_frame.pack(pady=10, padx=10)

# one img, one description
# image size= 50x50
manual_1 = ttk.Frame(manual_frame)
manual_1.pack(pady=10, padx=10)
manual_1_img = tk.PhotoImage(file="imgs/1.png")
manual_1_label = ttk.Label(manual_1, image=manual_1_img)
manual_1_label.pack(side="left")
manual_1_desc = ttk.Label(manual_1, text="V-shape: Cursor-moving state")
manual_1_desc.pack(side="left")


manual_2 = ttk.Frame(manual_frame)
manual_2.pack(pady=10, padx=10)
manual_2_img = tk.PhotoImage(file="imgs/2.png")
manual_2_label = ttk.Label(manual_2, image=manual_1_img)
manual_2_label.pack(side="left")
manual_2_desc = ttk.Label(manual_2, text="ㅇㄹㄹㄹ")
manual_2_desc.pack(side="left")


# Toggle debug mode
def toggle_debug():
    global debug
    debug = not debug


debug_button = ttk.Button(root, text="Toggle Debug", command=toggle_debug)
debug_button.pack()


# Slider for smoothing
def update_smoothing(value):
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
smoothing_value_label.pack()

root.mainloop()
