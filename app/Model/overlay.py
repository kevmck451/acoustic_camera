import cv2
import numpy as np


class Overlay:
    def __init__(self, pi_hardware, color_map='jet'):
        """
        Initializes the overlay with the Raspberry Pi hardware components.

        :param pi_hardware: An instance of PiHardware which contains the microphone array and camera
        :param color_map: String representing the color map to use for visualizing sound intensities
        """
        self.pi_hardware = pi_hardware
        self.color_map = color_map
        self.image_size = (self.pi_hardware.camera_hardware.width, self.pi_hardware.camera_hardware.height)
        self.overlay_image = np.zeros((self.image_size[1], self.image_size[0], 3), dtype=np.uint8)

    def create_intensity_map(self):
        """
        Creates an intensity map based on the RMS values from the microphone array.
        """
        # Get RMS values from the microphone array
        rms_values = self.pi_hardware.mic_hardware.RMS_values
        intensity_map = np.zeros(self.image_size, dtype=np.uint8)

        # Normalize and map the RMS values to the intensity map
        norm_rms_values = np.interp(rms_values, (rms_values.min(), rms_values.max()), (0, 255))
        for i in range(norm_rms_values.shape[0]):
            for j in range(norm_rms_values.shape[1]):
                intensity = norm_rms_values[i, j]
                cv2.circle(intensity_map, (j * 40, i * 40), 20, int(intensity), -1)

        intensity_map_colored = cv2.applyColorMap(intensity_map, getattr(cv2, self.color_map.upper()))
        return intensity_map_colored

    def update_overlay(self, intensity_map):
        """
        Updates the overlay image based on the provided intensity map.

        :param intensity_map: An intensity map as a NumPy array
        """
        self.overlay_image = cv2.addWeighted(self.overlay_image, 0.5, intensity_map, 0.5, 0)

    def display_overlay(self):
        """
        Displays the overlay on top of the current camera frame.
        """
        background_image = self.pi_hardware.camera_hardware.read()
        combined_image = cv2.addWeighted(background_image, 0.8, self.overlay_image, 0.2, 0)
        cv2.imshow("Overlay", combined_image)
        cv2.waitKey(1)  # Display the frame for a short moment

    def run(self):
        """
        Main method to run the overlay process.
        """
        while True:
            intensity_map = self.create_intensity_map()
            self.update_overlay(intensity_map)
            self.display_overlay()











# ORIGINAL ROUGH DRAFT

# import cv2 # pip install opencv-python
# import threading
# import numpy as np
# import cv2 # pip install opencv-python # This will take really long time
#
#
# class Overlay:
#     def __init__(self, pi_hardware):
#         self.mic_hardware = pi_hardware.mic_hardware
#         self.camera_hardware = pi_hardware.camera_hardware
#         self.height, self.width = self.camera_hardware.frame_height, self.camera_hardware.frame_width
#         self.overlay = np.zeros((self.height, self.width))
#         self.detect_sound_power = False
#         self.detect_drones = False
#         self.classify_drones = False
#         self.detect_vehicles = False
#         self.classify_vehicles = False
#         self.running = True
#
#
#
#     def scale_audio_matrix(self, original_matrix):
#         scaling_factor = self.height // self.mic_hardware.map_row
#         scaled_matrix = []
#
#         for row in original_matrix:
#             new_row = []
#             for element in row:
#                 # Create a block of size scaling_factor x scaling_factor
#                 # where all elements are 'element' from the original matrix
#                 block = [[element] * scaling_factor for _ in range(scaling_factor)]
#                 new_row.extend(block)
#             scaled_matrix.extend(new_row)
#
#         return scaled_matrix
#
#     def generate_overlay(self):
#
#         pass
#
#
#
#     def stop_overlay(self):
#         self.running = False
