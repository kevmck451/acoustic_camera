
import numpy as np
import socket
import time

class Video_Client:
    def __init__(self, host='127.0.0.1', port=55555):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data):
        print(f'TX Data Type: {type(data)}')
        # self.sock.sendto(data.encode(), (self.host, self.port))
        self.sock.sendto(data.tobytes(), (self.host, self.port))

    def close(self):
        self.sock.close()

    @staticmethod
    def test():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto('Hello, server!'.encode(), ('127.0.0.1', 55555))
        sock.close()


if __name__ == '__main__':
    video_client = Video_Client()

    total_overlay = np.zeros((10, 10, 3))

    while True:
        print('sending')
        video_client.send_data(total_overlay)
        # video_client.test()
        time.sleep(1)












