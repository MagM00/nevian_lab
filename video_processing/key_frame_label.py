import tkinter as tk
from tkinter import filedialog, ttk
import cv2
import pandas as pd
from PIL import Image, ImageTk
import os

class VideoPlayer:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # Canvas for video playback
        self.canvas = tk.Canvas(window, width=1920, height=1080)
        self.canvas.pack()

        # Frame number display
        self.frame_number = tk.Entry(window)
        self.frame_number.pack()

        # Slider for frame navigation
        self.slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, command=self.slider_used)
        self.slider.pack()

        # Dropdown menu for event logging
        self.event_var = tk.StringVar(window)
        self.event_options = {"4: Cold water", "5: Room temp", "6: Hot water", 
                              "0: Pinprick", "1: 0.07g", "2: 0.4g", "3: 2g"}
        self.event_var.set("Select Event")
        self.dropdown = tk.OptionMenu(window, self.event_var, *self.event_options)
        self.dropdown.pack()

        # Log button
        self.btn_log = tk.Button(window, text="Log Event", command=self.log_event)
        self.btn_log.pack()

        # Load video button
        self.btn_load = tk.Button(window, text="Load Video", command=self.load_video)
        self.btn_load.pack()

        # Frame navigation buttons
        self.btn_forward_900 = tk.Button(window, text="Forward 900 frames", command=lambda: self.jump_frames(900))
        self.btn_forward_900.pack(side=tk.LEFT)

        self.btn_backward_900 = tk.Button(window, text="Backward 900 frames", command=lambda: self.jump_frames(-900))
        self.btn_backward_900.pack(side=tk.LEFT)

        self.btn_forward_10 = tk.Button(window, text="Forward 10 frames", command=lambda: self.jump_frames(10))
        self.btn_forward_10.pack(side=tk.LEFT)

        self.btn_backward_10 = tk.Button(window, text="Backward 10 frames", command=lambda: self.jump_frames(-10))
        self.btn_backward_10.pack(side=tk.LEFT)

        self.video_source = None
        self.vid = None
        self.log_data = []

    def load_video(self):
        self.video_source = filedialog.askopenfilename()
        if self.video_source:
            self.vid = cv2.VideoCapture(self.video_source)
            self.slider.configure(to=self.vid.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
            self.update()

    def slider_used(self, _):
        if self.vid:
            frame_no = self.slider.get()
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            self.update()

    def jump_frames(self, frame_count):
        if self.vid:
            frame_no = int(self.frame_number.get() or 0) + frame_count
            frame_no = max(0, min(frame_no, self.vid.get(cv2.CAP_PROP_FRAME_COUNT) - 1))
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            self.slider.set(frame_no)
            self.update()

    def log_event(self):
        if self.vid and self.event_var.get() != "Select Event":
            current_frame = int(self.vid.get(cv2.CAP_PROP_POS_FRAMES))
            self.log_data.append([self.event_var.get(), current_frame])
            # Save to Excel file
            df = pd.DataFrame(self.log_data, columns=['Event', 'Frame'])
            df.to_excel(os.path.splitext(self.video_source)[0] + "_log.xlsx", index=False)

    def update(self):
        if self.vid:
            ret, frame = self.vid.read()
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

                # Update frame number
                current_frame = int(self.vid.get(cv2.CAP_PROP_POS_FRAMES))
                self.frame_number.delete(0, tk.END)
                self.frame_number.insert(0, str(current_frame))
                self.slider.set(current_frame)

    def __del__(self):
        if self.vid:
            self.vid.release()

# Create a window and pass it to the video player
root = tk.Tk()
VideoPlayer(root, "Tkinter and OpenCV with Event Logger")
root.mainloop()
