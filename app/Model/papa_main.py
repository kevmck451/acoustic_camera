


from .microphones import MicArray
from .camera import Camera
from .overlay import Overlay
from .video_stream_sender import Video_Overlay_Sending
from .server_events import Event_Listener_Server


import threading
import time


if __name__ == "__main__":

    event_listener_server = Event_Listener_Server()

    # camera_hardware = Camera().start_camera()

    # server on FPGA will need to be running
    # mic_hardware = MicArray().start_client_connection()

    # video_feed = Overlay(mic_hardware, camera_hardware)

    # Generate way to constantly update overlays
    # video_thread = threading.Thread(target=video_feed.generate_overlay, daemon=True).start()

    # When event to start transmission
    # Send overlay through video stream socket to gui

    # overlay_stream = Video_Overlay_Sending()
    # overlay_stream.send_data(video_feed.overlay)









