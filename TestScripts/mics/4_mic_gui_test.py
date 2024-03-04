import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
import threading
import pyaudio
import queue

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize PyAudio
p = pyaudio.PyAudio()

# Queue for audio data
audio_queue = queue.Queue()


def audio_callback(in_data, frame_count, time_info, status):
    audio_queue.put(np.frombuffer(in_data, dtype=np.int16))
    return (None, pyaudio.paContinue)


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=audio_callback)


def plot_audio():
    # Assuming you have a mechanism to get your audio data
    # For demonstration, let's plot 1 second of audio data
    frames = []
    for _ in range(0, int(RATE / CHUNK)):
        data = audio_queue.get()
        frames.append(data)

    audio_data = np.hstack(frames)

    plt.figure()
    plt.plot(audio_data)
    plt.title("Audio Signal")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.show()


# CustomTkinter setup
app = ctk.CTk()
app.geometry("400x200")


def on_plot_button_click():
    # Plot audio in a separate thread to prevent GUI from freezing
    threading.Thread(target=plot_audio, daemon=True).start()


plot_button = ctk.CTkButton(app, text="Plot Audio Signal", command=on_plot_button_click)
plot_button.pack(pady=20)

# Start the audio stream
stream.start_stream()

# Run the customTkinter application
app.mainloop()

# Cleanup on exit
stream.stop_stream()
stream.close()
p.terminate()
