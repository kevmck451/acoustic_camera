import tkinter as tk
from PIL import Image, ImageTk
from picamera import PiCamera
from io import BytesIO

# Initialize the GUI window
root = tk.Tk()
root.title("Camera Feed")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the size for the video feed (maintaining the aspect ratio)
video_width = 1280
video_height = 720
if screen_width < video_width or screen_height < video_height:
    # Resize to fit the screen while maintaining the aspect ratio
    aspect_ratio = video_height / video_width
    video_width = min(video_width, screen_width)
    video_height = int(video_width * aspect_ratio)

label = tk.Label(root)
label.pack()

# Initialize the camera
camera = PiCamera()
camera.rotation = 90
camera.resolution = (video_width, video_height)
camera.framerate = 24

def update_camera_feed():
    stream = BytesIO()
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    image = Image.open(stream)
    image = image.resize((video_width, video_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo
    root.after(40, update_camera_feed)  # Update the feed roughly every 40 milliseconds (~25 fps)

update_camera_feed()  # Start the camera feed
root.mainloop()  # Start the GUI event loop
