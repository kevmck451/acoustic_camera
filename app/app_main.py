from app.View.Main_Window import Main_Window
from app.Controller.controller import Controller
from app.Controller.client_events import Event_Sender_Client
from app.Controller.server_video_stream import Video_Overlay_Server

if __name__ == "__main__":

    # event_sender = Event_Sender_Client(name='Pi App')
    event_sender = Event_Sender_Client(name='MacBook')

    controller = Controller()
    gui = Main_Window(controller.handle_event)
    video_server = Video_Overlay_Server()
    gui.set_server(video_server)

    controller.set_gui(gui)
    controller.set_event_sender(event_sender)

    gui.mainloop()

