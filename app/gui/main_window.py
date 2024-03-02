import tkinter as tk
from PIL import Image, ImageTk
from picamera import PiCamera
from io import BytesIO
import time

# Set up the GUI window using Tkinter
root = tk.Tk()
label = tk.Label(root)
label.pack()

# Initialize the camera
camera = PiCamera()
camera.rotation = 90
camera.resolution = (640, 480)

def update_camera_feed():
    stream = BytesIO()
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    image = Image.open(stream)
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo
    root.after(5, update_camera_feed)  # Update the feed every 100 milliseconds

update_camera_feed()  # Start the camera feed
root.mainloop()  # Start the GUI event loop
