
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

        print(f"Server listening on {self.host}:{self.port}")
        self.run_thread = threading.Thread(target=self.run, daemon=True).start()

    def set_hardware(self, hardware, overlay):
        self.hardware = hardware
        self.overlay = overlay

    def handle_client(self, client_socket):
        with client_socket:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode().split('=')
                command = message[0]
                value = message[1]
                print(f"Received: {command} = {value}")

                if command == 'camera_color':
                    if value: self.hardware.camera_hardware.set_color(True)
                    else: self.hardware.camera_hardware.set_color(False)
                elif command == 'mic_rms_threshold':
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

    def run(self):
        while self.running:
            client_socket, addr = self.socket.accept()
            time.sleep(0.1)
            name = client_socket.recv(1024).decode()
            client = Client(name=name, socket=client_socket, ip_addr=addr[0], port=addr[1])
            self.client_list.append(client)
            print(f"Connection from {client.name} with address: {addr}")
            client_socket.sendall('ack'.encode())
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def stop(self):
        self.running = False




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
