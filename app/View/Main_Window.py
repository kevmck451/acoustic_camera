


import app.View.configuration as configuration
from app.Controller.events_states import Event

# import matplotlib
# matplotlib.use('TkAgg')  # Specify the backend
from tkinter import PhotoImage
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk
import warnings
import queue
import cv2





class Main_Window(ctk.CTk):
    def __init__(self, event_handler):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.event_handler = event_handler

        # Computer Icon
        # img = Image.open(configuration.main_window_icon)
        # icon = ImageTk.PhotoImage(img)
        # self.tk.call('wm', 'iconphoto', self._w, icon)

        # Main Setup ------------------------------------------------------------
        self.title(configuration.window_title)

        # Screen: full screen
        self.attributes('-fullscreen', True)

        # Screen: can see window
        # screen_width = self.winfo_screenwidth()
        # screen_height = self.winfo_screenheight()
        # center_x = int((screen_width / 2) - (configuration.window_width / 2))
        # center_y = int((screen_height / 2) - (configuration.window_height / 2))
        # self.geometry(f'{configuration.window_width}x{configuration.window_height}+{center_x}+{center_y}')
        # self.minsize(configuration.min_window_width, configuration.min_window_height)

        # -------------------------------
        # MAIN TWO LEVELS: TOP AND BOTTOM
        # -------------------------------
        self.Console_Frame = Console_Frame(self)
        self.Main_Frame = Main_Frame(self, self.Console_Frame, self.event_handler)

        # Configure grid rows with equal weight
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)


        # Place the frames using grid
        self.Console_Frame.grid(row=0, column=0, sticky='nsew')
        self.Main_Frame.grid(row=1, column=0, sticky='nsew')

        self.columnconfigure(0, weight=1)

        # Ending Procedures
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Escape>", self.close_application)
        self.bind("<Control-c>", self.close_application)

    def set_video_sender(self, video_server):
        self.video_sender = video_server

    def on_close(self):
        # Perform any cleanup or process termination steps here
        # For example, safely terminate any running threads, save state, release resources, etc.
        # self.matrix_mics.stop_stream()
        self.event_handler(Event.ON_CLOSE)
        self.destroy()

    def close_application(self, event=None):
        # Perform any cleanup or process termination steps here
        # Then close the application
        self.on_close()


# ---------------------------------------------------
# CONSOLE FRAME --------------------------------------
# ---------------------------------------------------
class Console_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Main Frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')

        # Configure the columns and rows of main_frame to expand
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        self.console_box(main_frame)

    def console_box(self, frame):
        # Experiment Metadata Info Box (Title)
        self.title = ctk.CTkLabel(frame, text="Acoustic Camera", font=configuration.console_font_style)
        # Place the title in the third column, centered
        self.title.grid(row=0, column=0, padx=configuration.console_x_pad, pady=configuration.console_y_pad, sticky='nsew')

        self.main_info_label = ctk.CTkLabel(frame, text="University of Memphis", font=configuration.console_font_style)
        # Place the main info label in the third column, centered
        self.main_info_label.grid(row=1, column=0, padx=configuration.console_x_pad, pady=configuration.console_y_pad, sticky='nsew')



# ---------------------------------------------------
# MAIN FRAME --------------------------------------
# ---------------------------------------------------
class Main_Frame(ctk.CTkFrame):
    def __init__(self, parent, console_frame, event_handler):
        super().__init__(parent)
        self.console_frame = console_frame
        self.event_handler = event_handler
        self.parent = parent

        self.Left_Frame = Left_Frame(self, self.event_handler)
        self.Center_Frame = Video_Frame(self, self.event_handler)
        self.Right_Frame = Right_Frame(self, self.event_handler)

        # Grid configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)  # Left column with x/3 of the space
        self.columnconfigure(1, weight=2)  # Right column with x/3 of the space
        self.columnconfigure(2, weight=1)  # Right column with x/3 of the space




        # Place the frames using grid
        self.Left_Frame.grid(row=0, column=0, sticky='nsew')  # Left frame in column 0
        self.Center_Frame.grid(row=0, column=1, sticky='nsew')  # Right frame in column 1
        self.Right_Frame.grid(row=0, column=2, sticky='nsew')  # Right frame in column 1


# ---------------------------------------------------
# VIDEO FRAME --------------------------------------
# ---------------------------------------------------
class Video_Frame(ctk.CTkFrame):
    def __init__(self, parent, event_handler):
        super().__init__(parent)
        self.parent = parent
        self.event_handler = event_handler
        self.label = tk.Label(self)  # Assuming video display within the custom frame
        self.label.pack(expand=True, fill='both')

    def update_frame(self, cv_image):
        # Convert the OpenCV image to PIL format
        pil_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGBA))
        tk_image = ImageTk.PhotoImage(image=pil_image)

        # Update the label with the new image
        self.label.configure(image=tk_image)
        self.label.image = tk_image  # Keep a reference to avoid garbage collection



