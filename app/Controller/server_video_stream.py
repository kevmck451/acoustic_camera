
import numpy as np
import threading
import socket
import time
import cv2

# UDP Socket used for communicating to pi's camera
class Video_Overlay_Server:
    def __init__(self, host='0.0.0.0', port=55555):
        self.host = host
        self.port = port
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the address and port
        self.sock.bind((self.host, self.port))
        self.decompressed_image = None
        self.running = False
        # self.run()

    def start_server(self):
        print('Server Running')
        while self.running:
            data, addr = self.sock.recvfrom(1024)  # Use the maximum safe UDP packet size 65507
            print(f'RX Data Type: {type(data)}')
            print(data.decode())
            # Attempt to decode the received bytes as an image
            # image_data = np.frombuffer(data, dtype=np.uint8)
            # self.decompressed_image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    def run(self):
        self.running = True
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()



def test():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 55555))
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received from {addr}: {data.decode()}")

if __name__ == '__main__':

    # Test
    # server_thread = threading.Thread(target=test, daemon=True)
    # server_thread.start()

    server = Video_Overlay_Server()
    server_thread = threading.Thread(target=server.start_server, daemon=True)
    server_thread.start()

    while True:
        time.sleep(1)


