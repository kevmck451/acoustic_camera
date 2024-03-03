

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

        # Window Closing Actions
        elif event == Event.ON_CLOSE:
            pass

        elif event == Event.START_CAMERA:
            pass










