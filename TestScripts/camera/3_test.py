from picamera2 import Picamera2, Preview
from libcamera import Transform

import time

# Messing with parameters
# From ch3 in doc

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
picam2.start_preview(Preview.QTGL, width=400, height=400)

picam2.start()

time.sleep(20)