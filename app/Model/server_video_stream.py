
from dataclasses import dataclass
import threading
import socket
import time

class Video_Server:
    def __init__(self, host='10.0.0.1', port=55555):
        self.host = host
        self.port = port
        self.BUFFER_SIZE = 65536
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFFER_SIZE)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.running = True
        self.client_list = []
        self.hardware = None
        self.overlay = None
        self.video_server = None
        self.sending_video = False
        self.transmission_rate = 0.5

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
                print(message)
                if message == 'start':
                    # start stream thread
                    self.sending_video = True
                    video_stream_thread = threading.Thread(target=self.send_video_stream, args=(client_socket,), daemon=True)
                    video_stream_thread.start()

                elif message == 'stop':
                    # stop stream thread
                    self.sending_video = False


    def run(self):
        while self.running:
            client_socket, addr = self.socket.accept()
            print('client accepted')
            # time.sleep(0.1)
            name = client_socket.recv(1024).decode()

            # check if client name already exists and remove them
            print(self.client_list)
            for client_x in self.client_list:
                if client_x.name == name:
                    print('Duplicated Client Discovered and Removing')
                    self.client_list.remove(client_x)

            client = Client(name=name, socket=client_socket, ip_addr=addr[0], port=addr[1])
            self.client_list.append(client)
            print(f"Connection from {client.name} with address: {addr}")
            client_socket.sendall('ack'.encode())
            video_stream_feed = threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True)
            video_stream_feed.start()

    def stop(self):
        self.running = False


    def send_video_stream(self, client_socket):
        while self.sending_video:
            print(f'attempting to stream video to {client_socket}')
            # client_socket.sendall(self.overlay.total_overlay_compressed)
            client_socket.sendall('Testing'.encode())
            time.sleep(self.transmission_rate)



@dataclass
class Client:
    name: str
    socket: object
    ip_addr: str
    port: int




# To run the server
if __name__ == '__main__':
    server = Video_Server('0.0.0.0')
    run_thread = threading.Thread(target=server.run, daemon=True).start()

    while True:
        time.sleep(0.1)