
from app.Model.pi_hardware.pi_hardware import PiHardware
from app.Model.overlay import Overlay



import time




if __name__ == "__main__":
    print('Papa Pi Hardware')

    pi_hardware = PiHardware()
    overlay = Overlay(pi_hardware)

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt: break







