


import socket



# UDP Socket used for communicating to pi's camera
class Video_Overlay_Socket:
    def __init__(self):
        self.host = '10.0.0.1'
        self.port = 55555
        # Change the socket type to SOCK_DGRAM for UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_frame(self, frame):
        # Assume the frame is already encoded to bytes
        self.sock.sendto(frame, (self.host, self.port))