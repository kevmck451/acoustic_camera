

from dataclasses import dataclass
import threading
import socket
import time

class Event_Server:
    def __init__(self, host='10.0.0.1', port=42069):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.running = True
        self.client_list = []
        self.hardware = None
        self.overlay = None
        self.video_server = None

        print(f"Server listening on {self.host}:{self.port}")

    def set_hardware(self, hardware, overlay):
        self.hardware = hardware
        self.overlay = overlay

    def set_video_server(self, video_server):
        self.video_server = video_server

    def handle_client(self, client_socket):
        with client_socket:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = data.decode()
                if 'heartbeat' in message:
                    pass

                elif '=' in message:
                    command_message = message.split('=')
                    command = command_message[0]
                    value = command_message[1]
                    print(f"Received: {command} = {value}")
                    self.event_commands(command, value)

                elif message == 'fpga_status':
                    print('Feature in Progress')

                else: print(message)

    def run(self):
        while self.running:
            client_socket, addr = self.socket.accept()
            print('client accepted')
            time.sleep(0.1)
            name = client_socket.recv(1024).decode()

            # check if client name already exists and remove them
            for client_x in self.client_list:
                if client_x.name == name:
                    self.client_list.remove(client_x)

            client = Client(name=name, socket=client_socket, ip_addr=addr[0], port=addr[1])
            self.client_list.append(client)
            print(f"Connection from {client.name} with address: {addr}")
            client_socket.sendall('ack'.encode())
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def stop(self):
        self.running = False

    def event_commands(self, command, value):
        if command == 'mic_rms_threshold':
            self.overlay.rms_threshold = value
        elif command == 'mic_rms_max':
            self.overlay.rms_max = value
        elif command == 'mic_overlay_color':
            # BGR 0, 1, 2
            if value == 'red':
                self.overlay.audio_overlay_color = 2
            elif value == 'green':
                self.overlay.audio_overlay_color = 1
            elif value == 'blue':
                self.overlay.audio_overlay_color = 0
        elif command == 'video_stream':
            if value == 'True':
                self.video_server.start_streaming()
            elif value == 'False':
                self.video_server.stop_streaming()


@dataclass
class Client:
    name: str
    socket: object
    ip_addr: str
    port: int




# To run the server
if __name__ == '__main__':
    server = Event_Server('0.0.0.0')
    server.run()
