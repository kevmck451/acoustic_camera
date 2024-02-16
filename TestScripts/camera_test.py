from picamera import PiCamera
from time import sleep

# Initialize the camera
camera = PiCamera()

# Optionally, set camera resolution. The default is 1920x1080.
# camera.resolution = (1024, 768)

# Optionally, set a preview window. This is useful if you're working with a display.
# camera.start_preview()

# Sleep for a bit to allow the camera to adjust to lighting conditions
sleep(2)

# Capture an image
camera.capture('/home/pi/Desktop/image.jpg')

# Optionally, stop the preview if you started one.
# camera.stop_preview()
