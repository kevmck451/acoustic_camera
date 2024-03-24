

import threading
import socket
import time


# UDP Socket used for communicating to pi's camera
class Video_Overlay_Server:
    def __init__(self, host='10.0.0.13', port=55555):
        self.host = host
        self.port = port
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the address and port
        self.sock.bind((self.host, self.port))

    def start_server(self):
        while True:
            data, addr = self.sock.recvfrom(1024)  # Buffer size is 1024 bytes
            print(data)


if __name__ == '__main__':
    # for running mac to mac
    # client = Event_Sender_Client('127.0.0.1', name='MacBook')
    # for running papapi to mac
    server = Video_Overlay_Server()
    server_thread = threading.Thread(target=server.start_server(), daemon=True)

    while True:
        time.sleep(1)