# ---------------------------------------------------
# LEFT FRAME --------------------------------------
# ---------------------------------------------------
class Left_Frame(ctk.CTkFrame):
    def __init__(self, parent, event_handler):
        super().__init__(parent)
        self.event_handler = event_handler
        self.parent = parent

        self.demo_button_state = True
        self.audio_feed_figure = None
        self.update_mic_levels_id = None

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

        self.detection_overlays(top_frame)
        self.overlay_options(middle_frame)
        self.template_button_frame_z(bottom_frame)

    # FRAMES ---------------------------------------------

    # Detection Overlays: Sound, Drones, Vehicles
    def detection_overlays(self, frame):

        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.button_detect_sounds = ctk.CTkButton(frame, text='Detect Sounds', font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.gray_fg_color, hover_color=configuration.gray_hover_color,
                                          command=lambda: self.event_handler(Event.DETECT_SOUNDS))
        self.button_detect_sounds.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.button_detect_drones = ctk.CTkButton(frame, text='Detect Drones',
                                          font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.gray_fg_color, hover_color=configuration.gray_hover_color,
                                          command=lambda: self.event_handler(Event.DETECT_DRONES))
        self.button_detect_drones.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.button_detect_vehicles = ctk.CTkButton(frame, text='Detect Vehicles', font=(configuration.main_font_style, configuration.main_font_size),
                                        fg_color=configuration.gray_fg_color, hover_color=configuration.gray_hover_color,
                                        command=lambda: self.event_handler(Event.DETECT_VEHICLES))
        self.button_detect_vehicles.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

    # Overlay Options
    def overlay_options(self, frame):
        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.overlay_options_display = ctk.CTkLabel(frame, text='---- Overlay Options ----',
                                               font=(configuration.main_font_style, configuration.main_font_size))
        self.overlay_options_display.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2,
                                     sticky='nsew')

        self.overlay_color_button = ctk.CTkButton(frame, text='Blue Overlay',
                                      font=(configuration.main_font_style, configuration.main_font_size),
                                      fg_color=configuration.blue_fg_color,
                                      hover_color=configuration.blue_hover_color,
                                      command=lambda: self.event_handler(Event.OVERLAY_COLOR_BLUE))
        self.overlay_color_button.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.overlay_threshold_button = ctk.CTkButton(frame, text='Overlay Threshold',
                                                  font=(configuration.main_font_style, configuration.main_font_size),
                                                  fg_color=configuration.bluelight_fg_color,
                                                  hover_color=configuration.bluelight_hover_color,
                                                  command=lambda: self.event_handler(Event.OVERLAY_THRESHOLD_WINDOW))
        self.overlay_threshold_button.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2,
                                       sticky='nsew')


    def template_button_frame_z(self, frame):

        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.button_1 = ctk.CTkButton(frame, text='Button', font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.gray_fg_color, hover_color=configuration.gray_hover_color,
                                          command=lambda: self.event_handler(Event.DUMMY_BUTTON))
        self.button_1.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.button_2 = ctk.CTkButton(frame, text='Button',
                                          font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.gray_fg_color, hover_color=configuration.gray_hover_color,
                                          command=lambda: self.event_handler(Event.DUMMY_BUTTON))
        self.button_2.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.button_3 = ctk.CTkButton(frame, text='Button', font=(configuration.main_font_style, configuration.main_font_size),
                                        fg_color=configuration.gray_fg_color, hover_color=configuration.gray_hover_color,
                                        command=lambda: self.event_handler(Event.DUMMY_BUTTON))
        self.button_3.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')


    # BUTTON TOGGLE STATES ------------------------
    def set_overlay_color_red(self):
        self.overlay_color_button.configure(text="Red Overlay",
                                            fg_color=configuration.red_fg_color,
                                            hover_color=configuration.red_hover_color,
                                            command=lambda: self.event_handler(Event.OVERLAY_COLOR_RED))

    def set_overlay_color_blue(self):
        self.overlay_color_button.configure(text="Blue Overlay",
                                            fg_color=configuration.blue_fg_color,
                                            hover_color=configuration.blue_hover_color,
                                            command=lambda: self.event_handler(Event.OVERLAY_COLOR_BLUE))

    def set_overlay_color_green(self):
        self.overlay_color_button.configure(text="Green Overlay",
                                            fg_color=configuration.green_fg_color,
                                            hover_color=configuration.green_hover_color,
                                            command=lambda: self.event_handler(Event.OVERLAY_COLOR_GREEN))

    # UPDATE METADATA FRAMES ------------------------





# ---------------------------------------------------
# RIGHT FRAME --------------------------------------
# ---------------------------------------------------

