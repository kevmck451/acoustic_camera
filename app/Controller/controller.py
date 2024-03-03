

from threading import Thread
import time
import threading


from app.View.settings import Settings_Window
from app.Controller.events_states import Event
from app.Controller.events_states import State


class Controller:
    def __init__(self):
        self.app_state = State.IDLE

    def set_gui(self, gui):
        self.gui = gui

    # These are the gate keepers for whether or not to perform the action
    def handle_event(self, event):

        # Load from Specific Stimulus Number:
        if event == Event.SETTINGS:
                self.settings_window = Settings_Window(self.handle_event)
                self.settings_window.mainloop()

        elif event == Event.SETTINGS_BUTTON_1:
            print('SETTINGS BUTTON 1 PRESSED')

        elif event == Event.SETTINGS_BUTTON_2:
            print('SETTINGS BUTTON 2 PRESSED')

        elif event == Event.TAKE_PICTURE:
            print('TAKE PICTURE')

        elif event == Event.RECORD_VIDEO:
            print('RECORD VIDEO')

        elif event == Event.DUMMY_BUTTON:
            print('BUTTON PRESSED')

        elif event == Event.DEMO:
            print('DEMO BUTTON PRESSED')
            self.start_demo()

        # Window Closing Actions
        elif event == Event.ON_CLOSE:
            pass

        elif event == Event.START_CAMERA:
            pass

    # Action Functions ------------------------------
    def start_demo(self):
        threading.Thread(target=self.demo, daemon=True).start()

    def demo(self):
        positions = [(100, 100), (400, 100), (400, 400), (100, 400)]  # Corners of a square path
        size_changes = [50, 60, 70, 80]  # Sizes to cycle through
        transparencies = [0.5, 0.6, 0.7, 0.8]  # Transparencies to cycle through
        colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]  # Colors to cycle through (BGR)

        while True:
            for i in range(len(positions)):
                # Update square attributes
                self.gui.Camera.square_position = positions[i]
                self.gui.Camera.square_size = size_changes[i % len(size_changes)]
                self.gui.Camera.square_transparency = transparencies[i % len(transparencies)]
                self.gui.Camera.square_color = colors[i % len(colors)]

                # Wait a bit before the next update
                time.sleep(1)



