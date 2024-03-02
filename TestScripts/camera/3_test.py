from picamera2 import Picamera2, Preview
from libcamera import Transform

import time

# Messing with parameters
# From ch3 in doc

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600,
transform=Transform(hflip=1, vflip=1))
picam2.start()

time.sleep(20)