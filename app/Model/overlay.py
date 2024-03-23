

# ORIGINAL ROUGH DRAFT

import cv2 # pip install opencv-python
import threading
import numpy as np
import cv2 # pip install opencv-python # This will take really long time


class Overlay:
    def __init__(self, pi_hardware):
        self.mic_hardware = pi_hardware.mic_hardware
        self.camera_hardware = pi_hardware.camera_hardware
        self.height, self.width = self.camera_hardware.height, self.camera_hardware.width
        self.audio_overlay = np.zeros((self.height, self.width))
        self.total_overlay = np.zeros((self.height, self.width))
        self.detect_sound_power = False
        self.detect_drones = False
        self.classify_drones = False
        self.detect_vehicles = False
        self.classify_vehicles = False
        self.audio_visual_running = True
        self.running = True


        audio_scale_thread = threading.Thread(target=self._generate_audio_view, daemon=True)
        audio_scale_thread.start()


    # def _generate_audio_view(self):
    #     while self.audio_visual_running:
    #         print(self.mic_hardware.RMS_values)
    #         print(self.mic_hardware.RMS_values.shape)
    #         self.audio_overlay = self.scale_audio_matrix(self.mic_hardware.RMS_values)
    #         print(self.audio_overlay)
    #         print(self.audio_overlay.shape)
    #         cv2.imshow('Frame Display', self.audio_overlay)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #     cv2.destroyAllWindows()

    def _generate_audio_view(self):
        while self.audio_visual_running:
            print(self.mic_hardware.RMS_values)
            print(self.mic_hardware.RMS_values.shape)
            self.audio_overlay = self.scale_audio_matrix(self.mic_hardware.RMS_values)

            # Normalize the audio_overlay for display purposes
            norm_audio_overlay = cv2.normalize(self.audio_overlay, None, 0, 255, cv2.NORM_MINMAX)
            norm_audio_overlay = norm_audio_overlay.astype(np.uint8)

            # Apply a colormap to create a heatmap effect similar to matplotlib
            heatmap = cv2.applyColorMap(norm_audio_overlay, cv2.COLORMAP_JET)

            print(self.audio_overlay)
            print(self.audio_overlay.shape)
            cv2.imshow('Frame Display', heatmap)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def scale_audio_matrix(self, original_matrix):
        # Determine the scaling factors for rows and columns
        # Ensure that the entire height and width are covered by rounding up
        scaling_factor_row = int(np.ceil(self.height / original_matrix.shape[0]))
        scaling_factor_col = int(np.ceil(self.width / original_matrix.shape[1]))

        # Use np.kron to expand the matrix in both dimensions
        # Create a matrix of ones of size (scaling_factor_row, scaling_factor_col)
        # This matrix will act as the template for repeating elements of the original matrix
        repeater_matrix = np.ones((scaling_factor_row, scaling_factor_col))

        # The Kronecker product will repeat elements of the original matrix
        # by the structure of the repeater_matrix
        scaled_matrix = np.kron(original_matrix, repeater_matrix)

        # If the scaled matrix is larger than the desired size, trim the excess
        scaled_matrix = scaled_matrix[:self.height, :self.width]

        return scaled_matrix


    def start_overlay(self):

        while self.running:
            print('-'*80)

            # Current Camera Frame
            frame = self.camera_hardware.read()
            print(f'Frame Shape: {frame.shape}')

            # Current Mic Frame

            if frame is not None:
                # do something to frame
                pass









    def stop_overlay(self):
        self.running = False
