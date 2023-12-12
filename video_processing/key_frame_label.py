import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

class VideoPlayer:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # Create a canvas for video playback
        self.canvas = tk.Canvas(window, width=1200, height=900)
        self.canvas.pack()

        # Frame number display
        self.frame_number = tk.Entry(window)
        self.frame_number.pack()

        # Buttons
        self.btn_load = tk.Button(window, text="Load Video", command=self.load_video)
        self.btn_load.pack(side=tk.LEFT)

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

    def load_video(self):
        self.video_source = filedialog.askopenfilename()
        self.vid = cv2.VideoCapture(self.video_source)
        self.update()

    def jump_frames(self, frame_count):
        if self.vid is not None:
            frame_no = int(self.frame_number.get() or 0) + frame_count
            frame_no = max(0, frame_no)  # Avoid negative frame numbers
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            self.update()

    def update(self):
        if self.vid is not None:
            ret, frame = self.vid.read()
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

                # Update frame number
                current_frame = int(self.vid.get(cv2.CAP_PROP_POS_FRAMES))
                self.frame_number.delete(0, tk.END)
                self.frame_number.insert(0, str(current_frame))

    def __del__(self):
        if self.vid is not None:
            self.vid.release()

# Create a window and pass it to the video player
root = tk.Tk()
VideoPlayer(root, "Tkinter and OpenCV")
root.mainloop()
