


from .microphones import MicArray
from .camera import Camera
from .overlay import Overlay


import threading
import time


if __name__ == "__main__":
    mic_hardware = MicArray().start_client_connection()
    camera_hardware = Camera()

    video_feed = Overlay(mic_hardware, camera_hardware)







