

from app.View.Main_Window import Main_Window
from app.Controller.controller import Controller
from app.Controller.client_events import Event_Sender_Client
from app.Controller.client_video import VideoClient


import threading

if __name__ == "__main__":

    event_sender = Event_Sender_Client(name='Pi App Event')

    video_sender = VideoClient('10.0.0.1')
    video_sender.connect()
    # video_sender_thread = threading.Thread(target=video_sender.receive_video_data)
    video_sender_thread = threading.Thread(target=video_sender.demo_overlay_stream)
    video_sender_thread.start()

    controller = Controller()

    gui = Main_Window(controller.handle_event)

    controller.set_gui(gui)
    controller.set_event_sender(event_sender)

    gui.mainloop()

