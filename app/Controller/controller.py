

from threading import Thread
import time
import threading


from app.View.settings import Settings_Window
from app.Controller.events_states import Event
from app.Controller.events_states import State


class Controller:
    def __init__(self):
        self.app_state = State.IDLE
        self.demo_stop = True

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
            if self.app_state == State.IDLE:
                self.app_state = State.DEMO_IN_PROGRESS
                self.gui.Left_Frame.toggle_demo_button()
                self.start_demo()
            elif self.app_state == State.DEMO_IN_PROGRESS:
                self.app_state = State.IDLE
                self.gui.Left_Frame.toggle_demo_button()
                self.stop_demo()

        # Window Closing Actions
        elif event == Event.ON_CLOSE:
            pass

        elif event == Event.START_CAMERA:
            pass

    # Action Functions ------------------------------
    def start_demo(self):
        print('start demo')
        self.demo_stop = True
        threading.Thread(target=self.demo, daemon=True).start()

    def stop_demo(self):
        print('stop demo')
        self.demo_stop = False
        self.gui.Camera.square_transparency = 0


    def demo(self):
        # Initial setup
        direction = [2, 3]  # Initial direction for movement (x, y)
        max_width, max_height = 580, 580  # Maximum dimensions based on the camera setup
        min_size, max_size = 20, 150  # Min and max square sizes
        size_increment = 1  # Size change per iteration
        transparency_increment = 0.1  # Transparency change per iteration
        color_increment = [1, 20, 40]  # RGB color change per iteration

        while self.demo_stop:
            position = list(self.gui.Camera.square_position)
            size = self.gui.Camera.square_size
            transparency = 0.6
            color = list(self.gui.Camera.square_color)

            # Update position
            for i in range(2):
                position[i] += direction[i]
                if position[i] >= max_width - size or position[i] <= 0:
                    direction[i] *= -1  # Reverse direction on hitting bounds

            # Update size
            size += size_increment
            if size >= max_size or size <= min_size:
                size_increment *= -1  # Reverse size change direction

            # Update transparency
            # transparency += transparency_increment
            # if transparency >= 1.0 or transparency <= 0.1:
            #     transparency_increment *= -1  # Reverse transparency change direction

            # Update color
            if size % 5 == 0:
                for i in range(3):
                    color[i] += color_increment[i]
                    if color[i] > 255 or color[i] < 0:
                        color_increment[i] *= -1  # Reverse color change direction
                    color[i] = max(0, min(255, color[i]))  # Ensure color stays within valid range

            # Apply updates
            self.gui.Camera.square_position = tuple(position)
            self.gui.Camera.square_size = size
            self.gui.Camera.square_transparency = transparency
            self.gui.Camera.square_color = tuple(color)

            # Wait a bit before the next update to make the movement visible
            time.sleep(0.05)



