


from .microphones import MicArray
from .camera import Camera
from .overlay import Overlay


import threading
import time


if __name__ == "__main__":

    camera_hardware = Camera().start_camera()

    # server on FPGA will need to be running
    mic_hardware = MicArray().start_client_connection()

    video_feed = Overlay(mic_hardware, camera_hardware)

    # video_thread = threading.Thread(target=video_feed.generate_overlay, daemon=True).start()









