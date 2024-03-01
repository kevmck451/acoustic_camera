# Acoustic Camera
- Real Time Passive Acoustic Phase Array with Visual Display
- Senior Design Project for the University of Memphis

## Camera Module
This is for bookworm OS
#### Links:
- [PiCamera2 Library Documentation](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)

#### First Connection
- New versions of rpi should have camera packages preinstalled
- To test if camera is working, type this command in terminal
- This should bring up a window with camera feed for about 5 seconds
```zsh
rpicam-hello
```
- if using through ssh, then you can type this command before rpicam-hello
```zsh
export DISPLAY=:0
```


#### Install Dependecies
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

## Example Scripts

#### Setup your Virtual Environment
```zsh
# cd into folder
cd acoustic_camera/
# create virtual env with system packages
python3 -m venv --system-site-packages camera_venv
# activate environ
source camera_venv/bin/activate
# add it to your gitignore
nano .gitignore # add camera_venv/ 
```

#### Go through example scripts
```zsh
cd acoustic_camera/TestScripts/camera/
```
1_test.py: works
- got this message 
  - ```QStandardPaths: wrong permissions on runtime directory /run/user/1000, 0770 instead of 0700```
  - this stopped it:
  - ```chmod 0700 /run/user/1000```








