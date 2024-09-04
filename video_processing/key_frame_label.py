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

        logo_path = r'M:/Jun/software/logo.ico'
        logo_image = Image.open(logo_path)
        photo = ImageTk.PhotoImage(logo_image)
        self.window.iconphoto(False, photo)

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
        self.log_view = ttk.Treeview(self.log_frame, columns=("Index", "Event", "Frame", "Response"), show="headings")
        self.log_view.column("Index", width=40, anchor=tk.CENTER)
        self.log_view.column("Event", anchor=tk.CENTER)
        self.log_view.column("Frame", anchor=tk.CENTER)
        self.log_view.column("Response", width=60, anchor=tk.CENTER)
        self.log_view.heading("Index", text="Index")
        self.log_view.heading("Event", text="Event")
        self.log_view.heading("Frame", text="Frame")
        self.log_view.heading("Response", text="Response")
        self.log_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind double-click event to jump to frame
        self.log_view.bind("<Double-1>", self.jump_to_logged_frame)

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
        self.slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, length=1900, resolution=1, command=self.slider_used)
        self.slider.pack(fill=tk.X)

        # Event controls frame
        self.event_control_frame = tk.Frame(window)
        self.event_control_frame.pack()

        # Dropdown Menu for Event Selection (下拉菜单)
        self.event_var = tk.StringVar()
        self.event_options = {
            "0: Pinprick": "0",
            "1: 0.07g-Green": "1",
            "2: 0.4g-Dark blue": "2",
            "3: 2g-Purple": "3",
            "4: Cold water": "4",
            "5: Room temp": "5",
            "6: Hot water": "6"
        }
        self.event_dropdown = ttk.Combobox(self.event_control_frame, textvariable=self.event_var)
        self.event_dropdown['values'] = list(self.event_options.keys())
        self.event_dropdown.pack(side=tk.LEFT)

        # Log button
        self.btn_log = tk.Button(self.event_control_frame, text="📝 Log Event", command=self.log_event)
        self.btn_log.pack(side=tk.LEFT)
        
        # Modify Event button
        self.btn_modify = tk.Button(self.event_control_frame, text="Modify Event", command=self.modify_event)
        self.btn_modify.pack(side=tk.LEFT)

        # Delete Event button
        self.btn_delete = tk.Button(self.event_control_frame, text="Delete Event", command=self.delete_event)
        self.btn_delete.pack(side=tk.LEFT)

        # Move Event Up button
        self.btn_move_up = tk.Button(self.event_control_frame, text="Move Event Up", command=lambda: self.move_event(-1))
        self.btn_move_up.pack(side=tk.LEFT)

        # Move Event Down button
        self.btn_move_down = tk.Button(self.event_control_frame, text="Move Event Down", command=lambda: self.move_event(1))
        self.btn_move_down.pack(side=tk.LEFT)

        # Response checkbox
        self.response_var = tk.BooleanVar()
        self.response_checkbox = tk.Checkbutton(self.event_control_frame, text="Response", variable=self.response_var)
        self.response_checkbox.pack(side=tk.LEFT)

        # Bind Move Event Up and Move Event Down keys to corresponding methods
        self.window.bind("<Up>", lambda event: self.move_event(-1))
        self.window.bind("<Down>", lambda event: self.move_event(1))

        # Sync Button
        self.btn_sync = tk.Button(self.event_control_frame, text="Sync and Save Events", command=self.sync_events)
        self.btn_sync.pack(side=tk.LEFT)

        # Load Button
        self.btn_load_events = tk.Button(self.event_control_frame, text="Load Unfinished Events", command=self.load_events)
        self.btn_load_events.pack(side=tk.LEFT)

        # Load video button
        self.btn_load = tk.Button(self.event_control_frame, text="Load Video", command=self.load_video)
        self.btn_load.pack(side=tk.LEFT)

        # Frame navigation buttons frame
        self.frame_nav_buttons_frame = tk.Frame(window)
        self.frame_nav_buttons_frame.pack(fill=tk.X)  # This will allow the frame to expand to fill the width

        # Call to create navigation buttons
        self.create_frame_navigation_buttons(self.frame_nav_buttons_frame)

        self.video_source = None
        self.vid = None
        self.log_data = []
        
        # Initial and maximum frame skip values
        self.initial_frame_skip = 30
        self.max_frame_skip = 60
        self.current_frame_skip = self.initial_frame_skip

        # Timing variable to increase frame skip speed
        self.key_press_time = 0

        # Bind left and right key events
        self.window.bind('<Left>', self.on_left_arrow_press)
        self.window.bind('<Right>', self.on_right_arrow_press)
        self.window.bind('<KeyRelease-Left>', self.on_key_release)
        self.window.bind('<KeyRelease-Right>', self.on_key_release)

    def on_left_arrow_press(self, event):
        # Handle continuous press and speed adjustment
        self.adjust_frame_skip()
        self.jump_frames(-self.current_frame_skip)

    def on_right_arrow_press(self, event):
        # Handle continuous press and speed adjustment
        self.adjust_frame_skip()
        self.jump_frames(self.current_frame_skip)

    def on_key_release(self, event):
        # Reset frame skip to initial value and reset timer
        self.current_frame_skip = self.initial_frame_skip
        self.key_press_time = 0

    def adjust_frame_skip(self):
        # Example logic to increase frame skip speed based on time or consecutive presses
        self.key_press_time += 1  # Increase time or counter
        if self.key_press_time >= 5:  # If key is pressed continuously, adjust frame skip
            self.current_frame_skip = min(self.current_frame_skip + 5, self.max_frame_skip)

    def create_frame_navigation_buttons(self, frame):
        # Place frame navigation buttons centered
        navigation_buttons = ["   ⏪   1800   ", "   ⏪   900   ", "   ⏪   300   ", "   ⏪   100   ",
                              "   ⏪   50   ", "   ⏪   30   ", "   ⏪   10   ", "   ⏪   5   ", "   ⏪   1   ",
                              "   ⏩   1   ", "   ⏩   5   ", "   ⏩   10   ", "   ⏩   30   ", "   ⏩   50   ",
                              "   ⏩   100   ", "   ⏩   300   ", "   ⏩   900   ", "   ⏩   1800   "]
        frame_steps = [-1800, -900, -300, -100, -50, -30, -10, -5, -1, 1, 5, 10, 30, 50, 100, 300, 900, 1800]

        inner_frame = tk.Frame(frame)  # Create an inner frame to hold buttons
        inner_frame.pack(anchor='center')  # Pack the inner frame centered

        for text, step in zip(navigation_buttons, frame_steps):
            btn = tk.Button(inner_frame, text=text, command=lambda s=step: self.jump_frames(s))
            btn.pack(side=tk.LEFT)

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
            event_text = self.event_var.get()
            if event_text in self.event_options:
                event_index = len(self.log_data) + 1
                response = 1 if self.response_var.get() else 0
                self.log_data.append([event_index, event_text, current_frame, response])
                print(f"Logged Event: {event_text}, Frame: {current_frame}, Response: {response}")
                
                new_entry = self.log_view.insert('', 'end', values=(event_index, event_text, current_frame, response))
                
                self.log_view.see(new_entry)
                
                df = pd.DataFrame(self.log_data, columns=['Index', 'Event', 'Frame', 'Response'])
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

    def jump_to_logged_frame(self, event):
        item = self.log_view.selection()[0]
        values = self.log_view.item(item, "values")
        frame_no = int(values[2])
        event_text = values[1]
        response = int(values[3])

        # Update frame number
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        self.slider.set(frame_no)
        self.update_frame_number(frame_no)

        # Update event type
        self.event_var.set(event_text)

        # Update response state
        self.response_var.set(bool(response))

        self.update()

    def modify_event(self):
        selected_item = self.log_view.selection()
        if selected_item:
            new_event = self.event_var.get()
            if new_event:
                index = self.log_view.index(selected_item)
                current_frame = self.log_data[index][2]
                response = 1 if self.response_var.get() else 0
                self.log_data[index] = [index+1, new_event, current_frame, response]
                self.log_view.item(selected_item, values=(index+1, new_event, current_frame, response))

    def delete_event(self):
        selected_item = self.log_view.selection()
        if selected_item:
            index = self.log_view.index(selected_item)
            del self.log_data[index]  # Delete from log data
            self.log_view.delete(selected_item)  # Delete from Treeview

    def move_event(self, direction):
        selected_item = self.log_view.selection()
        if selected_item:
            index = self.log_view.index(selected_item)
            if 0 <= index + direction < len(self.log_data):
                self.log_data[index], self.log_data[index + direction] = self.log_data[index + direction], self.log_data[index]
                for i in [index, index + direction]:
                    self.log_view.delete(self.log_view.get_children()[i])
                    self.log_view.insert('', i, values=self.log_data[i])

    def sync_events(self):
        df = pd.DataFrame(self.log_data, columns=['Index', 'Event', 'Frame', 'Response'])
        df.to_excel(os.path.splitext(self.video_source)[0] + "_log.xlsx", index=False)

    def load_events(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.read_excel(file_path)
            self.log_data = df.values.tolist()
            for i in self.log_view.get_children():
                self.log_view.delete(i)
            for log in self.log_data:
                self.log_view.insert('', 'end', values=log)

# Create a window and pass it to the video player
root = tk.Tk()
VideoPlayer(root, "Key frame logger ©Jun Huang")
root.mainloop()