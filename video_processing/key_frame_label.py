import tkinter as tk
from tkinter import filedialog
import cv2
import pandas as pd
from PIL import Image, ImageTk
import os
from tkinter import filedialog, ttk  # ttk is imported for Treeview

class VideoPlayer:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Set window to full-screen mode
        self.is_full_screen = True
        self.window.attributes('-fullscreen', self.is_full_screen)

        # Bind the ESC key to the toggle_full_screen method
        self.window.bind('<Escape>', self.toggle_full_screen)

        # Bind mouse click event on the main window
        self.window.bind("<Button-1>", self.on_window_click)

        # Main frame to hold the video and log side by side
        self.main_frame = tk.Frame(window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame for the Treeview
        self.log_frame = tk.Frame(self.main_frame)
        self.log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Treeview for displaying log data
        self.log_view = ttk.Treeview(self.log_frame, columns=("Index", "Event", "Frame"), show="headings")
        self.log_view.column("Index", width=40, anchor=tk.CENTER)
        self.log_view.column("Event", anchor=tk.CENTER)
        self.log_view.column("Frame", anchor=tk.CENTER)
        self.log_view.heading("Index", text="Index")
        self.log_view.heading("Event", text="Event")
        self.log_view.heading("Frame", text="Frame")
        self.log_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adding vertical scrollbar for the Treeview
        self.tree_scroll = tk.Scrollbar(self.log_frame, orient="vertical", command=self.log_view.yview)
        self.tree_scroll.pack(side='right', fill='y')

        # Configure the Treeview to use the scrollbar
        self.log_view.configure(yscrollcommand=self.tree_scroll.set)

        # Canvas for video playback
        self.canvas = tk.Canvas(self.main_frame, width=1600, height=900)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frame number display
        self.frame_number = tk.Entry(window)
        self.frame_number.pack()

        # Bind Enter key in the frame number entry to jump_to_frame method
        self.frame_number.bind("<Return>", self.jump_to_frame)

        # Jump to frame button
        self.btn_jump = tk.Button(window, text="Jump to Frame", command=self.jump_to_frame)
        self.btn_jump.pack()

        # Slider for frame navigation
        self.slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, length=1900, command=self.slider_used)
        self.slider.pack(fill=tk.X)

        # Event selection using radio buttons
        self.event_var = tk.StringVar()
        self.event_options = {
            "0: Pinprick": "0",
            "1: 0.07g": "1",
            "2: 0.4g": "2",
            "3: 2g": "3",
            "4: Cold water": "4",
            "5: Room temp": "5",
            "6: Hot water": "6"
        }
        self.radio_frame = tk.Frame(window)
        self.radio_frame.pack()
        for (text, value) in self.event_options.items():
            tk.Radiobutton(self.radio_frame, text=text, variable=self.event_var, value=value).pack(side=tk.LEFT)

        # Log button
        self.btn_log = tk.Button(window, text="Log Event", command=self.log_event)
        self.btn_log.pack()

        # Load video button
        self.btn_load = tk.Button(window, text="Load Video", command=self.load_video)
        self.btn_load.pack()

        # Frame navigation buttons

        self.btn_backward_900 = tk.Button(window, text="Backward 900 frames", command=lambda: self.jump_frames(-900))
        self.btn_backward_900.pack(side=tk.LEFT)

        self.btn_backward_100 = tk.Button(window, text="Backward 100 frames", command=lambda: self.jump_frames(-100))
        self.btn_backward_100.pack(side=tk.LEFT)

        self.btn_backward_50 = tk.Button(window, text="Backward 50 frames", command=lambda: self.jump_frames(-50))
        self.btn_backward_50.pack(side=tk.LEFT)

        self.btn_backward_10 = tk.Button(window, text="Backward 10 frames", command=lambda: self.jump_frames(-10))
        self.btn_backward_10.pack(side=tk.LEFT)

        self.btn_backward_1 = tk.Button(window, text="Backward 1 frames", command=lambda: self.jump_frames(-1))
        self.btn_backward_1.pack(side=tk.LEFT)

        self.btn_forward_1 = tk.Button(window, text="Forward 1 frames", command=lambda: self.jump_frames(1))
        self.btn_forward_1.pack(side=tk.LEFT)

        self.btn_forward_10 = tk.Button(window, text="Forward 10 frames", command=lambda: self.jump_frames(10))
        self.btn_forward_10.pack(side=tk.LEFT)

        self.btn_forward_50 = tk.Button(window, text="Forward 50 frames", command=lambda: self.jump_frames(50))
        self.btn_forward_50.pack(side=tk.LEFT)

        self.btn_forward_100 = tk.Button(window, text="Forward 100 frames", command=lambda: self.jump_frames(100))
        self.btn_forward_100.pack(side=tk.LEFT)

        self.btn_forward_900 = tk.Button(window, text="Forward 900 frames", command=lambda: self.jump_frames(900))
        self.btn_forward_900.pack(side=tk.LEFT)

        self.video_source = None
        self.vid = None
        self.log_data = []

    def load_video(self):
        self.video_source = filedialog.askopenfilename()
        if self.video_source:
            self.vid = cv2.VideoCapture(self.video_source)
            total_frames = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
            self.slider.configure(to=total_frames - 1)
            self.update()

    def slider_used(self, event):
        if self.vid:
            frame_no = int(self.slider.get())
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            self.update_frame_number(frame_no)
            self.update()

    def jump_frames(self, frame_count):
        if self.vid:
            frame_no = int(self.frame_number.get() or 0) + frame_count
            frame_no = max(0, min(frame_no, self.vid.get(cv2.CAP_PROP_FRAME_COUNT) - 1))
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            self.slider.set(frame_no)
            self.update_frame_number(frame_no)
            self.update()

    def log_event(self):
        if self.vid and self.event_var.get():
            current_frame = int(self.vid.get(cv2.CAP_PROP_POS_FRAMES))
            event_text = [key for key, value in self.event_options.items() if value == self.event_var.get()][0]
            event_index = len(self.log_data) + 1  # Index for the new event
            self.log_data.append([event_index, event_text, current_frame])
            print(f"Logged Event: {event_text}, Frame: {current_frame}")
            
            # Insert log data into Treeview with index
            new_entry = self.log_view.insert('', 'end', values=(event_index, event_text, current_frame))
            
            # Ensure the new entry is visible
            self.log_view.see(new_entry)
            
            df = pd.DataFrame(self.log_data, columns=['Index', 'Event', 'Frame'])
            df.to_excel(os.path.splitext(self.video_source)[0] + "_log.xlsx", index=False)

    def update_frame_number(self, frame_no):
        self.frame_number.delete(0, tk.END)
        self.frame_number.insert(0, str(frame_no))

    def update(self):
        if self.vid:
            ret, frame = self.vid.read()
            if ret:
                frame = self.resize_frame(frame, 1600, 900)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def resize_frame(self, frame, width, height):
        (h, w) = frame.shape[:2]
        r = width / float(w)
        dim = (width, int(h * r))
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        return cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    def __del__(self):
        if self.vid:
            self.vid.release()
    
    def toggle_full_screen(self, event=None):
        self.is_full_screen = not self.is_full_screen
        self.window.attributes('-fullscreen', self.is_full_screen)
        if not self.is_full_screen:
            self.window.state('zoomed')  # This maximizes the window

    def on_window_click(self, event):
        """Handle mouse click events on the window to remove focus from Entry widget."""
        # Check if the click is outside the Entry widget
        if event.widget != self.frame_number:
            self.window.focus_set()

    def jump_to_frame(self, event=None):
        # event parameter added to handle the Enter key event
        if self.vid:
            frame_no = int(self.frame_number.get())
            frame_no = max(0, min(frame_no, self.vid.get(cv2.CAP_PROP_FRAME_COUNT) - 1))
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            self.slider.set(frame_no)
            self.update()
            self.window.focus_set()

# Create a window and pass it to the video player
root = tk.Tk()
VideoPlayer(root, "Tkinter and OpenCV with Event Logger")
root.mainloop()
