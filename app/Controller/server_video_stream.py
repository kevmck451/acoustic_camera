


import socket



# UDP Socket used for communicating to pi's camera
class Video_Overlay_Server:
    def __init__(self):
        self.host = '10.0.0.1'
        self.port = 55555
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the address and port
        self.sock.bind((self.host, self.port))

    def start_server(self):
        while True:
            data, addr = self.sock.recvfrom(1024)  # Buffer size is 1024 bytes

            # Process the data here (if necessary)