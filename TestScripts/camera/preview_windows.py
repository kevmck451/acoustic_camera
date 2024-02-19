from picamera2 import Picamera2, Preview
from libcamera import Transform
import numpy as np


# Example 1

'''
All the parameters are optional, and default values will be chosen if omitted. The following example will place an
800x600 pixel preview window at (100, 200) on the display, and will horizontally mirror the camera preview image:
'''
picam2 = Picamera2()
picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600, transform=Transform(hflip=1))
picam2.start()

'''
The supported transforms are:
• Transform() - the identity transform, which is the default
• Transform(hflip=1) - horizontal flip
• Transform(vflip=1) - vertical flip
• Transform(hflip=1, vflip=1) - horizontal and vertical flip (equivalent to a 180 degree rotation)

It’s important to realise that the display transform discussed here does not have any effect on the actual images received from the camera. 
It only applies the requested transform as it renders the pixels onto the screen. 

'''

'''
Chapter 8: Advance Topics - Display Overlays
'''


picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start(show_preview=True)

overlay = np.zeros((300, 400, 4), dtype=np.uint8) overlay[:150, 200:] = (255, 0, 0, 64)

overlay[145:155, 195:205] = (255, 0, 0, 64) # reddish


picam2.set_overlay(overlay)


