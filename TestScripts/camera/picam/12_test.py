import picamera

camera = picamera.PiCamera()
# Turn the camera's LED off
camera.led = True
# Take a picture while the LED remains off
camera.capture('foo3.jpg')