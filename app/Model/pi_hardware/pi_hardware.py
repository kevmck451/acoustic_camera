


from app.Model.pi_hardware.microphones import MicArray
from app.Model.pi_hardware.camera import Camera


import threading

class PiHardware:

    def __init__(self):
        print('Initializing Hardware')

        # MICROPHONE HARDWARE CONNECTION--------------
        # server on FPGA will need to be running
        print('MICROPHONE HARDWARE CONNECTION--------------')
        self.mic_hardware = MicArray()
        self.mic_hardware.start_client_connection()
        self.mic_thread = threading.Thread(target=self.mic_hardware.get_RMS, daemon=True)
        self.mic_thread.start()

        # CAMERA HARDWARE CONNECTION-----------------
        print('CAMERA HARDWARE CONNECTION-----------------')
        self.camera_hardware = Camera(width=560, height=560, fps=30, color=True) # width=580, height=580,
        # self.camera_hardware.start_viewing()





if __name__ == "__main__":
    print('Stating Papa Pi Hardware')
    pi_hardware = PiHardware()