


# from .microphones import MicArray
# from .camera import Camera
# from .overlay import Overlay
# from .video_stream_sender import Video_Overlay_Sending
# from .server_events import Event_Listener_Server


from server_events import Event_Server
from microphones import MicArray
from camera import Camera
from overlay import Overlay

# from overlay import Overlay
# from video_stream_sender import Video_Overlay_Sending


import threading
import time
import cv2 # pip install opencv-python # This will take really long time

class PiHardware:

    def __init__(self):
        print('Initializing Setup')

        print('EVENT LISTENER SERVER-----------------------')
        self.event_server = Event_Server()
        # set for simulation connection with 0.0.0.0 if testing
        # event_server = Event_Server('0.0.0.0')
        self.event_thread = threading.Thread(target=self.event_server.run, daemon=True)
        self.event_thread.start()

        print('MICROPHONE HARDWARE CONNECTION--------------')
        # server on FPGA will need to be running
        self.mic_hardware = MicArray()
        self.mic_hardware.start_client_connection()
        # print(mic_hardware)
        self.mic_thread = threading.Thread(target=self.mic_hardware.get_RMS, daemon=True)
        self.mic_thread.start()

        print('CAMERA HARDWARE CONNECTION-----------------')
        self.camera_hardware = Camera(fps=25, color=False)
        # self.camera_hardware.start_viewing()

        # self.overlay = Overlay(self.camera_hardware, self.mic_hardware)

    # def start(self):
    #     # Start event, mic, and camera threads
    #
    #     print('OVERLAY PROCESS-----------------')
    #     overlay_thread = threading.Thread(target=self.overlay.update, daemon=True)
    #     overlay_thread.start()


# def view_camera(camera_instance):
#     while True:
#         frame = camera_instance.get_latest_frame()
#         print(type(frame))
#         # print(frame.shape)
#         if frame is not None:
#             cv2.imshow('Camera Feed', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#
#     cv2.destroyAllWindows()

def view_camera(camera_instance):
    cv2.namedWindow('Camera Feed', cv2.WINDOW_AUTOSIZE)  # Create a window for display.
    while True:
        frame = camera_instance.get_latest_frame()
        if frame is not None:
            print('<class \'numpy.ndarray\'>')
            cv2.imshow('Camera Feed', frame)
        else:
            print('<class \'NoneType\'>')
            time.sleep(0.1)  # Small delay to wait for the next frame

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Break the loop if 'q' is pressed.
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    print('Papa Pi Hardware')
    pi_hardware = PiHardware()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt: break







