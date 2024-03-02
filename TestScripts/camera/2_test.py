from picamera2 import Picamera2

# Save an Video

picam2 = Picamera2()
picam2.start_and_record_video("test.mp4", duration=5)