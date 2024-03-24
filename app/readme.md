

# Running Things & Demos

- Need to create bash scripts that do all this with commands
```zsh
. start_fpga.sh
. start_event_client_thread.sh
. start_papa_main.sh
```

## FPGA Audio Server
```zsh
ssh pi@papapi.local #123456
ssh nixos@fpga # no password, hit enter
sudo server
```


## Event Client
- how to control pi hardware from external controller
- otherwise this functionality is incorporated into app
```zsh
ssh pi@papapi.local #123456
cd Desktop/acoustic_camera
source venv_acoustic_camera/bin/activate
cd app/Controller
python3 client_events.py
```


## Papa Main Script
```zsh
ssh -X pi@papapi.local #123456
cd Desktop/acoustic_camera
source venv_acoustic_camera/bin/activate
python3 -m app.Model.papa_main
```


## App Main Script
- should run on any computer since it doesnt directly control any hardware
```zsh
cd Desktop/acoustic_camera
source venv_app/bin/activate
```
- need to get requirements from current venv on screen
- change name with new venv and install requirements






# Acoustic Camera Demo
- inside overlay function:
  - to view the audio heat map, uncomment in init method the audio_scale_thread with view audio heatmap
  - to view camera + acoustic heat map uncomment the overlay thread with view_overlay







# App Timeline


# Application is started 


- Controller Started
- Gui Started
- Controller and Gui are bonded
- Main Loop


# Connection to hardware is attempted
- If cant find, try again in a few seconds
  - When Event Listener Connection made
    - PiCam Connection
    - FPGA Connection
    - Handshake and acknowledgement
      - Sets connection flag true
