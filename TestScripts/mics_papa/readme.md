
# Mics from Papa

- start session: open two terminals
- ssh into papapi in both
- ssh into fpga on one
```zsh
# Terminal 1
ssh pi@papapi.local
ssh nixos@fpga
sudo server

# Terminal 2
# on macbook
ssh -X pi@papapi.local
cd Desktop/acoustic_camera
source venv_acoustic_camera/bin/activate
cd TestScripts/mics_papa
# export DISPLAY=:0 # if not using X11 forwarding 
python3 5_test.py
```




## Test Scripts
1. Modified noah's main code - not tested
2. Modified code to get chunk data from server
3. Calculates RMS of cube every 0.5 secs
4. Stops unconnecting from server for each chunks - works well
5. Heatmap of RMS values using matplotlib
   - Works on mac, but had issues running on screen pi


## random commands needed
```zsh
export DISPLAY=:0
```