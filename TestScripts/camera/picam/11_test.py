import picamera
import time
import numpy as np

# Create an array representing a 1280x720 image of
# a cross through the center of the display.
a = np.zeros((720, 1280, 3), dtype=np.uint8)
a[360, :, :] = 0xff
a[:, 640, :] = 0xff

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)  # Adjust the camera resolution to match the overlay
    camera.rotation = 90
    camera.zoom = (0.0, 0.0, 1.0, 1.0)
    camera.start_preview()

    # Add the overlay with the specified format and size
    o = camera.add_overlay(a.tobytes(), size=(1280, 720), layer=3, alpha=64, format='rgb')
    try:
        # Wait indefinitely until the user terminates the script
        while True:
            time.sleep(1)
    finally:
        camera.remove_overlay(o)
