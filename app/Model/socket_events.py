


import socket


# TCP Socket to give commands to PapaPi
class Event_Listener_Socket:
    def __init__(self, host='10.0.0.1', port=42069):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))  # Bind the socket to the address and port
        self.sock.listen(5)  # Start listening for incoming connections

    def accept_connection(self):
        # This method will block until a connection is established
        client_socket, client_address = self.sock.accept()
        print(f"Connection established with {client_address}")
        return client_socket, client_address

    def receive_event(self, client_socket):
        data = client_socket.recv(1024)  # Adjust buffer size as needed
        if data:
            event_str = data.decode('utf-8')
            return event_str  # Assuming conversion back to Enum is handled elsewhere

