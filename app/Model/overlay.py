

import threading
import numpy as np
import time
import cv2



class Overlay:
    def __init__(self, pi_hardware):
        self.mic_hardware = pi_hardware.mic_hardware
        self.camera_hardware = pi_hardware.camera_hardware
        self.height, self.width = self.camera_hardware.height, self.camera_hardware.width
        self.audio_overlay = np.zeros((self.height, self.width))
        self.total_overlay = np.zeros((self.height, self.width))
        self.total_overlay_compressed = None
        self.save_video = False
        self.stream_video = False
        self.detect_sound_power = False
        self.detect_drones = False
        self.classify_drones = False
        self.detect_vehicles = False
        self.classify_vehicles = False
        self.audio_visual_running = True
        self.running = True
        self.rms_threshold = np.log(20)  # 20
        self.rms_max = np.log(85)  # 85
        self.audio_overlay_color = 2
        self.compression_rate = 20  # Max 100


        # audio_scale_thread = threading.Thread(target=self.view_audio_heatmap, daemon=True)
        # audio_scale_thread.start()
        audio_scale_thread = threading.Thread(target=self._generate_audio_view, daemon=True)
        audio_scale_thread.start()

        # if wanting to view overlay uncomment this and comment out above
        # overlay_thread = threading.Thread(target=self.view_overlay, daemon=True)
        # overlay_thread.start()

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


    def view_audio_heatmap(self):
        while self.audio_visual_running:
            rms_values = self.mic_hardware.RMS_values
            scaled_audio_values = self.scale_audio_matrix(rms_values)  # Process the RMS values

            # Normalize the scaled audio values within the specified range
            clipped_audio_overlay = np.clip(scaled_audio_values, self.rms_threshold, self.rms_max)
            norm_audio_overlay = np.uint8(
                255 * (clipped_audio_overlay - self.rms_threshold) / (self.rms_max - self.rms_threshold))

            # Create an RGB image where the red channel intensity is based on audio level
            # In OpenCV, the channel order is BGR, so the red channel is the last one
            self.audio_overlay = np.zeros((norm_audio_overlay.shape[0], norm_audio_overlay.shape[1], 3), dtype=np.uint8)
            self.audio_overlay[:, :, 2] = norm_audio_overlay  # Set the red channel in BGR order

            # For Test Viewing Red Channel Intensity Map
            # cv2.imshow('Audio Intensity Map', self.audio_overlay)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        # cv2.destroyAllWindows()


    def _generate_audio_view(self):
        while self.audio_visual_running:
            rms_values = self.mic_hardware.RMS_values
            scaled_audio_values = self.scale_audio_matrix(rms_values)  # Process the RMS values

            # Normalize the scaled audio values within the specified range
            clipped_audio_overlay = np.clip(np.log(scaled_audio_values), self.rms_threshold, self.rms_max)
            norm_audio_overlay = np.uint8(
                255 * (clipped_audio_overlay - self.rms_threshold) / (self.rms_max - self.rms_threshold))

            # Create an RGB image where the red channel intensity is based on audio level
            # In OpenCV, the channel order is BGR, so the red channel is the last one
            self.audio_overlay = np.zeros((norm_audio_overlay.shape[0], norm_audio_overlay.shape[1], 3), dtype=np.uint8)
            self.audio_overlay[:, :, self.audio_overlay_color] = norm_audio_overlay  # Set the red channel in BGR order

            # For Test Viewing Red Channel Intensity Map
        #     cv2.imshow('Audio Intensity Map', self.audio_overlay)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        #
        # cv2.destroyAllWindows()


    def view_overlay(self):
        while self.running:
            frame = self.camera_hardware.read()
            if frame is not None and self.audio_overlay is not None:
                if frame.shape == self.audio_overlay.shape:

                    # Blend the audio overlay with the video frame
                    combined_overlay = cv2.addWeighted(frame, 1, self.audio_overlay, 0.5, 0)
                    self.total_overlay = combined_overlay

                    # Display the result
                    cv2.imshow('Total Overlay', self.total_overlay)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        cv2.destroyAllWindows()


    def start_overlay(self):
        while self.running:
            frame = self.camera_hardware.read()
            if frame is not None and self.audio_overlay is not None:
                if frame.shape == self.audio_overlay.shape:

                    # Blend the audio overlay with the video frame
                    combined_overlay = cv2.addWeighted(frame, 1, self.audio_overlay, 0.5, 0)
                    self.total_overlay = combined_overlay
                    # print(self.total_overlay.shape)
                    # Calculate the number of bytes: 921600 bytes
                    # num_bytes = self.total_overlay.nbytes
                    # print(num_bytes)

                    # Compress the combined overlay to a JPEG format in memory

                    result, self.total_overlay_compressed = cv2.imencode('.jpg', self.total_overlay,
                                                                         [int(cv2.IMWRITE_JPEG_QUALITY), self.compression_rate])

                    # num_bytes = self.total_overlay_compressed.nbytes
                    # print(num_bytes)
                    # print(self.total_overlay_compressed)


    def stop_overlay(self):
        self.running = False


    def get_data(self):
        """
        Get the compressed video data for network transmission.

        Returns:
            bytes: The compressed video data.
        """
        # Ensure the video data is ready for transmission
        if self.total_overlay_compressed is not None:
            # Return the data as a bytes object
            return self.total_overlay_compressed.tobytes()
        else:
            return b''





