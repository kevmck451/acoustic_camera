# Acoustic Camera
- Real Time Passive Acoustic Phase Array with Visual Display
- Senior Design Project for the University of Memphis

## 1. Raspberry Pi Setup
#### Links:
- [Raspberry Pi 4 Purchase Page](https://www.amazon.com/dp/B07TC2BK1X?ref=ppx_yo2ov_dt_b_product_details&th=1)
- [SD Card Purchase Page](https://www.amazon.com/dp/B09X7BK27V?ref=ppx_yo2ov_dt_b_product_details&th=1)
- [Screen Purchase Page](https://www.amazon.com/dp/B0CJNKFVPY?ref=ppx_yo2ov_dt_b_product_details&th=1)
- [Keyboard/Mouse Purchase Page](https://www.amazon.com/dp/B07KPVZ1Y4?ref=ppx_yo2ov_dt_b_product_details&th=1)
- [Power Supply Purchase Page](https://www.amazon.com/dp/B097P2NLVH?psc=1&ref=ppx_yo2ov_dt_b_product_details)
- [RaspPi Set Up Guide](https://www.raspberrypi.com/documentation/computers/getting-started.html)

#### Flash SD Card
- Settings
  - set username / password
  - turn ssh on
  - enter WIFI credentials (optional: if using screen, you can do this later)
#### Connect Pi Hardware
- Follow screen instructions for proper connection
#### SSH into Pi
- Open terminal (ctr + alt + t)
- Need IP4 address: Use terminal command ```ifconfig``` Ex: IP4 192.168.0.111 or inet 192.168.0.111
- If you set up a hostname, you can use it instead of the IP address
- Need root user name (should be green): pi is default (pi@raspberrypi:~ $)
- Type this command with your info replaced: ```ssh pi@192.168.0.111```
#### Update everything
- ```sudo apt update```
- ```sudo apt full-upgrade```
- ```sudo apt autoremove```
- ```sudo apt clean```
- ```sudo reboot```

## 2. Project Directory / Github Connection
- My preferred work flow is to program and run files on the pi from my desktop computer as opposed to on the pi directly. 
- If you are doing everything on the pi, then you can skip this step. 
- It's still recommended to create a github repo to back up your work and tracking progress.

#### Create repo in github with markdown file
#### Clone repo to pi and desktop computer
#### Test connection with a commit and push / pull

## 3. Camera Module
#### Links:
- [Camera Purchase Page](https://www.amazon.com/gp/product/B01ER2SKFS/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&th=1)
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


## 4. Microphone Module
#### Links:
- [Product Purchase Page](https://www.newark.com/matrix-labs/matrix-voice-esp/voice-development-board-spartan/dp/55AC2404?gclid=Cj0KCQjwiIOmBhDjARIsAP6YhSVaI4keeU8VfIYhUSqK6x4ST3JNHzf88cvQXWHzEGxW4CGrv8TJlCUaAo5qEALw_wcB&mckv=_dc%7Cpcrid%7C%7Cplid%7C%7Ckword%7C%7Cmatch%7C%7Cslid%7C%7Cproduct%7C55AC2404%7Cpgrid%7C%7Cptaid%7C%7C&CMP=KNC-GUSA-PMAX-Shopping-High-ROAS-S40)
- [Device Overview PDF](https://www.farnell.com/datasheets/2608206.pdf?_ga=2.219371345.993533472.1539793131-901402398.1539269224)
- [ALSA Mic Overview](https://matrix-io.github.io/matrix-documentation/matrix-lite/py-reference/alsa-mics/)
- [MatrixIO Kernal Modules](https://github.com/matrix-io/matrixio-kernel-modules/blob/master/README.md#option-1-package-installation)

#### Following option 1 from MatrixIO Kernal Modules
- Supposedly only works with buster

#### Buster OS
- Link to zip file [Link](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip)
- Used Raspberry Pi imager to image the SD card with this .img file
- Reverting back to current stock Raspbian kernel use:

```zsh
sudo apt-get install --reinstall raspberrypi-bootloader raspberrypi-kernel
sudo apt update
sudo apt-get -y install raspberrypi-kernel-headers raspberrypi-kernel git 
sudo reboot
git clone https://github.com/matrix-io/matrixio-kernel-modules
cd matrixio-kernel-modules/src
make && make install
```
- Output:
~~~
pi@acousticpi:~/matrixio-kernel-modules/src $ make && make install
dtc -W no-unit_address_vs_reg -@ -I dts -O dtb -o matrixio.dtbo matrixio.dts
make -C /lib/modules/5.10.103-v7l+/build M=/home/pi/matrixio-kernel-modules/src modules
make[1]: Entering directory '/usr/src/linux-headers-5.10.103-v7l+'
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-core.o
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-uart.o
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-everloop.o
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-codec.o
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-mic.o
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-playback.o
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-gpio.o
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-env.o
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-imu.o
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-regmap.o
  MODPOST /home/pi/matrixio-kernel-modules/src/Module.symvers
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-codec.mod.o
  LD [M]  /home/pi/matrixio-kernel-modules/src/matrixio-codec.ko
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-core.mod.o
  LD [M]  /home/pi/matrixio-kernel-modules/src/matrixio-core.ko
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-env.mod.o
  LD [M]  /home/pi/matrixio-kernel-modules/src/matrixio-env.ko
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-everloop.mod.o
  LD [M]  /home/pi/matrixio-kernel-modules/src/matrixio-everloop.ko
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-gpio.mod.o
  LD [M]  /home/pi/matrixio-kernel-modules/src/matrixio-gpio.ko
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-imu.mod.o
  LD [M]  /home/pi/matrixio-kernel-modules/src/matrixio-imu.ko
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-mic.mod.o
  LD [M]  /home/pi/matrixio-kernel-modules/src/matrixio-mic.ko
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-playback.mod.o
  LD [M]  /home/pi/matrixio-kernel-modules/src/matrixio-playback.ko
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-regmap.mod.o
  LD [M]  /home/pi/matrixio-kernel-modules/src/matrixio-regmap.ko
  CC [M]  /home/pi/matrixio-kernel-modules/src/matrixio-uart.mod.o
  LD [M]  /home/pi/matrixio-kernel-modules/src/matrixio-uart.ko
make[1]: Leaving directory '/usr/src/linux-headers-5.10.103-v7l+'
make -C /lib/modules/5.10.103-v7l+/build M=/home/pi/matrixio-kernel-modules/src modules_install
make[1]: Entering directory '/usr/src/linux-headers-5.10.103-v7l+'
mkdir: cannot create directory ‘/lib/modules/5.10.103-v7l+/extra’: Permission denied
make[1]: *** [Makefile:1740: _emodinst_] Error 1
make[1]: Leaving directory '/usr/src/linux-headers-5.10.103-v7l+'
make: *** [Makefile:11: install] Error 2
~~~








