from picamera2 import Picamera2, Preview

import time

# Messing with QtGL preview window
# From ch3 in doc

'''
This preview window is implemented using the Qt GUI toolkit and 
uses GLES hardware graphics acceleration. 
It is the most efficient way to display images on the screen 
when using the GUI environment and we would recommend it in
nearly all circumstances when a GUI is required. 
The QtGL preview window can be started with:
'''
picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
time.sleep(10)


picam2 = Picamera2()
picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600, transform=Transform(hflip=1, vflip=1))
picam2.start()
'''
The QtGL preview window is not recommended when the image needs 
to be shown on a remote display (not connected to the Pi)
'''