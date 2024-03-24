


from app.View.overlay_threshold import Overlay_Threshold_Window
from app.View.settings import Settings_Window
from app.Controller.events_states import Event
from app.Controller.events_states import State





class Controller:
    def __init__(self):
        self.app_state = State.IDLE
        self.gui = None
        self.event_sender = None

    def set_gui(self, gui):
        self.gui = gui

    def set_event_sender(self, event_sender):
        self.event_sender = event_sender

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
            command = 'mic_overlay_color=blue'
            self.event_sender.send_data(command)

        elif event == Event.DUMMY_BUTTON:
            print('BUTTON PRESSED')

        elif event == Event.OVERLAY_COLOR_RED:
            # Check if Connected to Hardware
            if self.event_sender.connected:
                command = 'mic_overlay_color=red'
                self.event_sender.send_data(command)

                print('OVERLAY_COLOR_RED')
                self.gui.Left_Frame.toggle_overlay_color_button()

            else: print('Not Connected to Hardware')

        elif event == Event.OVERLAY_COLOR_BLUE:
            # Check if Connected to Hardware
            if self.event_sender.connected:
                command = 'mic_overlay_color=blue'
                self.event_sender.send_data(command)

                print('OVERLAY_COLOR_BLUE')
                self.gui.Left_Frame.toggle_overlay_color_button()

            else: print('Not Connected to Hardware')

        elif event == Event.OVERLAY_COLOR_GREEN:
            # Check if Connected to Hardware
            if self.event_sender.connected:
                command = 'mic_overlay_color=green'
                self.event_sender.send_data(command)

                print('OVERLAY_COLOR_GREEN')
                self.gui.Left_Frame.toggle_overlay_color_button()

            else: print('Not Connected to Hardware')

        elif event == Event.OVERLAY_THRESHOLD_WINDOW:
            if self.event_sender.connected:
                self.overlay_threshold_window = Overlay_Threshold_Window(self.handle_event)
                self.overlay_threshold_window.mainloop()


        elif event == Event.START_CAMERA:
            print('START_CAMERA')
            self.gui.Center_Frame.update_camera_feed()


        # Window Closing Actions
        elif event == Event.ON_CLOSE:
            pass

        elif event == Event.START_CAMERA:
            pass

    # Action Functions ------------------------------


