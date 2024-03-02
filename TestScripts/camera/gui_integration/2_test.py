import tkinter as tk
from PIL import Image, ImageTk
from picamera import PiCamera
from io import BytesIO
import threading
import queue

frame_queue = queue.Queue(maxsize=1)

def capture_frames():
    with PiCamera() as camera:
        camera.rotation = 90
        # camera.resolution = (640, 480)
        camera.resolution = (720, 480)
        stream = BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            if not frame_queue.full():  # Don't block if the queue is full
                frame_queue.put(stream.read())
            stream.seek(0)
            stream.truncate()

def update_gui():
    try:
        frame_data = frame_queue.get_nowait()
        image = Image.open(BytesIO(frame_data))
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
    except queue.Empty:
        pass
    root.after(1, update_gui)

root = tk.Tk()
label = tk.Label(root)
label.pack()

threading.Thread(target=capture_frames, daemon=True).start()
update_gui()

root.mainloop()
