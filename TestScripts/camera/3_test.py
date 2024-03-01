from picamera2 import Picamera2
import time

# ssh -X username@your_pi_address

def main():
    picam2 = Picamera2()
    # Start the camera preview
    picam2.start_preview(fullscreen=True)  # Set fullscreen to True for better viewing experience
    try:
        while True:
            time.sleep(1)  # Keep the script running until interrupted
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up: Stop the camera preview
        picam2.stop_preview()

if __name__ == "__main__":
    main()