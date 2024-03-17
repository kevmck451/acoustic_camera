import pyaudio

# Instantiate PyAudio
p = pyaudio.PyAudio()

# List all available devices and their info
def list_devices():
    print("Available devices:\n")
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print(f"Device {i}: {dev['name']} (Input Channels: {dev['maxInputChannels']})")

# Use this function to list devices
list_devices()

# Now, assuming you've identified the device index you want to use
# For example, to use the device with index 2 for recording
device_index = 2  # Replace with the correct device index for your sound card

# Open a stream with the specific device
stream = p.open(format=pyaudio.paInt16,
                channels=8,  # Assuming you want to use all 8 channels
                rate=44100,
                input=True,
                input_device_index=3,  # Use MATRIXIO-SOUND device
                frames_per_buffer=1024)

# Do something with the stream (e.g., record audio)
# ...

# Close the stream when done
stream.stop_stream()
stream.close()

# Terminate the PyAudio session
p.terminate()
