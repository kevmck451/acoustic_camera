
from enum import Enum, auto
from threading import Thread
import time
import threading


from app.View.settings import Settings_Window
from app.Controller.events import Event


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

        # Window Closing Actions
        elif event == Event.ON_CLOSE:
            pass

        elif event == Event.START_CAMERA:
            pass




# Define the states using an enumeration
class State(Enum):
    IDLE = auto()
    SHUTTING_DOWN = auto()
    SETTINGS_OPEN = auto()





