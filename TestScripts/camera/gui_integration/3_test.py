import tkinter as tk
from PIL import Image, ImageTk
from picamera import PiCamera
from io import BytesIO

# Initialize the GUI window
root = tk.Tk()
root.attributes('-fullscreen', True)  # Start in full-screen mode

# Function to ensure the title is set correctly
def set_title():
    root.title("Camera Feed")

# Function to toggle full-screen with F11 or exit with Esc
def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))
    set_title()  # Ensure the title is correct after toggling
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)
    set_title()  # Ensure the title is correct after exiting full-screen

# Bind the toggle function to F11 and exit to Esc
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', exit_fullscreen)

# Adjust label to fill the window
label = tk.Label(root)
label.pack(expand=True, fill=tk.BOTH)

# Initialize the camera
camera = PiCamera()
# camera.rotation = 90
camera.resolution = (1280, 720)  # Set a default resolution
camera.framerate = 24

def update_camera_feed():
    stream = BytesIO()
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    image = Image.open(stream)
    # Automatically resize to fill the screen
    image = image.resize((root.winfo_width(), root.winfo_height()), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo
    root.after(40, update_camera_feed)  # Update the feed roughly every 40 milliseconds (~25 fps)

# Set the window title
set_title()

update_camera_feed()  # Start the camera feed
root.mainloop()  # Start the GUI event loop
