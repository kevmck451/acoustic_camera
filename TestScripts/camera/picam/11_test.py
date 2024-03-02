import picamera
import time
import numpy as np

# Create an array representing a 1280x720 image of
# a cross through the center of the display.
a = np.zeros((720, 1280, 3), dtype=np.uint8)
a[360, :, :] = 0xff
a[:, 640, :] = 0xff

# Desired center point for zoom (as a fraction of the width and height)
center_x, center_y = 0.25, 0.5
# Zoom level (2x zoom in this example)
zoom_level = 2

# Calculate width and height of the zoom area
zoom_width = 1 / zoom_level
zoom_height = 1 / zoom_level

# Calculate top-left corner of the zoom area
x = center_x - (zoom_width / 2)
y = center_y - (zoom_height / 2)

screen_width_size = 1920
screen_height_size = 1080

with picamera.PiCamera() as camera:
    camera.rotation = 90
    camera.resolution = (screen_width_size, screen_height_size)
    camera.zoom = (x, y, zoom_width, zoom_height)
    camera.start_preview()

    # Add the overlay with the specified format and size
    o = camera.add_overlay(a.tobytes(), size=(screen_width_size, screen_height_size), layer=3, alpha=64, format='rgb')
    try:
        # Wait indefinitely until the user terminates the script
        while True:
            time.sleep(1)
    finally:
        camera.remove_overlay(o)
