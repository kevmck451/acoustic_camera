

from ..Model.camera.camera import Camera

import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
import queue




import app.View.configuration as configuration
from app.Controller.events import Event


class Main_Window(ctk.CTk):
    def __init__(self, event_handler):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.event_handler = event_handler

        # Computer Icon
        img = Image.open(configuration.main_window_icon)
        icon = ImageTk.PhotoImage(img)
        self.tk.call('wm', 'iconphoto', self._w, icon)

        # Main Setup ------------------------------------------------------------
        self.title(configuration.window_title)

        # Start full screen
        self.attributes('-fullscreen', True)

        # Get the screen dimension
        # screen_width = self.winfo_screenwidth()
        # screen_height = self.winfo_screenheight()
        # center_x = int((screen_width / 2) - (configuration.window_width / 2))
        # center_y = int((screen_height / 2) - (configuration.window_height / 2))
        # self.geometry(f'{configuration.window_width}x{configuration.window_height}+{center_x}+{center_y}')
        # self.minsize(configuration.min_window_width, configuration.min_window_height)

        # self.Console_Frame = Console_Frame(self)
        # self.Main_Frame = Main_Frame(self, self.Console_Frame, self.event_handler)
        self.Left_Frame = Left_Frame(self, self.event_handler)
        self.Video_Frame = Video_Frame(self, self.event_handler)
        self.Right_Frame = Right_Frame(self, self.event_handler)

        # Grid configuration
        self.columnconfigure(0, weight=1)  # Left column with 2/3 of the space
        self.columnconfigure(1, weight=1)  # Right column with 1/3 of the space
        self.columnconfigure(2, weight=1)  # Right column with 1/3 of the space

        # Place the frames using grid
        self.Left_Frame.grid(row=0, column=0, sticky='nsew')  # Left frame in column 0
        self.Video_Frame.grid(row=0, column=1, sticky='nsew')  # Right frame in column 1
        self.Right_Frame.grid(row=0, column=2, sticky='nsew')  # Right frame in column 1

        # Ending Procedures
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Escape>", self.close_application)

    def on_close(self):
        # Perform any cleanup or process termination steps here
        # For example, safely terminate any running threads, save state, release resources, etc.

        self.event_handler(Event.ON_CLOSE)
        self.destroy()

    def close_application(self, event=None):
        # Perform any cleanup or process termination steps here
        # Then close the application
        self.on_close()


# ---------------------------------------------------
# LEFT FRAME --------------------------------------
# ---------------------------------------------------
class Left_Frame(ctk.CTkFrame):
    def __init__(self, parent, event_handler):
        super().__init__(parent)
        self.event_handler = event_handler





        # Top Frame
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')


        top_frame.grid_rowconfigure(0, weight=1, uniform='row')

        # Middle Frame
        middle_frame = ctk.CTkFrame(self)
        middle_frame.grid(row=1, column=0, padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')

        middle_frame.grid_rowconfigure(0, weight=1, uniform='row')

        # Bottom Frame
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=2, column=0, padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')

        bottom_frame.grid_rowconfigure(0, weight=1, uniform='row')

        # Configure the grid rows and column for self
        self.grid_rowconfigure(0, weight=1)  # Top row
        self.grid_rowconfigure(1, weight=1)  # Middle row
        self.grid_rowconfigure(2, weight=1)  # Bottom row
        self.grid_columnconfigure(0, weight=1, uniform='col')  # Single column

    # FRAMES ---------------------------------------------



# ---------------------------------------------------
# VIDEO FRAME --------------------------------------
# ---------------------------------------------------
class Video_Frame(ctk.CTkFrame):
    def __init__(self, parent, event_handler):
        super().__init__(parent)
        self.event_handler = event_handler

        self.Camera = Camera()

        self.label = tk.Label(self)  # Assuming video display within the custom frame
        self.label.pack()

        # Overlay properties
        self.overlay_position = [50, 50]  # Default position
        self.overlay_size = 100  # Default size (square)
        self.overlay_color = (255, 0, 0)  # Default color (green, in BGR format)

        # Movement properties
        self.move_direction = 1  # 1 for right, -1 for left
        self.move_speed = 2  # Pixels per update

        self.update_gui()

    def update_gui(self):
        try:
            frame = self.Camera.frame_queue.get_nowait()
            self.label.configure(image=frame)
            self.label.image = frame
        except queue.Empty:
            pass

        self.after(10, self.update_gui)

    def update_overlay(self, position=None, size=None, color=None):
        if position is not None:
            self.overlay_position = position
        if size is not None:
            self.overlay_size = size
        if color is not None:
            # Convert color from RGB (or whatever format you use) to BGR for OpenCV
            self.overlay_color = color[::-1]  # Assuming color is given in RGB and converting to BGR



# ---------------------------------------------------
# RIGHT FRAME --------------------------------------
# ---------------------------------------------------

class Right_Frame(ctk.CTkFrame):
    def __init__(self, parent, event_handler):
        super().__init__(parent)
        self.event_handler = event_handler



        # Top Frame
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')

        top_frame.grid_rowconfigure(0, weight=1, uniform='row')

        # Middle Frame
        middle_frame = ctk.CTkFrame(self)
        middle_frame.grid(row=1, column=0, padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')

        middle_frame.grid_rowconfigure(0, weight=1, uniform='row')

        # Bottom Frame
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=2, column=0, padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')

        bottom_frame.grid_rowconfigure(0, weight=1, uniform='row')

        # Configure the grid rows and column for self
        self.grid_rowconfigure(0, weight=1)  # Top row
        self.grid_rowconfigure(1, weight=1)  # Middle row
        self.grid_rowconfigure(2, weight=1)  # Bottom row
        self.grid_columnconfigure(0, weight=1, uniform='col')  # Single column

    # FRAMES ---------------------------------------------










