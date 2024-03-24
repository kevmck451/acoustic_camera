
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
        self.running = True

    def start_server(self):
        print('Server Running')
        while self.running:
            data, addr = self.sock.recvfrom(65507)  # Use the maximum safe UDP packet size
            if not data:
                continue
            print(type(data))
            # Attempt to decode the received bytes as an image
            image_data = np.frombuffer(data, dtype=np.uint8)
            decompressed_image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        #     if decompressed_image is not None:
        #         cv2.imshow('Compressed Overlay', decompressed_image)
        #         if cv2.waitKey(1) & 0xFF == ord('q'):
        #             break
        #
        # cv2.destroyAllWindows()



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