class Right_Frame(ctk.CTkFrame):
    def __init__(self, parent, event_handler):
        super().__init__(parent)
        self.event_handler = event_handler
        self.parent = parent

        self.papapi_connection_state = 0
        self.micfpga_connection_state = 0
        self.overlay_start_feed_state = 0

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

        self.template_bottom_buttons(top_frame)
        self.camera_settings_frame(middle_frame)
        self.settings_frame(bottom_frame)

    # FRAMES ---------------------------------------------

    def template_bottom_buttons(self, frame):
        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.video_feed_button = ctk.CTkButton(frame, text='Start Video Feed',
                                      font=(configuration.main_font_style, configuration.main_font_size),
                                      fg_color=configuration.green_fg_color,
                                      hover_color=configuration.green_hover_color,
                                      command=lambda: self.event_handler(Event.START_CAMERA))
        self.video_feed_button.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.papapi_hardware_connect_label = ctk.CTkLabel(frame, text='Papa Pi Disconnected',
                                                    font=(configuration.main_font_style, configuration.main_font_size),
                                                           text_color=configuration.red_fg_color)
        self.papapi_hardware_connect_label.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2,
                                          sticky='nsew')

        self.micfpga_hardware_connect_label = ctk.CTkLabel(frame, text='',
                                                    font=(configuration.main_font_style, configuration.main_font_size),
                                                           text_color=configuration.red_fg_color)
        self.micfpga_hardware_connect_label.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2,
                                          sticky='nsew')

    def camera_settings_frame(self, frame):

        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.capture_image_button = ctk.CTkButton(frame, text='Save Image', font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.green_fg_color, hover_color=configuration.green_hover_color,
                                          command=lambda: self.event_handler(Event.TAKE_PICTURE))
        self.capture_image_button.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.capture_video_button = ctk.CTkButton(frame, text='Rec Video',
                                          font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.bluelight_fg_color,
                                          hover_color=configuration.bluelight_hover_color,
                                          command=lambda: self.event_handler(Event.RECORD_VIDEO))
        self.capture_video_button.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')


        self.total_time_display = ctk.CTkLabel(frame, text='00:00',
                                               font=(configuration.main_font_style, configuration.main_font_size))
        self.total_time_display.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2,
                                     sticky='nsew')

    def template_button_frame_z(self, frame):

        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.button_1 = ctk.CTkButton(frame, text='Button', font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.gray_fg_color, hover_color=configuration.gray_hover_color,
                                          command=lambda: self.event_handler(Event.DUMMY_BUTTON))
        self.button_1.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.button_2 = ctk.CTkButton(frame, text='Button',
                                          font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.gray_fg_color, hover_color=configuration.gray_hover_color,
                                          command=lambda: self.event_handler(Event.DUMMY_BUTTON))
        self.button_2.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.button_3 = ctk.CTkButton(frame, text='Button', font=(configuration.main_font_style, configuration.main_font_size),
                                        fg_color=configuration.gray_fg_color, hover_color=configuration.gray_hover_color,
                                        command=lambda: self.event_handler(Event.DUMMY_BUTTON))
        self.button_3.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

    def settings_frame(self, frame):

        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        # frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.settings_button_1 = ctk.CTkButton(frame, text='Button', font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.gray_fg_color, hover_color=configuration.gray_hover_color,
                                          command=lambda: self.event_handler(Event.SETTINGS_BUTTON_1))
        self.settings_button_1.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')



        self.settings_button = ctk.CTkButton(frame, text='Settings', font=(configuration.main_font_style, configuration.main_font_size),
                                        fg_color=configuration.darkgray_fg_color, hover_color=configuration.darkgray_hover_color,
                                        command=lambda: self.event_handler(Event.SETTINGS))
        self.settings_button.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.exit_button = ctk.CTkButton(frame, text='EXIT',
                                         font=(configuration.main_font_style, configuration.main_font_size),
                                         fg_color=configuration.red_fg_color, hover_color=configuration.red_hover_color,
                                         command=self.parent.parent.close_application)
        self.exit_button.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

    # BUTTON TOGGLE STATES ------------------------

    def toggle_video_feed_button(self):
        if self.overlay_start_feed_state == 0:
            self.video_feed_button.configure(text="Stop Video Feed",
                                               fg_color=configuration.red_fg_color,
                                               hover_color=configuration.red_hover_color,
                                               command=lambda: self.event_handler(Event.STOP_CAMERA))
            self.overlay_start_feed_state += 1

        else:
            self.video_feed_button.configure(text="Start Video Feed",
                                        fg_color=configuration.green_fg_color,
                                        hover_color=configuration.green_hover_color,
                                        command=lambda: self.event_handler(Event.START_CAMERA))
            self.overlay_start_feed_state = 0

    def set_papapi_connected_label(self):
        self.papapi_hardware_connect_label.configure(text="Papa Pi Connected", text_color=configuration.green_fg_color)

    def set_papapi_disconnected_label(self):
        self.papapi_hardware_connect_label.configure(text="Papa Pi Disconnected", text_color=configuration.red_fg_color)
