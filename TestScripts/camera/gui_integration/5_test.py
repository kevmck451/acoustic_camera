import cv2
import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

def update_frame():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    frame = ImageTk.PhotoImage(frame)
    video_label.configure(image=frame)
    video_label.image = frame
    video_label.after(10, update_frame)

cap = cv2.VideoCapture(0)  # Use 0 for the first webcam

root = ctk.CTk()  # This initializes your main CustomTkinter window
video_label = ctk.CTkLabel(root)  # Use CTkLabel for a CustomTkinter Label
video_label.pack()

update_frame()  # Start the frame update loop

root.mainloop()
