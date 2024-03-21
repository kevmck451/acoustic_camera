


import socket


# TCP Socket to give commands to PapaPi
class Event_Listener_Socket:
    def __init__(self):
        self.host = '10.0.0.1'
        self.port = 42069
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_EL_connection(self):
        self.sock.connect((self.host, self.port))

    def send_event(self, event):
        # Convert the enum to a string and send it over the socket
        event_str = event.name
        self.sock.sendall(event_str.encode('utf-8'))

    def receive_event(self):
        # Receive a string from the socket and convert it back to an enum
        data = self.sock.recv(1024)  # Adjust buffer size as needed
        event_str = data.decode('utf-8')
        return event_str  # No conversion back to Enum, assuming that's handled elsewhere
