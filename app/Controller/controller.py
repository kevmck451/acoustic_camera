



from app.View.settings import Settings_Window
from app.Controller.events_states import Event
from app.Controller.events_states import State
from video_stream_server import Video_Overlay_Server


from threading import Thread
import threading
import numpy as np
import time



class Controller:
    def __init__(self):
        self.app_state = State.IDLE
        self.demo_stop = True

        self.video_stream_server = Video_Overlay_Server().start_server()
        # Start Hardware Scripts
        # Attempt to start camera and mic streams



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

        elif event == Event.ACOUSTIC_VIEWER:
            print('ACOUSTIC_VIEWER')

        elif event == Event.CAMERA_VIEWER:
            print('CAMERA_VIEWER')
            # start camera hardware if not connected already

        elif event == Event.ACOUSTIC_CAMERA_VIEWER:
            print('ACOUSTIC_CAMERA_VIEWER')


        # Window Closing Actions
        elif event == Event.ON_CLOSE:
            pass

        elif event == Event.START_CAMERA:
            pass

    # Action Functions ------------------------------



