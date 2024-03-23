
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

        print(f"Server listening on {self.host}:{self.port}")
        self.run_thread = threading.Thread(target=self.run, daemon=True).start()

    @staticmethod
    def handle_client(client_socket):
        with client_socket:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}")
                # Process the data here

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
