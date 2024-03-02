from picamera2 import Picamera2

# Save an Video
# From ch2 in doc

picam2 = Picamera2()
picam2.start_and_record_video("test.mp4", duration=5)