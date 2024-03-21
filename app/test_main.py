from .Model.microphones import MicArray
from .Model.socket_events import Event_Listener_Socket

import threading
import time


if __name__ == "__main__":

    mic_array = MicArray()
    mic_array.start_client_connection()

    RMS_calculations = threading.Thread(target=mic_array.get_RMS, daemon=True)
    RMS_calculations.start()


    while True:
        try:
            time.sleep(.1)

        except KeyboardInterrupt:
            mic_array.end_client_connection()



