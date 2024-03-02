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
ssh -X pi@192.168.0.111
# if using hostname
# ssh -X pi@hostname.local
# ssh-keygen -f "/Users/KevMcK/.ssh/known_hosts" -R "192.168.0.147"
# -X is to show diaply on remote screen

# Update everything
sudo apt update
sudo apt full-upgrade
sudo apt autoremove
sudo apt clean
sudo reboot
````
## Project Directory / Github Connection
- My preferred work flow is to program and run files on the pi from my desktop computer as opposed to on the pi directly. 
- If you are doing everything on the pi, then you can skip this step. 
- It's still recommended to create a github repo to back up your work and tracking progress.
- clone repo to pi and desktop computer
```zsh
git clone https://github.com/kevmck451/acoustic_camera
```

## ---------------------------------------------------------
## Camera Module
This is for BusterOS
#### Links:
- [PiCamera2 Library Documentation](https://picamera.readthedocs.io/en/release-1.13/install.html)

#### First Connection
- ```python -c "import picamera"```
- If no error, you're good
- ```raspistill -o image.jpg```
- If shows preview window and save image, you're good

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
cd acoustic_camera/TestScripts/camera/picam/
```
- 1_test.py: works
- 2_test.py: works
- 3_test.py: works
- 4_test.py: works
- 5_test.py: works

##### 3.8. Capturing to a network stream: 
- this would be good when transfering from pi to pi
- 6_test.py: works
  - ran server through ssh'd session
  - ran client directly from pi terminal 

