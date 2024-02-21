# Bread Crumbs for Matrix Voice Access to Microphones



## 4. Microphone Module
#### Links:
- [Product Purchase Page](https://www.newark.com/matrix-labs/matrix-voice-esp/voice-development-board-spartan/dp/55AC2404?gclid=Cj0KCQjwiIOmBhDjARIsAP6YhSVaI4keeU8VfIYhUSqK6x4ST3JNHzf88cvQXWHzEGxW4CGrv8TJlCUaAo5qEALw_wcB&mckv=_dc%7Cpcrid%7C%7Cplid%7C%7Ckword%7C%7Cmatch%7C%7Cslid%7C%7Cproduct%7C55AC2404%7Cpgrid%7C%7Cptaid%7C%7C&CMP=KNC-GUSA-PMAX-Shopping-High-ROAS-S40)
- [Device Overview PDF](https://www.farnell.com/datasheets/2608206.pdf?_ga=2.219371345.993533472.1539793131-901402398.1539269224)
- [ALSA Mic Overview](https://matrix-io.github.io/matrix-documentation/matrix-lite/py-reference/alsa-mics/)
- [MatrixIO Kernal Modules](https://github.com/matrix-io/matrixio-kernel-modules/blob/master/README.md#option-1-package-installation)

### Following option 1 from MatrixIO Kernel Modules
- Supposedly only works with buster

#### Buster OS
- Link to zip file [Link](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip)
- Used Raspberry Pi imager to image the SD card with this .img file
- Following steps from MatrixIO Kernel Modules

```zsh
sudo apt-get install --reinstall raspberrypi-bootloader raspberrypi-kernel
sudo apt update
sudo apt-get -y install raspberrypi-kernel-headers raspberrypi-kernel git 
sudo reboot
git clone https://github.com/matrix-io/matrixio-kernel-modules
cd matrixio-kernel-modules/src
make
sudo make install
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


### Following option 2 from MatrixIO Kernel Modules

##### Troubleshooting APT Repository and GPG Key Addition
- Found this [link] and at the bottom he said:
~~~
All the websites referencing the voice pi setup (matrix, hackster) 
point to an outdated repository which, confusingly, still has 
the key but an expired one. Here, for anyone reading this thread, 
is the correct way to install the matrix software and prepare it 
for flashing your satellite project.
~~~
~~~
curl https://s3.amazonaws.com/apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
sudo apt-get update
sudo apt-get upgrade
sudo apt install matrixio-kernel-modules
sudo reboot
sudo apt install matrixio-creator-init
sudo reboot
sudo voice_esp32_enable
esptool.py --chip esp32 --port /dev/ttyS0 --baud 115200 --before default_reset --after hard_reset erase_flash
~~~


##### Troubleshooting APT Repository and GPG Key Addition

1. Download the GPG Key Manually
```bash
curl -L https://apt.matrix.one/doc/apt-key.gpg -o matrix_key.gpg
```
- Instead of piping the output of curl directly to apt-key add, first save the GPG key to a file to ensure it's correctly downloaded.
- `-o matrix_key.gpg` saves the downloaded file as `matrix_key.gpg` in your current directory.
- After downloading, you can check if the `matrix_key.gpg` file looks correct (it should not be empty or contain error messages).

2. Manually Add the GPG Key
```bash
sudo apt-key add matrix_key.gpg
```
- After verifying the GPG key file, manually add it to your APT trusted keys.
- If there's an error in this step, it could be related to permissions, the GPG key itself, or your APT configuration.

3. Manually Add the Repository
```bash
lsb_release -sc
```
- Before adding the repository, ensure the command substitution `$(lsb_release -sc)` works correctly by running:
- This should output the codename of your Linux distribution (e.g., `buster` for Debian 10). If there's an issue here
- It might be because the `lsb-release` package isn't installed or there's a problem with your distribution's release information.

4. Manually construct the repository line and add it to your sources:
```bash
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
```
- Ensure this command successfully creates the `matrixlabs.list` file in `/etc/apt/sources.list.d/` and the content is correct.

5. Update APT and Install
```bash
sudo apt update
```
- After adding the key and repository, update your package lists:










