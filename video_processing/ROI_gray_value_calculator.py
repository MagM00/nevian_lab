import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import time

class VideoFrameGrabber:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame Grabber")
        self.vid = None
        self.frame = None
        self.total_frames = 0
        self.current_frame = 0
        self.roi_start = None
        self.roi_end = None
        self.roi_values = []

        # Canvas for video, initialized with default size.
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        # Frame slider
        self.slider = tk.Scale(root, from_=0, to=1, orient='horizontal', length=500, command=self.get_frame)
        self.slider.pack(fill='x')

        # Buttons
        self.btn_load = tk.Button(root, text="Load Video", command=self.load_video)
        self.btn_load.pack(fill='x')

        self.btn_label_roi = tk.Button(root, text="Label ROI", command=self.label_roi)
        self.btn_label_roi.pack(fill='x')

        # Call update function to start the loop for video frame reading
        self.update()

    def load_video(self):
        self.filename = filedialog.askopenfilename(title="Select a video file", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
        self.basename_without_ext = os.path.splitext(os.path.basename(self.filename))[0]
        self.vid = cv2.VideoCapture(self.filename)
        self.total_frames = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        self.slider.config(to=self.total_frames)
        self.get_frame(0)

        width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        canvas_width = 800
        canvas_height = 600
        self.canvas.config(width=canvas_width, height=canvas_height, scrollregion=(0, 0, width, height))
        x_scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        x_scrollbar.pack(fill=tk.X)
        x_scrollbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=x_scrollbar.set)
        y_scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        y_scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=y_scrollbar.set)

    def label_roi(self):
        if self.frame is not None:
            self.roi_start = None
            self.roi_end = None
            self.roi_values = []
            self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
            self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        else:
            messagebox.showwarning("Warning", "No frame to label. Please load a video.")

    def on_mouse_press(self, event):
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        self.roi_start = (canvas_x, canvas_y)

    def on_mouse_drag(self, event):
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        self.roi_end = (canvas_x, canvas_y)
        self.draw_roi()

    def on_mouse_release(self, event):
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        self.roi_end = (canvas_x, canvas_y)
        self.draw_roi()
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.calculate_average_red_value()

    def calculate_average_gray_value(self):
        if self.vid is not None and self.roi_start is not None and self.roi_end is not None:
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.vid.read()
            frame_count = 0
            start_time = time.time()
            while ret:
                # Convert to grayscale
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                roi_gray = gray_frame[int(self.roi_start[1]):int(self.roi_end[1]), int(self.roi_start[0]):int(self.roi_end[0])]
                avg_gray = np.mean(roi_gray)
                self.roi_values.append(avg_gray)
                ret, frame = self.vid.read()
                frame_count += 1
                if frame_count % 10000 == 0:
                    elapsed_time = time.time() - start_time
                    print(f"Time spent: {elapsed_time:.2f} sec | Current Frame: {frame_count} / {self.total_frames}")
            frame_numbers = np.arange(frame_count)
            plt.plot(frame_numbers, self.roi_values)
            plt.xlabel('Frame Number')
            plt.ylabel('Average Gray Value')
            plt.title(f"{self.basename_without_ext} ROI Average Gray Value over Time")
            plt.show()
            data_array = np.array(self.roi_values)
            save_path = f"{self.basename_without_ext}_gray_event.npy"
            np.save(save_path, data_array)

    def draw_roi(self):
        self.canvas.delete("roi_rectangle")
        if self.roi_start is not None and self.roi_end is not None:
            self.canvas.create_rectangle(self.roi_start[0], self.roi_start[1], self.roi_end[0], self.roi_end[1],
                                         outline="green", width=2, tags="roi_rectangle")
            self.canvas.update_idletasks()

    def get_frame(self, current_frame):
        self.current_frame = int(current_frame)
        if self.vid is not None:
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
            _, self.frame = self.vid.read()
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def update(self):
        self.slider.set(self.current_frame)
        self.root.after(1, self.update)

root = tk.Tk()
app = VideoFrameGrabber(root)
root.mainloop()
