import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk, ImageEnhance
import os

def select_video_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv *.flv"), ("All files", "*.*")])
    if not file_path:
        print("No file selected.")
        exit()
    return file_path

def get_rectangle(frame):
    root = tk.Tk()
    root.geometry("+{}+{}".format(100, 100))  # Position the window
    canvas = tk.Canvas(root, width=frame.shape[1], height=frame.shape[0])
    canvas.pack()

    # Convert the OpenCV frame (BGR) to a Tkinter image
    cv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv_img)
    photo = ImageTk.PhotoImage(image=pil_img)

    # Keep a reference to the image to prevent garbage collection
    canvas.image = photo
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    def on_drag(event):
        canvas.coords(rectangle, x0, y0, event.x, event.y)

    def on_press(event):
        global x0, y0
        x0, y0 = event.x, event.y
        global rectangle
        rectangle = canvas.create_rectangle(x0, y0, x0, y0, outline='red')

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)

    def on_release(event):
        root.quit()

    canvas.bind("<ButtonRelease-1>", on_release)
    root.mainloop()
    return canvas.coords(rectangle)


def adjust_brightness_contrast(image, brightness=0, contrast=0):
    buf = cv2.addWeighted(image, contrast, image, 0, brightness)
    return buf

def main():
    video_path = select_video_file()
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Failed to read video")
        cap.release()
        return

    # Display the first frame and let the user select a rectangle
    rect = get_rectangle(frame)
    x, y, w, h = map(int, rect)

    # Ask user for prefix
    prefix = simpledialog.askstring("Input", "Enter the animal_ID you just cropped; or left and right:")

    # Cropping and saving the video
    dirname = os.path.dirname(video_path)
    output_path = os.path.join(dirname, f"cropped_{prefix}_{os.path.basename(video_path)}")
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), (w//4, h//4))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = adjust_brightness_contrast(frame, brightness=30, contrast=1.5)  # Adjust according to your needs
        cropped = frame[y:y+h, x:x+w]
        resized = cv2.resize(cropped, (w//4, h//4))  # Decrease resolution by 4
        out.write(resized)

    cap.release()
    out.release()
    print(f"Cropped video saved as: {output_path}")

if __name__ == "__main__":
    main()
