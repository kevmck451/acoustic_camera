

import socket

class Video_Overlay_Sending:
    def __init__(self, host='10.0.0.1', port=55555):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data):
        self.sock.sendto(data, (self.host, self.port))

    def close(self):
        self.sock.close()