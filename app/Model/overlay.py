


import cv2 # pip install opencv-python
import threading
import numpy as np




class Overlay:
    def __init__(self, mics, camera):
        self.mic_hardware = mics
        self.camera_hardware = camera
        self.height, self.width = self.camera_hardware.frame_height, self.camera_hardware.frame_width
        self.overlay = np.zeros((self.height, self.width))
        self.detect_sound_power = False
        self.detect_drones = False
        self.classify_drones = False
        self.detect_vehicles = False
        self.classify_vehicles = False



    def add_overlay(self):


        if self.detect_sound_power:
            RMS_calculations_thread = threading.Thread(target=self.mic_hardware.get_RMS).start()
            self.mic_hardware.RMS_values

        elif self.detect_drones:
            pass
        elif self.classify_drones:
            pass
        elif self.detect_vehicles:
            pass
        elif self.classify_vehicles:
            pass



