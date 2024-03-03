

from ..Model.camera.camera import Camera


from tkinter import PhotoImage
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk
import warnings
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

        self.playing_icon = PhotoImage(file=configuration.playing_icon_filepath)
        self.playing_icon_s = PhotoImage(file=configuration.playing_icon_s_filepath)
        self.start_icon = PhotoImage(file=configuration.start_icon_filepath)
        self.stop_icon = PhotoImage(file=configuration.stop_icon_filepath)
        self.pause_icon = PhotoImage(file=configuration.pause_icon_filepath)
        self.load_icon = PhotoImage(file=configuration.load_icon_filepath)
        self.settings_icon = PhotoImage(file=configuration.settings_icon_filepath)
        self.reset_icon = PhotoImage(file=configuration.reset_icon_filepath)
        warnings.filterwarnings('ignore', category=UserWarning, module='customtkinter.*')



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

        self.start_stop_frames(top_frame)
        self.demo_frame(bottom_frame)

    # FRAMES ---------------------------------------------
    def start_stop_frames(self, frame):

        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.start_button = ctk.CTkButton(frame, text='Button 1', font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.start_fg_color, hover_color=configuration.start_hover_color,
                                          image=self.start_icon, command=lambda: self.event_handler(Event.START_EXPERIMENT))
        self.start_button.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.pause_button = ctk.CTkButton(frame, text='Button 2',
                                          font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.button_fg_color,
                                          hover_color=configuration.button_hover_color,
                                          image=self.pause_icon, command=lambda: self.event_handler(Event.PAUSE))
        self.pause_button.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.settings_button = ctk.CTkButton(frame, text='Button 3', font=(configuration.main_font_style, configuration.main_font_size),
                                        fg_color=configuration.pause_fg_color, hover_color=configuration.pause_hover_color,
                                        image=self.settings_icon, command=lambda: self.event_handler(Event.SETTINGS))
        self.settings_button.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')


    def demo_frame(self, frame):

        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.demo_button = ctk.CTkButton(frame, text='Demo Overlay', font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.reset_fg_color, hover_color=configuration.reset_hover_color,
                                          image=self.load_icon, command=lambda: self.event_handler(Event.DEMO))
        self.demo_button.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')


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

        self.update_gui()

    def update_gui(self):
        try:
            frame = self.Camera.frame_queue.get_nowait()
            self.label.configure(image=frame)
            self.label.image = frame
        except queue.Empty:
            pass

        self.after(10, self.update_gui)




# ---------------------------------------------------
# RIGHT FRAME --------------------------------------
# ---------------------------------------------------

class Right_Frame(ctk.CTkFrame):
    def __init__(self, parent, event_handler):
        super().__init__(parent)
        self.event_handler = event_handler
        self.parent = parent

        self.playing_icon = PhotoImage(file=configuration.playing_icon_filepath)
        self.playing_icon_s = PhotoImage(file=configuration.playing_icon_s_filepath)
        self.start_icon = PhotoImage(file=configuration.start_icon_filepath)
        self.stop_icon = PhotoImage(file=configuration.stop_icon_filepath)
        self.pause_icon = PhotoImage(file=configuration.pause_icon_filepath)
        self.load_icon = PhotoImage(file=configuration.load_icon_filepath)
        self.settings_icon = PhotoImage(file=configuration.settings_icon_filepath)
        self.reset_icon = PhotoImage(file=configuration.reset_icon_filepath)
        warnings.filterwarnings('ignore', category=UserWarning, module='customtkinter.*')

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

        self.camera_settings_frame(top_frame)
        self.settings_frame(bottom_frame)

    # FRAMES ---------------------------------------------
    def settings_frame(self, frame):

        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        # frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.settings_button_1 = ctk.CTkButton(frame, text='Button 1', font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.pause_fg_color, hover_color=configuration.pause_hover_color,
                                          image=self.load_icon, command=lambda: self.event_handler(Event.SETTINGS_BUTTON_1))
        self.settings_button_1.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')



        self.settings_button = ctk.CTkButton(frame, text='Settings', font=(configuration.main_font_style, configuration.main_font_size),
                                        fg_color=configuration.pause_fg_color, hover_color=configuration.pause_hover_color,
                                        image=self.settings_icon, command=lambda: self.event_handler(Event.SETTINGS))
        self.settings_button.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.exit_button = ctk.CTkButton(frame, text='EXIT',
                                         font=(configuration.main_font_style, configuration.main_font_size),
                                         fg_color=configuration.stop_fg_color, hover_color=configuration.stop_hover_color,
                                         image=self.reset_icon, command=self.parent.close_application)
        self.exit_button.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')


    def camera_settings_frame(self, frame):

        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.capture_image_button = ctk.CTkButton(frame, text='Save Image', font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.start_fg_color, hover_color=configuration.start_hover_color,
                                          image=self.load_icon, command=lambda: self.event_handler(Event.TAKE_PICTURE))
        self.capture_image_button.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.capture_video_button = ctk.CTkButton(frame, text='Rec Video',
                                          font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.button_fg_color,
                                          hover_color=configuration.button_hover_color,
                                          image=self.load_icon, command=lambda: self.event_handler(Event.RECORD_VIDEO))
        self.capture_video_button.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')


        self.total_time_display = ctk.CTkLabel(frame, text='00:00',
                                               font=(configuration.main_font_style, configuration.main_font_size))
        self.total_time_display.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2,
                                     sticky='nsew')
