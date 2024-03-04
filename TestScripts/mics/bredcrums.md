# Bread Crumbs for Matrix Voice Access to Microphones

## 4. Microphone Module
#### Links:
- [Product Purchase Page](https://www.newark.com/matrix-labs/matrix-voice-esp/voice-development-board-spartan/dp/55AC2404?gclid=Cj0KCQjwiIOmBhDjARIsAP6YhSVaI4keeU8VfIYhUSqK6x4ST3JNHzf88cvQXWHzEGxW4CGrv8TJlCUaAo5qEALw_wcB&mckv=_dc%7Cpcrid%7C%7Cplid%7C%7Ckword%7C%7Cmatch%7C%7Cslid%7C%7Cproduct%7C55AC2404%7Cpgrid%7C%7Cptaid%7C%7C&CMP=KNC-GUSA-PMAX-Shopping-High-ROAS-S40)
- [Device Overview PDF](https://www.farnell.com/datasheets/2608206.pdf?_ga=2.219371345.993533472.1539793131-901402398.1539269224)
- [ALSA Mic Overview](https://matrix-io.github.io/matrix-documentation/matrix-lite/py-reference/alsa-mics/)
- [MatrixIO Kernal Modules](https://github.com/matrix-io/matrixio-kernel-modules/blob/master/README.md#option-1-package-installation)

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
~~~

### Following option 1 from MatrixIO Kernel Modules
- Supposedly only works with buster


- Following steps from MatrixIO Kernel Modules

```zsh
sudo apt-get install --reinstall raspberrypi-bootloader raspberrypi-kernel
sudo apt update
sudo apt-get -y install raspberrypi-kernel-headers raspberrypi-kernel git 
sudo reboot
git clone https://github.com/matrix-io/matrixio-kernel-modules
cd matrixio-kernel-modules/src
make
sudo make install # <------------------
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


### Following option 2 from MatrixIO Kernel Modules !!!!!!!!!!!!!

##### Troubleshooting APT Repository and GPG Key Addition Option 1
- Found this [link] and at the bottom he said:
~~~
All the websites referencing the voice pi setup (matrix, hackster) 
point to an outdated repository which, confusingly, still has 
the key but an expired one. Here, for anyone reading this thread, 
is the correct way to install the matrix software and prepare it 
for flashing your satellite project.
~~~
```zsh
curl https://s3.amazonaws.com/apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://s3.amazonaws.com/apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
sudo apt-get update
sudo apt-get upgrade
sudo reboot
sudo apt install matrixio-kernel-modules
```
- Ouput:
~~~
Unpacking matrixio-kernel-modules (0.2.5) ...
dpkg: error processing archive /tmp/apt-dpkg-install-kNojMo/13-matrixio-kernel-modules_0.2.5_all.deb (--unpack):
 unable to make backup link of './boot/overlays/matrixio.dtbo' before installing new version: Operation not permitted
Errors were encountered while processing:
 /tmp/apt-dpkg-install-kNojMo/13-matrixio-kernel-modules_0.2.5_all.deb
E: Sub-process /usr/bin/dpkg returned an error code (1)
~~~
- backup .dtbo file
```zsh
sudo cp /boot/overlays/matrixio.dtbo /home/pi/Desktop/
```
- remove .dtbo file thats causing issues
```zsh
sudo rm /boot/overlays/matrixio.dtbo
```
- try install again
```zsh
sudo apt install matrixio-kernel-modules
```
- appears to have worked
```zsh
sudo reboot
sudo apt install matrixio-creator-init
```
- check if modules are installed
```zsh
lsmod | grep matrix
```
- If modules present, then continue. If not, good luck
```zsh
sudo reboot
sudo voice_esp32_enable
```
- Reset Matrix Voice to confirm operation. LED lights should turn off
```zsh
esptool.py --chip esp32 --port /dev/ttyS0 --baud 115200 --before default_reset --after hard_reset erase_flash
```
- output:
~~~
esptool.py v3.3.3
Serial port /dev/ttyS0
Connecting...
Failed to get PID of a device on /dev/ttyS0, using standard reset sequence.
.
Chip is ESP32-D0WDQ6 (revision v1.0)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
WARNING: Detected crystal freq 41.01MHz is quite different to normalized freq 40MHz. Unsupported crystal in use?
Crystal is 40MHz
MAC: 24:0a:c4:ab:df:70
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 9.6s
Hard resetting via RTS pin...
~~~


```zsh
# Installation Kernel Packages
sudo apt-get -y install raspberrypi-kernel-headers raspberrypi-kernel git 

# Installation Kernel Packages
sudo apt-get -y install raspberrypi-kernel-headers raspberrypi-kernel git 

# Reboot
sudo reboot

# Cloning & Compiling
git clone https://github.com/matrix-io/matrixio-kernel-modules
cd matrixio-kernel-modules/src
make
sudo make install
```


#### PyAudio
- Remove some warnings [LINK](https://forums.raspberrypi.com/viewtopic.php?t=136974)

~~~
ALSA lib pcm_oss.c:377:(_snd_pcm_oss_open) Unknown field port
ALSA lib pcm_oss.c:377:(_snd_pcm_oss_open) Unknown field port
ALSA lib pcm_a52.c:823:(_snd_pcm_a52_open) a52 is only for playback
ALSA lib conf.c:4871:(parse_args) Unknown parameter AES0
ALSA lib conf.c:5031:(snd_config_expand) Parse arguments error: No such file or directory
ALSA lib pcm.c:2565:(snd_pcm_open_noupdate) Unknown PCM iec958:{AES0 0x6 AES1 0x82 AES2 0x0 AES3 0x2  CARD 0}
ALSA lib pcm_usb_stream.c:486:(_snd_pcm_usb_stream_open) Invalid type for card
ALSA lib pcm_usb_stream.c:486:(_snd_pcm_usb_stream_open) Invalid type for card
ALSA lib pcm_dsnoop.c:575:(snd_pcm_dsnoop_open) The dsnoop plugin supports only capture stream
ALSA lib pcm_dsnoop.c:575:(snd_pcm_dsnoop_open) The dsnoop plugin supports only capture stream
ALSA lib pcm_dsnoop.c:575:(snd_pcm_dsnoop_open) The dsnoop plugin supports only capture stream
ALSA lib pcm_dsnoop.c:575:(snd_pcm_dsnoop_open) The dsnoop plugin supports only capture stream
ALSA lib pcm_dsnoop.c:575:(snd_pcm_dsnoop_open) The dsnoop plugin supports only capture stream
ALSA lib pcm_dsnoop.c:575:(snd_pcm_dsnoop_open) The dsnoop plugin supports only capture stream
ALSA lib pcm_dsnoop.c:575:(snd_pcm_dsnoop_open) The dsnoop plugin supports only capture stream
ALSA lib pcm_dsnoop.c:575:(snd_pcm_dsnoop_open) The dsnoop plugin supports only capture stream
ALSA lib pcm_dsnoop.c:575:(snd_pcm_dsnoop_open) The dsnoop plugin supports only capture stream
~~~

```zsh
pip3 install sounddevice

# and then in your code import sounddevice
```







