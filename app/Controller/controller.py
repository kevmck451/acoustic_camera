



from app.Model.mic_matrix import Matrix_Mics
from app.View.settings import Settings_Window
from app.Controller.events_states import Event
from app.Controller.events_states import State



from threading import Thread
import threading
import numpy as np
import time



class Controller:
    def __init__(self):
        self.app_state = State.IDLE
        self.demo_stop = True
        self.matrix_mics = Matrix_Mics()




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


        elif event == Event.GET_PLOT_VALUES:
            self.get_audio_visuals()

        elif event == Event.NEED_ACOUSTIC_FIGURE:
            self.gui.Left_Frame.audio_feed_figure = self.matrix_mics.ch8_viewer_figure()

        elif event == Event.CAMERA_VIEWER:
            print('CAMERA_VIEWER')

        elif event == Event.ACOUSTIC_CAMERA_VIEWER:
            print('ACOUSTIC_CAMERA_VIEWER')

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
            self.matrix_mics.stop_stream()

        elif event == Event.START_CAMERA:
            pass

    # Action Functions ------------------------------

    def get_audio_visuals(self):
        threshold = 800
        data = self.matrix_mics.get_audio_data()
        for i in range(self.matrix_mics.mic_channels):
            channel_data = data[i::self.matrix_mics.mic_channels]
            if np.any(np.abs(channel_data) > threshold):
                self.gui.Left_Frame.audio_feed_figure.lines[i].set_color('red')  # Change color to red if threshold is exceeded
            else:
                self.gui.Left_Frame.audio_feed_figure.lines[i].set_color('blue')  # Reset to default color otherwise
            self.gui.Left_Frame.audio_feed_figure.lines[i].set_ydata(channel_data)



    def start_demo(self):
        print('start demo')
        self.demo_stop = True
        threading.Thread(target=self.demo, daemon=True).start()

    def stop_demo(self):
        print('stop demo')
        self.demo_stop = False
        self.gui.Camera.clear_squares()

    def demo(self):
        # Create a list to hold properties for 4 squares
        # squares = [{
        #     'position': [100, 100],  # Starting position
        #     'direction': [2, 3],  # Initial movement direction
        #     'size': 50,
        #     'color': [0, 100, 200],
        #     'transparency': 0.6
        # } for _ in range(4)]  # Creates 4 square dicts with the same initial properties

        squares = [
            {
                'position': [100, 100],  # Starting position
                'direction': [2, 2],  # Initial movement direction
                'size': 50,
                'color': [255, 0, 0],  # Red
                'transparency': 0.6
            },
            {
                'position': [200, 100],  # Starting position
                'direction': [-2, 3],  # Initial movement direction, moving left and down
                'size': 60,
                'color': [0, 255, 0],  # Green
                'transparency': 0.6
            },
            {
                'position': [300, 100],  # Starting position
                'direction': [3, -2],  # Initial movement direction, moving right and up
                'size': 70,
                'color': [0, 0, 255],  # Blue
                'transparency': 0.6
            },
            {
                'position': [400, 100],  # Starting position
                'direction': [-3, -2],  # Initial movement direction, moving left and up
                'size': 80,
                'color': [255, 255, 0],  # Yellow
                'transparency': 0.6
            }
        ]

        max_width, max_height = 580, 580  # Maximum dimensions
        min_size, max_size = 20, 150  # Size range
        size_increment = 1
        transparency_increment = 0.01
        color_increment = [1, 2, 3]  # Adjust as needed for visual effect

        while self.demo_stop:
            for square in squares:
                position = square['position']
                size = square['size']
                color = square['color']

                # Update position and reverse direction on bounds
                for i in range(2):
                    position[i] += square['direction'][i]
                    if position[i] >= max_width - size or position[i] <= 0:
                        square['direction'][i] *= -1

                # Update size
                size += size_increment
                if size >= max_size or size <= min_size:
                    size_increment *= -1

                # Update transparency (Example logic, customize as needed)
                # square['transparency'] += transparency_increment
                # if square['transparency'] >= 1.0 or square['transparency'] <= 0.1:
                #     transparency_increment *= -1

                # Update color
                for i in range(3):
                    color[i] += color_increment[i]
                    if color[i] > 255 or color[i] < 0:
                        color_increment[i] *= -1
                    color[i] = max(0, min(255, color[i]))

                # Apply updates
                square['position'] = position
                square['size'] = size
                square['color'] = color

            # Draw each square on the frame
            # Assuming there is a method in gui.Camera to clear previous squares
            self.gui.Camera.clear_squares()
            for square in squares:
                self.gui.Camera.add_square(square['position'], square['size'], tuple(square['color']),
                                           square['transparency'])

            time.sleep(0.05)


    # def demo(self):
    #     # Initial setup
    #     direction = [2, 3]  # Initial direction for movement (x, y)
    #     max_width, max_height = 580, 580  # Maximum dimensions based on the camera setup
    #     min_size, max_size = 20, 150  # Min and max square sizes
    #     size_increment = 1  # Size change per iteration
    #     transparency_increment = 0.1  # Transparency change per iteration
    #     color_increment = [1, 1, 1]  # RGB color change per iteration
    #
    #     while self.demo_stop:
    #         position = list(self.gui.Camera.square_position)
    #         size = self.gui.Camera.square_size
    #         transparency = 0.6
    #         color = list(self.gui.Camera.square_color)
    #
    #         # Update position
    #         for i in range(2):
    #             position[i] += direction[i]
    #             if position[i] >= max_width - size or position[i] <= 0:
    #                 direction[i] *= -1  # Reverse direction on hitting bounds
    #
    #         # Update size
    #         size += size_increment
    #         if size >= max_size or size <= min_size:
    #             size_increment *= -1  # Reverse size change direction
    #
    #         # Update transparency
    #         # transparency += transparency_increment
    #         # if transparency >= 1.0 or transparency <= 0.1:
    #         #     transparency_increment *= -1  # Reverse transparency change direction
    #
    #         # Update color
    #         for i in range(3):
    #             color[i] += color_increment[i]
    #             if color[i] > 255 or color[i] < 0:
    #                 color_increment[i] *= -1  # Reverse color change direction
    #             color[i] = max(0, min(255, color[i]))  # Ensure color stays within valid range
    #
    #         # Apply updates
    #         self.gui.Camera.square_position = tuple(position)
    #         self.gui.Camera.square_size = size
    #         self.gui.Camera.square_transparency = transparency
    #         self.gui.Camera.square_color = tuple(color)
    #
    #         # Wait a bit before the next update to make the movement visible
    #         time.sleep(0.05)



