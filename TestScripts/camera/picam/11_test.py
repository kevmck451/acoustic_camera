import picamera
import time
import numpy as np

# Create an array representing a 1280x720 image of
# a cross through the center of the display. The shape of
# the array must be of the form (height, width, color)
a = np.zeros((720, 1280, 3), dtype=np.uint8)
a[360, :, :] = 0xff
a[:, 640, :] = 0xff

with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)  # Set the resolution as needed
    # Set a smaller ROI (zoom out)
    # x, y, w, h values should be between 0.0 and 1.0
    # This example sets the ROI to the full sensor area, adjust as needed
    camera.zoom = (0.0, 0.0, 1.0, 1.0)
    camera.start_preview()
    # Camera is now set to use the full sensor area
    # Adjust the zoom tuple as needed to simulate zooming out

    o = camera.add_overlay(a.tobytes(), layer=3, alpha=64)
    try:
        # Wait indefinitely until the user terminates the script
        while True:
            time.sleep(1)
    finally:
        camera.remove_overlay(o)