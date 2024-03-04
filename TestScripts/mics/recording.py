import pyaudio
import wave
import sounddevice

# recording configs
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 8
RATE = 48000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output4.wav"

# create & configure microphone
mic = pyaudio.PyAudio()

stream = mic.open(format=pyaudio.paInt16,
                channels=CHANNELS,  # Assuming you want to use all 8 channels
                rate=RATE,
                input=True,
                input_device_index=3,  # Use MATRIXIO-SOUND device
                frames_per_buffer=CHUNK)


print("* recording")
print('Should see something other than x00')
# read & store microphone data per frame read
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    # print(data)
    frames.append(data)
print(frames[0][:64])
print("* done recording")

# kill the mic and recording
stream.stop_stream()
stream.close()
mic.terminate()

# combine & store all microphone data to output.wav file
outputFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
outputFile.setnchannels(CHANNELS)
outputFile.setsampwidth(mic.get_sample_size(FORMAT))
outputFile.setframerate(RATE)
outputFile.writeframes(b''.join(frames))
outputFile.close()
