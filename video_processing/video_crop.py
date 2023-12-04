# © Jun Huang 2023.12.04
# video cropping tool for Magdalena and Kristina's mice social behavior (fiber photometry recording) videos
import cv2
import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Load video button
        self.load_button = tk.Button(window, text="Load Video", command=self.load_video)
        self.load_button.pack()

        # Label for video frames
        self.video_label = tk.Label(window)
        self.video_label.pack()

        # Slider for video frames
        self.slider = tk.Scale(window, from_=0, to=100, orient="horizontal", command=self.show_frame)
        self.slider.pack()

        # Coordinate display
        self.coordinates_label = tk.Label(window, text="X,Y Coordinates:")
        self.coordinates_label.pack()

        # Input for cropping coordinates
        self.y1_label = tk.Label(window, text="Y1:")
        self.y1_label.pack()
        self.y1_entry = tk.Entry(window)
        self.y1_entry.insert(0, "40")  # Default value for y1
        self.y1_entry.pack()

        self.y2_label = tk.Label(window, text="Y2:")
        self.y2_label.pack()
        self.y2_entry = tk.Entry(window)
        self.y2_entry.insert(0, "360")  # Default value for y2
        self.y2_entry.pack()

        # Button for cropping
        self.crop_button = tk.Button(window, text="Crop Video", command=self.crop_video)
        self.crop_button.pack()

        self.window.mainloop()

    def load_video(self):
        self.video_path = filedialog.askopenfilename()
        self.cap = cv2.VideoCapture(self.video_path)
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.slider.configure(to=self.length)

    def show_frame(self, value):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(value))
        ret, frame = self.cap.read()
        if ret:
            cv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
            self.video_label.configure(image=self.photo)
            self.video_label.bind('<Button-1>', self.get_coordinates)

    def get_coordinates(self, event):
        self.coordinates_label.configure(text=f"X,Y Coordinates: {event.x}, {event.y}")

    def crop_video(self):
        y1 = int(self.y1_entry.get())
        y2 = int(self.y2_entry.get())

        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        # Create subfolder if it doesn't exist
        video_dir = os.path.dirname(self.video_path)
        output_dir = os.path.join(video_dir, 'cropped_videos')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Construct output file path
        video_filename = os.path.basename(self.video_path)
        video_name, _ = os.path.splitext(video_filename)
        output_path = os.path.join(output_dir, f"{video_name}_cropped.mp4")

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, y2-y1))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cropped_frame = frame[y1:y2, :]
            out.write(cropped_frame)

        cap.release()
        out.release()
        print(f"Video cropped and saved as '{output_path}'")

if __name__ == "__main__":
    root = tk.Tk()
    VideoPlayer(root, "Video Player")
