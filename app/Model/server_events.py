import socket

class Event_Listener_Server:
    def __init__(self, host='10.0.0.1', port=42069):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket):
        with client_socket:
            print('Client connected')
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}")
                # Process the data here

    def run(self):
        while True:
            client_socket, addr = self.socket.accept()
            print(f"Connection from {addr}")
            self.handle_client(client_socket)

# To run the server
if __name__ == '__main__':
    server = Event_Listener_Server('0.0.0.0')
    server.run()
