# ALSA Microphone Attempt
- [MatrixIO Kernal Modules](https://github.com/matrix-io/matrixio-kernel-modules/blob/master/README.md#option-1-package-installation)
- [Kernal Install](https://github.com/matrix-io/matrixio-kernel-modules/blob/master/README.md#option-1-package-installation)
- buster OS installed

- ssh into pi (didnt use -X)
- cd to acoustic_camera folder
- activated VE which has access to system libraries

```zsh
sudo apt-get install --reinstall raspberrypi-bootloader raspberrypi-kernel
sudo apt update
curl https://s3.amazonaws.com/apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://s3.amazonaws.com/apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```
- Successful install
- ssh back into and get back in VE
```zsh
# Installation MATRIX Packages
sudo apt install matrixio-kernel-modules
```
- Successful install
```zsh
sudo apt install portaudio19-dev 
sudo python3 -m pip install pyaudio
nano /etc/asound.conf
# check speaker output like in link
```
- [Mic Link](https://matrix-io.github.io/matrix-documentation/matrix-voice/resources/microphone/)
```zsh
arecord recording.wav -f S16_LE -r 16000 -d 5
aplay recording.wav

scp pi@acousticpi.local:/home/pi/Desktop/acoustic_camera/TestScripts/mics/recording.wav /Users/KevMcK/Desktop
```
- Recording file didnt have any data, all 0's
```zsh
sudo apt install python3-pyaudio





```


