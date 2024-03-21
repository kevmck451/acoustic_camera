


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
        self.running = True



    def scale_audio_matrix(self, original_matrix):
        scaling_factor = self.height // self.mic_hardware.map_row
        scaled_matrix = []

        for row in original_matrix:
            new_row = []
            for element in row:
                # Create a block of size scaling_factor x scaling_factor
                # where all elements are 'element' from the original matrix
                block = [[element] * scaling_factor for _ in range(scaling_factor)]
                new_row.extend(block)
            scaled_matrix.extend(new_row)

        return scaled_matrix

    def generate_overlay(self):

        RMS_calculations_thread = threading.Thread(target=self.mic_hardware.get_RMS).start()
        audio_overlay = self.scale_audio_matrix(self.mic_hardware.RMS_values)
        # self.overlay =



    def stop_overlay(self):
        self.running = False


