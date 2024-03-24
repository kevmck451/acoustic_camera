from app.Model.pi_hardware.microphones import MicArray

import threading
import time


if __name__ == "__main__":

    mic_array = MicArray()
    mic_array.start_client_connection()

    RMS_calculations = threading.Thread(target=mic_array.get_RMS)
    RMS_calculations.start()


    while True:
        time.sleep(.1)



