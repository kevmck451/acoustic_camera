

from app.Model.pi_hardware.server_events import Event_Server
from app.Model.pi_hardware.microphones import MicArray
from app.Model.pi_hardware.camera import Camera


import threading

class PiHardware:

    def __init__(self):
        print('Initializing Hardware')

        # EVENT LISTENER SERVER-----------------------
        print('EVENT LISTENER SERVER-----------------------')
        # set for simulation connection with 0.0.0.0 if testing
        # event_server = Event_Server('0.0.0.0')
        self.event_server = Event_Server()
        self.event_thread = threading.Thread(target=self.event_server.run, daemon=True)
        self.event_thread.start()

        # MICROPHONE HARDWARE CONNECTION--------------
        # server on FPGA will need to be running
        print('MICROPHONE HARDWARE CONNECTION--------------')
        self.mic_hardware = MicArray()
        self.mic_hardware.start_client_connection()
        self.mic_thread = threading.Thread(target=self.mic_hardware.get_RMS, daemon=True)
        self.mic_thread.start()

        # CAMERA HARDWARE CONNECTION-----------------
        print('CAMERA HARDWARE CONNECTION-----------------')
        self.camera_hardware = Camera(fps=30, color=True) # width=580, height=580,
        # self.camera_hardware.start_viewing()





if __name__ == "__main__":
    print('Stating Papa Pi Hardware')
    pi_hardware = PiHardware()