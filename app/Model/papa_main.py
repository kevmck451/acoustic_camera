
from app.Model.server_events import Event_Server
from app.Model.pi_hardware.pi_hardware import PiHardware
from app.Model.overlay import Overlay
from app.Model.server_video_stream import Video_Server


import threading
import time



if __name__ == "__main__":


    # EVENT LISTENER SERVER-----------------------
    print('Event Listener Server Starting-----------------------')
    # set for simulation connection with 0.0.0.0 if testing
    # event_server = Event_Server('0.0.0.0')
    event_server = Event_Server()
    event_thread = threading.Thread(target=event_server.run, daemon=True)
    event_thread.start()

    print('Stating Papa Pi Hardware-----------------------')
    pi_hardware = PiHardware()

    print('Starting Overlay-----------------------')
    overlay = Overlay(pi_hardware)
    overlay_thread = threading.Thread(target=overlay.start_overlay, daemon=True)
    overlay_thread.start()

    event_server.set_hardware(pi_hardware, overlay)

    print('Video Stream Server Starting-----------------------')
    video_server = Video_Server()
    video_thread = threading.Thread(target=video_server.run, daemon=True)
    video_thread.start()

    video_server.set_hardware(overlay)
    event_server.set_video_server(video_server)


    print('Ready for Commands-----------------------')
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            print('Shutting Down')
            event_server.stop()
            video_server.stop()
            overlay.stop_overlay()
            break







