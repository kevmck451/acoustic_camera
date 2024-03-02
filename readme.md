# Acoustic Camera
- Real Time Passive Acoustic Phase Array with Visual Display
- Senior Design Project for the University of Memphis
## Hardware
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

## Raspberry Pi Setup
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



## ---------------------------------------------------------
## Camera Module
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







## 3. Project Directory / Github Connection
- My preferred work flow is to program and run files on the pi from my desktop computer as opposed to on the pi directly. 
- If you are doing everything on the pi, then you can skip this step. 
- It's still recommended to create a github repo to back up your work and tracking progress.
- clone repo to pi and desktop computer
```zsh
git clone https://github.com/kevmck451/acoustic_camera
```