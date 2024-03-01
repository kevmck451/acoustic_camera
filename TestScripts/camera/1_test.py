from picamera2 import Picamera2, Preview
from libcamera import Transform

'''
All the parameters are optional, and default values will be chosen if omitted. The following example will place an
800x600 pixel preview window at (100, 200) on the display, and will horizontally mirror the camera preview image:
'''
# picam2 = Picamera2()
# picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600, transform=Transform(hflip=1))
# picam2.start()


# picam2 = Picamera2()
# picam2.start_preview(Preview.QTGL)

import cv2

# Initialize the video capture object at video source 0 (default camera)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        # Display the resulting frame
        cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
