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
- reverting back to current stock Raspbian kernel use:

```zsh
sudo apt-get install --reinstall raspberrypi-bootloader raspberrypi-kernel
```

- output is in "ALSA or kernel output.txt" file

#### Add repo and key

```zsh
curl -L https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
```

#### Output:
~~~
pi@acousticpi:~ $ curl -L https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (6) Could not resolve host: apt.matrix.one
Warning: apt-key is deprecated. Manage keyring files in trusted.gpg.d instead (see apt-key(8)).
gpg: no valid OpenPGP data found.
~~~

#### Troubleshooting
- I googled this link from warning: https://apt.matrix.one/doc/apt-key.gpg
- First link was this github site: [Link](https://github.com/matrix-io/matrix-creator-init/issues/57)
- At the bottom, this was said from someone:

~~~
This issues is also adressed here matrix-org/synapse#1855

Their solution is to use another link
curl https://packages.matrix.org/debian/matrix-org-archive-keyring.asc | sudo apt-key add -

But this ends up in
The following signatures couldn't be verified because the public key is not available: NO_PUBKEY B16A1706B2DD19C3

Workaround for this is to open the sources file

sudo nano /etc/apt/sources.list.d/matrixlabs.list
and edit it to:
deb [trusted=yes]  https://apt.matrix.one/raspbian buster main

Another thing worth noting is that
matrixio-creator-init seems to be not availablie on bullseye (neither 32 nor 64 bit), only on buster
~~~

#### Finding Buster OS
- Googled "raspberry pi buster download 4" and found this [Link](https://raspberrypi.stackexchange.com/questions/144742/how-do-i-get-the-latest-version-of-raspberry-pi-os-buster-for-4)
- A link was given to zip file [Link](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip)
- Used Raspberry Pi imager to image the SD card with this .img file
- When I turned on the pi, it said something about file resize and rebooted, then rebooted again and a couple more times
- It finally booted up correctly, settings box popped up, new settings applied with reboot

#### MatrixIO Kernal Module Steps Attempt with Buster OS
- ssh into pi and try kernel install again
- output is in "ALSA or kernel output.txt 2" file
- Changed process from troubleshooting page:
~~~
sudo nano /etc/apt/sources.list.d/matrixlabs.list
~~~
and edit it to:
~~~
deb [trusted=yes]  https://apt.matrix.one/raspbian buster main
~~~
~~~
curl https://packages.matrix.org/debian/matrix-org-archive-keyring.asc | sudo apt-key add -
~~~
- no warning this time, but gpg still says no valid data found; doest that matter?

#### Output:
~~~
pi@acousticpi:~ $ curl https://packages.matrix.org/debian/matrix-org-archive-keyring.asc | sudo apt-key add -
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   146    0   146    0     0    185      0 --:--:-- --:--:-- --:--:--   185
gpg: no valid OpenPGP data found.
~~~
- Update packages and install
~~~
pi@acousticpi:~ $ sudo apt-get update
Err:1 https://apt.matrix.one/raspbian buster InRelease
  Could not resolve 'apt.matrix.one'
Get:2 http://raspbian.raspberrypi.org/raspbian buster InRelease [15.0 kB]          
Get:3 http://archive.raspberrypi.org/debian buster InRelease [32.6 kB]             
Get:4 http://raspbian.raspberrypi.org/raspbian buster/main armhf Packages [13.0 MB]
Get:5 http://archive.raspberrypi.org/debian buster/main armhf Packages [400 kB]
Get:6 http://raspbian.raspberrypi.org/raspbian buster/contrib armhf Packages [58.8 kB]
Get:7 http://raspbian.raspberrypi.org/raspbian buster/non-free armhf Packages [110 kB]
Fetched 13.6 MB in 8s (1,731 kB/s)                                                                                                                   
Reading package lists... Done
N: Ignoring file 'matrixlabs.listcurl' in directory '/etc/apt/sources.list.d/' as it has an invalid filename extension
N: Repository 'http://raspbian.raspberrypi.org/raspbian buster InRelease' changed its 'Suite' value from 'stable' to 'oldoldstable'
N: Repository 'http://archive.raspberrypi.org/debian buster InRelease' changed its 'Suite' value from 'testing' to 'oldoldstable'
W: Failed to fetch https://apt.matrix.one/raspbian/dists/buster/InRelease  Could not resolve 'apt.matrix.one'
W: Some index files failed to download. They have been ignored, or old ones used instead.
~~~
~~~
pi@acousticpi:~ $ sudo apt-get upgrade
Reading package lists... Done
Building dependency tree       
Reading state information... Done
Calculating upgrade... Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 vlc-bin : Depends: libvlc-bin (= 3.0.12-0+deb10u1+rpt1) but 3.0.20-0+deb10u1 is to be installed
 vlc-plugin-base : Depends: vlc-data (= 3.0.12-0+deb10u1+rpt1) but 3.0.20-0+deb10u1 is to be installed
 vlc-plugin-skins2 : Depends: vlc-plugin-qt (= 3.0.20-0+deb10u1) but 3.0.12-0+deb10u1+rpt1 is to be installed
N: Ignoring file 'matrixlabs.listcurl' in directory '/etc/apt/sources.list.d/' as it has an invalid filename extension
E: Broken packages
~~~

#### Trying Option 2
- yeilded the same results










