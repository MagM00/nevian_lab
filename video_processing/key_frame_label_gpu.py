import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import os
import pygame
from pygame.locals import *
import OpenGL.GL as gl
import OpenGL.GLU as glu

class VideoPlayerOpenGL:
    def __init__(self, vid_source):
        self.vid = cv2.VideoCapture(vid_source)
        pygame.init()
        display = (1600, 900)
        self.screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        
        # Generate a single texture
        self.texture = gl.glGenTextures(1)

        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        gl.glClearDepth(1.0)
        gl.glDepthFunc(gl.GL_LESS)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45, display[0] / display[1], 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Bind and update the texture
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, frame.shape[1], frame.shape[0], 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, frame)

            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            gl.glLoadIdentity()
            gl.glBegin(gl.GL_QUADS)
            gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f(-1.0, -1.0, 0.0)
            gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f(1.0, -1.0, 0.0)
            gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f(1.0, 1.0, 0.0)
            gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f(-1.0, 1.0, 0.0)
            gl.glEnd()
            pygame.display.flip()
        else:
            print("Failed to read frame")  # Diagnostic print

class VideoPlayerTkinter:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # Set window to full-screen mode
        self.is_full_screen = True
        self.window.attributes('-fullscreen', self.is_full_screen)

        # Bind the ESC key to the toggle_full_screen method
        self.window.bind('<Escape>', self.toggle_full_screen)
        
        # Canvas for video playback
        self.canvas = tk.Canvas(window, width=1600, height=900)
        self.canvas.pack()

        # Frame number display
        self.frame_number = tk.Entry(window)
        self.frame_number.pack()

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

        self.btn_backward_10 = tk.Button(window, text="Backward 10 frames", command=lambda: self.jump_frames(-10))
        self.btn_backward_10.pack(side=tk.LEFT)

        self.btn_forward_10 = tk.Button(window, text="Forward 10 frames", command=lambda: self.jump_frames(10))
        self.btn_forward_10.pack(side=tk.LEFT)

        self.btn_forward_100 = tk.Button(window, text="Forward 100 frames", command=lambda: self.jump_frames(100))
        self.btn_forward_100.pack(side=tk.LEFT)

        self.btn_forward_900 = tk.Button(window, text="Forward 900 frames", command=lambda: self.jump_frames(900))
        self.btn_forward_900.pack(side=tk.LEFT)

        self.video_source = None
        self.opengl_player = None
        self.thread = None

    def load_video(self):
        self.video_source = filedialog.askopenfilename()
        if self.video_source:
            self.opengl_player = VideoPlayerOpenGL(self.video_source)
            self.update_video()

    def update_video(self):
        if self.opengl_player:
            self.opengl_player.update()
            self.window.after(16, self.update_video)  # Schedule next update, e.g., for 60 fps use 16 ms

    def toggle_full_screen(self, event=None):
        self.is_full_screen = not self.is_full_screen
        self.window.attributes('-fullscreen', self.is_full_screen)
        if not self.is_full_screen:
            self.window.state('zoomed')  # This maximizes the window

    def slider_used(self, event):
        if self.vid:
            frame_no = int(self.slider.get())
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            # You might need to update your OpenGL player here

    def log_event(self):
        if self.vid and self.event_var.get():
            current_frame = int(self.vid.get(cv2.CAP_PROP_POS_FRAMES))
            event_text = [key for key, value in self.event_options.items() if value == self.event_var.get()][0]
            self.log_data.append([event_text, current_frame])
            print(f"Logged Event: {event_text}, Frame: {current_frame}")
            df = pd.DataFrame(self.log_data, columns=['Event', 'Frame'])
            df.to_excel(os.path.splitext(self.video_source)[0] + "_log.xlsx", index=False)

# Tkinter window setup
root = tk.Tk()
player = VideoPlayerTkinter(root, "Tkinter and OpenGL Video Player")
root.mainloop()
