## PiCam Camera Module
- This worked fine but didnt seem to integrated well into customtkinter
- Becuase of this, switched to using cv2 and moved to gui_integration with cv2 and ctk
- This is for BusterOS
- 
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
- **6_test.py: works**
  - 3.8. Capturing to a network stream: 
  - this would be good when transfering from pi to pi
  - ran server through ssh'd session
  - ran client directly from pi terminal 
- 7_test.py: works
- 8_test.py: works
  - 3.12. Recording to a circular stream
  - this would be good for if confident detection made, start recording video
- 9_test.py: 
  - not totally worked out, but if needed will come back
- **10_test.py: works**
  - 3.14. Overlays
- 11_test.py: 
  - zooming with overlays
  - not totally worked out, but will come back if needed










