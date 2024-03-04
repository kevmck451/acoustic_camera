# ALSA Microphone Attempt
- [MatrixIO Kernal Modules](https://github.com/matrix-io/matrixio-kernel-modules/blob/master/README.md#option-1-package-installation)
- [Kernal Install](https://github.com/matrix-io/matrixio-kernel-modules/blob/master/README.md#option-1-package-installation)
- buster OS installed

- ssh into pi 
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

# Lists all the sound recording devices (microphones) detected by ALSA
arecord -l
```
~~~
**** List of CAPTURE Hardware Devices ****
card 2: Dummy [Dummy], device 0: Dummy PCM [Dummy PCM]
  Subdevices: 8/8
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
  Subdevice #4: subdevice #4
  Subdevice #5: subdevice #5
  Subdevice #6: subdevice #6
  Subdevice #7: subdevice #7
card 3: MATRIXIOSOUND [MATRIXIO-SOUND], device 0: matrixio.mic.0 snd-soc-dummy-dai-0 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
~~~

```zsh
arecord -D plughw:3,0 -f cd -d 10 -t wav test.wav
# works

alsamixer
# cool

arecord -D plughw:3,0 -f S16_LE -r 48000 -c 8 -d 10 -t wav test_8ch_16bit.wav
# doesnt work

sudo nano /etc/asound.conf
```
~~~
pcm.channel_7 {
    type dsnoop
    ipc_key 234884
    slave {
        pcm "hw:2,0"
        channels 8
    }
    bindings.0  6
}

pcm.channel_8 {
    type dsnoop
    ipc_key 234884
    slave {
        pcm "hw:2,0"
        channels 8
    }
    bindings.0  7
}

pcm.all_channels {
    type dsnoop
    ipc_key 234884
    slave {
        pcm "hw:2,0"
        channels 8
    }
    bindings {
            0 0
            0 1
            0 2
            0 3
            0 4
            0 5
            0 6
            0 7
    }
}
~~~
- changing binding to 
~~~
bindings {
        0 0
        1 1
        2 2
        3 3
        4 4
        5 5
        6 6
        7 7
}
~~~
```zsh
arecord -D plughw:3,0 -f S16_LE -r 48000 -c 8 -d 10 -t wav test_8ch_16bit.wav
scp pi@acousticpi.local:/home/pi/Desktop/acoustic_camera/TestScripts/mics/test_8ch_16bit.wav /Users/KevMcK/Desktop
# IT WORKED!!!
python3 recording.py
scp pi@acousticpi.local:/home/pi/Desktop/acoustic_camera/TestScripts/mics/output4.wav /Users/KevMcK/Desktop
```
- ran 'check_sound_settings.py' to see which devices were available
- Device 3: MATRIXIO-SOUND: - (hw:3,0) (Input Channels: 8)
- So for PyAudio.open() settings need to set 'input_device_index=3'

##### Mic Viewer libraries installed:

```zsh
pip install pycairo
pip install cairocffi
sudo apt-get install libcairo2-dev
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
pip install pycairo
```






