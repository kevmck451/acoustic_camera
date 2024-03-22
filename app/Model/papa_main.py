


# from .microphones import MicArray
# from .camera import Camera
# from .overlay import Overlay
# from .video_stream_sender import Video_Overlay_Sending
# from .server_events import Event_Listener_Server


from server_events import Event_Server
from microphones import MicArray

# from camera import Camera
# from overlay import Overlay
# from video_stream_sender import Video_Overlay_Sending



import threading
import time

def run_pi_hardware():
    print('Initializing Setup')

    print('EVENT LISTENER SERVER-----------------------')
    # set for simulation connection with 0.0.0.0 if testing
    event_server = Event_Server('0.0.0.0')
    # event_server = Event_Server()
    event_thread = threading.Thread(target=event_server.run, daemon=True)
    event_thread.start()

    print('MICROPHONE HARDWARE CONNECTION--------------')

    # server on FPGA will need to be running
    mic_hardware = MicArray().start_client_connection()
    mic_thread = threading.Thread(target=mic_hardware.get_RMS, daemon=True)
    mic_thread.start()







if __name__ == "__main__":
    print('Papa Pi Hardware')
    run_pi_hardware()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt: break







