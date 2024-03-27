from app.View.Main_Window import Main_Window
from app.Controller.controller import Controller
from app.Controller.client_events import Event_Sender_Client
from app.Controller.client_video import VideoClient

if __name__ == "__main__":

    event_sender = Event_Sender_Client(name='Pi App Event')
    # event_sender = Event_Sender_Client(name='MacBook')

    video_sender = VideoClient('10.0.0.1')
    video_sender.connect()

    controller = Controller()
    gui = Main_Window(controller.handle_event)
    gui.set_video_sender(video_sender)

    controller.set_gui(gui)
    controller.set_event_sender(event_sender)


    gui.mainloop()

