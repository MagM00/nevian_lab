import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import tkinter as tk
from tkinter import filedialog
import os

# Initialize Tkinter root
root = tk.Tk()
root.withdraw()  # Hide the main window

# Ask the user to provide a video path
video_path = filedialog.askopenfilename(title='Select a Video File', filetypes=[('Video Files', '*.mp4 *.avi *.mkv *.flv'), ('All Files', '*.*')])

if not video_path:
    print('User selected Cancel')
    exit()

do_green = 1

# Display the first frame of the video
video_obj = cv2.VideoCapture(video_path)

ret, first_frame = video_obj.read()
if not ret:
    print("Failed to read the video")
    exit()

# Function to handle rectangle selection
def line_select_callback(eclick, erelease):
    global rect
    rect = [int(eclick.xdata), int(eclick.ydata), int(erelease.xdata - eclick.xdata), int(erelease.ydata - eclick.ydata)]

# Make figure and axes
fig, ax = plt.subplots()
plt.imshow(cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB))
toggle_selector = RectangleSelector(ax, line_select_callback,
                                    drawtype='box', useblit=True,
                                    button=[1],  # Left mouse button
                                    minspanx=5, minspany=5,
                                    spancoords='pixels',
                                    interactive=True)
plt.title('Select a rectangle to crop the video')
plt.show()

# Validate rectangle
if rect[2] <= 0 or rect[3] <= 0:
    print('Invalid rectangle selected')
    exit()

# Ask user for a prefix
prefix = input('Enter the animal_ID you just cropped; or left and right: ')

# Select where to save the cropped video
cropped_pathname = os.path.join(os.path.dirname(video_path), 'cropped')
if not os.path.exists(cropped_pathname):
    os.makedirs(cropped_pathname)

# Prepare output video path
if do_green:
    output_video_path = os.path.join(cropped_pathname, f'{prefix}_cropped_{os.path.basename(video_path)}')
else:
    output_video_path = os.path.join(cropped_pathname, f'{prefix}_cropped_RGB_{os.path.basename(video_path)}')

# Prepare output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_fps = video_obj.get(cv2.CAP_PROP_FPS)
output_video = cv2.VideoWriter(output_video_path, fourcc, out_fps, (rect[2] // 4, rect[3] // 4))

print(f'Cropping video: {os.path.basename(video_path)}...')

# Process video
while video_obj.isOpened():
    ret, frame = video_obj.read()
    if not ret:
        break

    # Apply green filter if needed
    if do_green:
        frame[:, :, 0] = 0  # Zero out the blue channel
        frame[:, :, 2] = 0  # Zero out the red channel

    # Crop and resize
    cropped_frame = frame[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    resized_frame = cv2.resize(cropped_frame, (rect[2] // 4, rect[3] // 4))

    output_video.write(resized_frame)

# Release everything
video_obj.release()
output_video.release()

print(f'Cropped video saved as: {output_video_path}')
