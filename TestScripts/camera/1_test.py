from picamera2 import Picamera2, Preview
from libcamera import Transform

'''
All the parameters are optional, and default values will be chosen if omitted. The following example will place an
800x600 pixel preview window at (100, 200) on the display, and will horizontally mirror the camera preview image:
'''
# picam2 = Picamera2()
# picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600, transform=Transform(hflip=1))
# picam2.start()


picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)