

import socket

class Video_Client:
    def __init__(self, host='10.0.0.13', port=55555):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data):
        self.sock.sendto(data, (self.host, self.port))

    def close(self):
        self.sock.close()







