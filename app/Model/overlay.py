


import cv2 # pip install opencv-python
import threading
import numpy as np
import cv2 # pip install opencv-python # This will take really long time



# class Overlay:
#     def __init__(self, mics, camera):
#         self.mic_hardware = mics
#         self.camera_hardware = camera
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
#         RMS_calculations_thread = threading.Thread(target=self.mic_hardware.get_RMS).start()
#         audio_overlay = self.scale_audio_matrix(self.mic_hardware.RMS_values)
#         # self.overlay =
#
#
#
#     def stop_overlay(self):
#         self.running = False








class Overlay:
    def __init__(self, camera, mic_array):
        self.camera = camera
        self.mic_array = mic_array
        self.audio_visualizer = AudioVisualizer()

    def update(self):
        while True:
            video_frame = self.camera.get_latest_frame()
            audio_data = self.mic_array.get_latest_audio_data()

            if video_frame is not None and audio_data is not None:
                # Generate the audio visualization
                audio_overlay = self.audio_visualizer.visualize(audio_data)

                # Combine the video frame with the audio visualization
                # Assuming the sizes are compatible or resized accordingly
                combined_frame = self.combine_frames(video_frame, audio_overlay)

                # Display the combined frame
                cv2.imshow('Overlay', combined_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    @staticmethod
    def combine_frames(video_frame, audio_overlay):
        # This is a simplified example; actual combination depends on how you want to overlay
        # For instance, you might want to overlay the audio visualization at the bottom of the video frame
        height, width, _ = video_frame.shape
        overlay_height, overlay_width, _ = audio_overlay.shape

        combined_frame = video_frame.copy()
        combined_frame[height - overlay_height:, :overlay_width, :] = audio_overlay
        return combined_frame

