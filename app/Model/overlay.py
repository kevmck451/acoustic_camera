

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
        self.rms_threshold = 20  # 20
        self.rms_max = 90  # 85


        audio_scale_thread = threading.Thread(target=self._generate_audio_view, daemon=True)
        audio_scale_thread.start()

    # THIS FUNCTION WORKS
    def _generate_audio_view(self):
        while self.audio_visual_running:
            rms_values = self.mic_hardware.RMS_values
            self.audio_overlay = self.scale_audio_matrix(rms_values)

            # Normalize the audio_overlay within the specified range
            # Ensure values below threshold are set to the minimum value
            clipped_audio_overlay = np.clip(self.audio_overlay, self.rms_threshold, self.rms_max)
            norm_audio_overlay = np.uint8(255*(clipped_audio_overlay-self.rms_threshold)/(self.rms_max-self.rms_threshold))

            # Apply a colormap to create a heatmap effect
            # Using COLORMAP_HOT to mimic 'Reds' from matplotlib
            self.audio_overlay = cv2.applyColorMap(norm_audio_overlay, cv2.COLORMAP_HOT)

        # For Test Viewing Raw Heat Map
        #     cv2.imshow('Audio Heatmap', heatmap)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        # cv2.destroyAllWindows()


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


    # THIS FUNCTION WORKS
    # def start_overlay(self):
    #     while self.running:
    #         frame = self.camera_hardware.read()
    #         if frame is not None:
    #             frame_resized = cv2.resize(frame, (self.width, self.height))
    #
    #             # Ensure the audio overlay is in the correct format
    #             if len(self.audio_overlay.shape) == 2 or (len(self.audio_overlay.shape) == 3 and self.audio_overlay.shape[2] == 1):
    #                 # If the audio overlay is indeed single-channel, convert it to BGR
    #                 audio_overlay_8bit = cv2.normalize(self.audio_overlay, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    #                 audio_overlay_bgr = cv2.cvtColor(audio_overlay_8bit, cv2.COLOR_GRAY2BGR)
    #             elif len(self.audio_overlay.shape) == 3 and self.audio_overlay.shape[2] == 3:
    #                 # If the overlay is already in BGR format, use it directly
    #                 audio_overlay_bgr = self.audio_overlay
    #             else:
    #                 raise ValueError("Unexpected number of channels in audio_overlay")
    #
    #             # Blend the audio overlay with the video frame
    #             combined_overlay = cv2.addWeighted(frame_resized, 1, audio_overlay_bgr, 0.5, 0)
    #             self.total_overlay = combined_overlay
    #
    #             # Display the result
    #             cv2.imshow('Total Overlay', self.total_overlay)
    #             if cv2.waitKey(1) & 0xFF == ord('q'):
    #                 break
    #
    #     cv2.destroyAllWindows()

    def start_overlay(self):
        while self.running:
            frame = self.camera_hardware.read()
            if frame is not None:
                frame_resized = cv2.resize(frame, (self.width, self.height))

                # Normalize self.audio_overlay to 8-bit if it's not already
                if self.audio_overlay.dtype != np.uint8:
                    audio_overlay_8bit = cv2.normalize(self.audio_overlay, None, 0, 255, cv2.NORM_MINMAX).astype(
                        np.uint8)
                else:
                    audio_overlay_8bit = self.audio_overlay

                # Convert to grayscale for thresholding
                heatmap_gray = cv2.cvtColor(audio_overlay_8bit, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(heatmap_gray, self.rms_threshold, 255, cv2.THRESH_BINARY)
                alpha_channel = np.uint8(mask)  # Use the mask for alpha channel

                # Convert the BGR heatmap to BGRA by adding the alpha channel
                audio_overlay_bgra = cv2.cvtColor(audio_overlay_8bit, cv2.COLOR_BGR2BGRA)
                audio_overlay_bgra[:, :, 3] = alpha_channel

                # Ensure the camera feed is in BGRA for alpha blending
                if frame_resized.shape[2] == 3:
                    frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2BGRA)

                # Blend the audio overlay with the video frame using the alpha channel
                combined_overlay = cv2.add(frame_resized, audio_overlay_bgra)
                self.total_overlay = combined_overlay

                cv2.imshow('Total Overlay', self.total_overlay)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()




    def stop_overlay(self):
        self.running = False
