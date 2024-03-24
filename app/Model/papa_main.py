
from app.Model.server_events import Event_Server
from app.Model.pi_hardware.pi_hardware import PiHardware
from app.Model.overlay import Overlay


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

    print('Ready for Commands-----------------------')
    event_server.set_hardware(pi_hardware, overlay)

    # overlay_thread = threading.Thread(target=overlay.start_overlay, daemon=True)
    # overlay_thread.start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt: break







