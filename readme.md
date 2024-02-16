# Acoustic Camera

Senior Design Project
University of Memphis


## 1. Camera Module
https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

### First Connection
- New versions of rpi should have camera packages preinstalled
- To test if camera is working, type this command in terminal
- This should bring up a window with camera feed for about 5 seconds
```zsh
rpicam-hello
```
### Install Dependecies
- Install OpenCV
- OpenCV (Open Source Computer Vision Library) is a library of programming functions mainly aimed at real-time computer vision
```zsh
sudo apt install -y python3-opencv
sudo apt install -y opencv-data
```
- Install FFmpeg
- FFmpeg is a powerful multimedia framework capable of decoding, encoding, transcode, mux, demux, stream, filter, and play almost anything that humans and machines have created
- It's widely used for video and audio processing tasks, including format conversion, compression, streaming, and more
```zsh
sudo apt install -y ffmpeg
```


## 2. Microphone Module
Device Overview: 
https://www.farnell.com/datasheets/2608206.pdf?_ga=2.219371345.993533472.1539793131-901402398.1539269224

ALSA Mic Overview: https://matrix-io.github.io/matrix-documentation/matrix-lite/py-reference/alsa-mics/

MatrixIO Kernal Modules: https://github.com/matrix-io/matrixio-kernel-modules/blob/master/README.md#option-1-package-installation






