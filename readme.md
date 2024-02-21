# Acoustic Camera
- Real Time Passive Acoustic Phase Array with Visual Display
- Senior Design Project for the University of Memphis
## 1. Hardware
#### Links:
- [Raspberry Pi 4 Purchase Page](https://www.amazon.com/dp/B07TC2BK1X?ref=ppx_yo2ov_dt_b_product_details&th=1)
- [SD Card Purchase Page](https://www.amazon.com/dp/B09X7BK27V?ref=ppx_yo2ov_dt_b_product_details&th=1)
- [Screen Purchase Page](https://www.amazon.com/dp/B0CJNKFVPY?ref=ppx_yo2ov_dt_b_product_details&th=1)
- [Keyboard/Mouse Purchase Page](https://www.amazon.com/dp/B07KPVZ1Y4?ref=ppx_yo2ov_dt_b_product_details&th=1)
- [Power Supply Purchase Page](https://www.amazon.com/dp/B097P2NLVH?psc=1&ref=ppx_yo2ov_dt_b_product_details)
- [Matrix Voice Mic Module](https://www.newark.com/matrix-labs/matrix-voice-esp/voice-development-board-spartan/dp/55AC2404?gclid=Cj0KCQjwiIOmBhDjARIsAP6YhSVaI4keeU8VfIYhUSqK6x4ST3JNHzf88cvQXWHzEGxW4CGrv8TJlCUaAo5qEALw_wcB&mckv=_dc%7Cpcrid%7C%7Cplid%7C%7Ckword%7C%7Cmatch%7C%7Cslid%7C%7Cproduct%7C55AC2404%7Cpgrid%7C%7Cptaid%7C%7C&CMP=KNC-GUSA-PMAX-Shopping-High-ROAS-S40)
- [Pi Camera V2](https://www.amazon.com/gp/product/B01ER2SKFS/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&th=1)

#### Connect Pi Hardware
- Follow screen instructions for proper connection

## 2. Raspberry Pi Setup
- [RaspPi Set Up Guide](https://www.raspberrypi.com/documentation/computers/getting-started.html)

#### Flash SD Card
- Matrix Voice only works with Buster OS
- Link to img zip file [Link](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip)
- Used Raspberry Pi imager to image the SD card with this .img file
- Settings
  - set username / password
  - turn ssh on
  - enter WIFI credentials (optional: if using screen, you can do this later)

#### Set Up
- Go through on screen instructions
- Change Interface Settings
  - Home Icon / Preferences / Raspberry Pi Configuration
    - Enable everything
- Reboot as needed

#### SSH into Pi
- Open terminal on pi (ctr + alt + t)
```zsh
# Need IP4 address
ifconfig
# Look for IP4 192.168.0.111 or inet 192.168.0.111
#If you set up a hostname, you can use it instead of the IP address

# Need root user name (should be green): pi is default
pi@raspberrypi:~ $
# Type this command with your info replaced: 
ssh pi@192.168.0.111
# if using hostname
# ssh pi@hostname.local
# ssh-keygen -f "/Users/KevMcK/.ssh/known_hosts" -R "192.168.0.147"

# Update everything
sudo apt update
sudo apt full-upgrade
sudo apt autoremove
sudo apt clean
sudo reboot
````





## -----------------------------------------------------------
## 5. Microphone Module
#### Links:
- 
- [Device Overview PDF](https://www.farnell.com/datasheets/2608206.pdf?_ga=2.219371345.993533472.1539793131-901402398.1539269224)
- [ALSA Mic Overview](https://matrix-io.github.io/matrix-documentation/matrix-lite/py-reference/alsa-mics/)
- [MatrixIO Kernal Modules](https://github.com/matrix-io/matrixio-kernel-modules/blob/master/README.md#option-1-package-installation)

#### Following option 2 from MatrixIO Kernel Modules
- Supposedly only works with buster
- This drivers only works with current stock raspbian kernel
- To reverting back to current stock Raspbian kernel use:
```zsh
sudo apt-get install --reinstall raspberrypi-bootloader raspberrypi-kernel
````
- Following basic steps from MatrixIO Kernel Module 
```zsh
curl https://s3.amazonaws.com/apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://s3.amazonaws.com/apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
sudo apt-get update
sudo apt-get upgrade
sudo apt install matrixio-kernel-modules
sudo reboot
git clone https://github.com/matrix-io/matrixio-kernel-modules
cd matrixio-kernel-modules/src
make && sudo make install
sudo nano /boot/config.txt
```
- scroll to the bottom and comment out current dtoverlay and change:
~~~
dtoverlay=matrixio
~~~
```zsh
sudo cp ~/matrixio-kernel-modules/misc/matrixio.conf /etc/modules-load.d/
sudo cp ~/matrixio-kernel-modules/misc/asound.conf /etc/
sudo reboot

sudo voice_esp32_enable
# Reset Matrix Voice to confirm operation. LED lights should turn off
esptool.py --chip esp32 --port /dev/ttyS0 --baud 115200 --before default_reset --after hard_reset erase_flash

```

#### Following Alsa Mic Overview
```zsh
sudo apt install portaudio19-dev 
sudo python3 -m pip install pyaudio
```
- Playback wont be needed but setting adjusted anyway
```zsh
sudo nano /etc/asound.conf
```
- rate 16000 added to file





## -----------------------------------------------------------
## 4. Camera Module
#### Links:
- [PiCamera2 Library Documentation](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)

#### First Connection
- New versions of rpi should have camera packages preinstalled
- To test if camera is working, type this command in terminal
- This should bring up a window with camera feed for about 5 seconds
```zsh
rpicam-hello
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







## 3. Project Directory / Github Connection
- My preferred work flow is to program and run files on the pi from my desktop computer as opposed to on the pi directly. 
- If you are doing everything on the pi, then you can skip this step. 
- It's still recommended to create a github repo to back up your work and tracking progress.
- clone repo to pi and desktop computer
```zsh
git clone https://github.com/kevmck451/acoustic_camera
```