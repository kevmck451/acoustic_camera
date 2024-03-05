

import pyaudio
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Specify the backend
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import queue


# class Matrix_Mics:
#     def __init__(self):
#
#         self.DEVICE_INDEX = 3 # This is specific to each hardware device -> Run 'check_sound_settings.py'
#
#         # Configuration
#         self.chunk_size = 16384
#         self.audio_dtype = pyaudio.paInt16
#         self.mic_channels = 8
#         self.sample_rate = 48000
#         self.time_domain_peak_threshold = 800
#
#         # Initialize PyAudio
#         self.p = pyaudio.PyAudio()
#
#         # Queue for transferring data from audio callback to main thread
#         self.audio_queue = queue.Queue()
#
#         def callback(in_data, frame_count, time_info, status):
#             self.audio_queue.put(np.frombuffer(in_data, dtype=np.int16))
#             return (None, pyaudio.paContinue)
#
#         self.audio_stream = self.p.open(format=self.audio_dtype,
#                         channels=self.mic_channels,
#                         rate=self.sample_rate,
#                         input=True,
#                         frames_per_buffer=self.chunk_size,
#                         input_device_index=self.DEVICE_INDEX,
#                         stream_callback=callback)
#
#     # Non-linear transformation function
#     def nonlinear_transform(self, data, scale_factor=0.01):
#         # Apply logarithmic transformation with sign preservation and avoid log(0)
#         return np.sign(data) * np.log1p(np.abs(data) * scale_factor)
#
#
#
#     def channel_viewer_figure(self):
#         # Prepare the plots for updating
#         fig, axs = plt.subplots(self.mic_channels, 1, figsize=(10, 5))
#         lines = []
#         for ax in axs:
#             x = np.arange(0, self.chunk_size)
#             y = np.zeros(self.chunk_size)
#             line, = ax.plot(x, y, color='blue')  # Set the default color to blue
#             ax.set_ylim(-5, 5)  # Adjusted for the transformed data range
#             ax.set_yticklabels([])
#             ax.set_xticklabels([])
#             lines.append(line)
#
#         fig.tight_layout(pad=1)
#
#         def update_plot(frame, self):
#
#             if not self.audio_queue.empty():
#                 data = self.audio_queue.get()
#                 for i in range(self.mic_channels):
#                     channel_data = data[i::self.mic_channels]
#                     # Apply the non-linear transformation
#                     transformed_data = self.nonlinear_transform(channel_data)
#                     # Check if any value in channel_data exceeds the threshold
#                     if np.any(np.abs(channel_data) > self.time_domain_peak_threshold):
#                         lines[i].set_color('red')  # Change color to red if threshold is exceeded
#                     else:
#                         lines[i].set_color('blue')  # Reset to default color otherwise
#                     lines[i].set_ydata(transformed_data)
#             return lines
#
#         ani = FuncAnimation(fig, update_plot, blit=True, interval=20, fargs=(self,))
#
#         # Start the stream and show the plot
#         self.audio_stream.start_stream()
#
#         try:
#             plt.show()
#         except KeyboardInterrupt:
#             pass
#
#         # Stop and close the stream
#         self.audio_stream.stop_stream()
#         self.audio_stream.close()
#         self.p.terminate()




# Configuration

class Matrix_Mics:
    def __init__(self):
        CHUNK = 16384
        FORMAT = pyaudio.paInt16
        CHANNELS = 8
        RATE = 48000
        DEVICE_INDEX = 3
        THRESHOLD = 800  # Define your threshold value here

        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Queue for transferring data from audio callback to main thread
        audio_queue = queue.Queue()

        def callback(in_data, frame_count, time_info, status):
            audio_queue.put(np.frombuffer(in_data, dtype=np.int16))
            return (None, pyaudio.paContinue)

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=DEVICE_INDEX,
                        stream_callback=callback)

        # Non-linear transformation function
        def nonlinear_transform(data, scale_factor=0.01):
            # Apply logarithmic transformation with sign preservation and avoid log(0)
            return np.sign(data) * np.log1p(np.abs(data) * scale_factor)

        # Prepare the plots for updating
        fig, axs = plt.subplots(CHANNELS, 1, figsize=(10, 5))
        lines = []
        for ax in axs:
            x = np.arange(0, CHUNK)
            y = np.zeros(CHUNK)
            line, = ax.plot(x, y, color='blue')  # Set the default color to blue
            ax.set_ylim(-5, 5)  # Adjusted for the transformed data range
            ax.set_yticklabels([])
            ax.set_xticklabels([])
            lines.append(line)

        fig.tight_layout(pad=1)

        def update_plot(frame):
            if not audio_queue.empty():
                data = audio_queue.get()
                for i in range(CHANNELS):
                    channel_data = data[i::CHANNELS]
                    # Apply the non-linear transformation
                    transformed_data = nonlinear_transform(channel_data)
                    # Check if any value in channel_data exceeds the threshold
                    if np.any(np.abs(channel_data) > THRESHOLD):
                        lines[i].set_color('red')  # Change color to red if threshold is exceeded
                    else:
                        lines[i].set_color('blue')  # Reset to default color otherwise
                    lines[i].set_ydata(transformed_data)
            return lines

        ani = FuncAnimation(fig, update_plot, blit=True, interval=20)

        # Start the stream and show the plot in a non-blocking manner
        plt.show(block=False)

        stream.start_stream()

        # Main loop to check if the window is open
        try:
            while plt.get_fignums():
                plt.pause(0.1)  # Pause to reduce CPU usage, adjust as necessary
        except KeyboardInterrupt:
            pass
        finally:
            # Cleanup
            stream.stop_stream()
            stream.close()
            p.terminate()