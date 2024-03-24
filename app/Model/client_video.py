

import socket
import time

class Video_Client:
    def __init__(self, host='10.0.0.13', port=55555):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data):
        self.sock.sendto(data, (self.host, self.port))

    def close(self):
        self.sock.close()





if __name__ == '__main__':
    video_client = Video_Client(host='127.0.0.1')

    while True:
        video_client.send_data('test')
        time.sleep(1)

