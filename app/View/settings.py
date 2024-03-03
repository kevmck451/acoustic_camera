from tkinter import PhotoImage
import customtkinter as ctk
import tkinter as tk
import numpy as np
import warnings

import app.View.configuration as configuration
from app.Controller.events import Event



# Settings Window
class Settings_Window(ctk.CTk):
    def __init__(self, event_handler):
        super().__init__()
        ctk.set_appearance_mode("light")
        # Computer Icon

        # Main Setup ------------------------------------------------------------
        self.title(configuration.settings_window_title)

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (configuration.settings_window_width / 2))
        center_y = int((screen_height / 2) - (configuration.settings_window_height / 2))
        self.geometry(f'{configuration.settings_window_width}x{configuration.settings_window_height}+{center_x}+{center_y}')
        self.minsize(configuration.settings_min_window_width, configuration.settings_min_window_height)


        self.Main_Frame = Settings_Frame(self, event_handler)
        self.columnconfigure(0, weight=1)  # Left column with 2/3 of the spac
        self.rowconfigure(0, weight=1)  # Left column with 2/3 of the spac
        self.Main_Frame.grid(row=0, column=0, sticky='nsew')  # Left frame in column 0

        # Ending Procedures
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Perform any cleanup or process termination steps here
        # For example, safely terminate any running threads, save state, release resources, etc.
        # print("Performing cleanup before exiting...")  # Replace this with actual cleanup code

        # End the application
        self.destroy()


class Settings_Frame(ctk.CTkFrame):
    def __init__(self, parent, event_handler):
        super().__init__(parent)

        self.event_handler = event_handler

        # Main Frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)  # Configure the column to expand
        self.grid_rowconfigure(0, weight=1)  # Configure the column to expand

        self.setting_frames(main_frame)

    def setting_frames(self, frame):
        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_rowconfigure(3, weight=1)  # Row for the load button
        frame.grid_rowconfigure(4, weight=1)  # Row for the load button
        frame.grid_rowconfigure(5, weight=1)  # Row for the load button
        frame.grid_rowconfigure(6, weight=1)  # Row for the load button
        frame.grid_rowconfigure(7, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column



