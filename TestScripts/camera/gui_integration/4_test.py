import tkinter as tk
from PIL import Image, ImageTk
from picamera import PiCamera
from io import BytesIO
import threading
import queue
import customtkinter as ctk  # Import customtkinter

frame_queue = queue.Queue(maxsize=1)

def capture_frames():
    with PiCamera() as camera:
        # camera.rotation = 90
        camera.resolution = (640, 480)
        stream = BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            if not frame_queue.full():
                frame_queue.put(stream.read())
            stream.seek(0)
            stream.truncate()

def update_gui():
    try:
        frame_data = frame_queue.get_nowait()
        image = Image.open(BytesIO(frame_data))
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
    except queue.Empty:
        pass
    root.after(1, update_gui)

ctk.set_appearance_mode("System")  # Set the theme
ctk.set_default_color_theme("blue")  # Set the color theme
root = ctk.CTk()  # Initialize the main window with customtkinter
label = tk.Label(root)  # Continue using Tkinter Label for the image
label.pack()

threading.Thread(target=capture_frames, daemon=True).start()
update_gui()

root.mainloop()
