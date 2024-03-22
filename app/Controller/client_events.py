import socket
import threading
import time

class Event_Sender_Client:
    def __init__(self, host='10.0.0.1', port=42069, name='Papa Pi'):
        self.host = host
        self.port = port
        self.name = name
        self.connected = False
        self.socket = None
        self.connect_thread = threading.Thread(target=self.ensure_connection, daemon=True)
        self.connect_thread.start()

    def ensure_connection(self):
        while not self.connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                handshake_message = f'{self.name}'
                self.socket.sendall(handshake_message.encode())

                # Attempt to receive a response within the timeout period
                response = self.socket.recv(1024)
                if not response.decode('utf-8') == 'ack': continue
                self.connected = True
                print(f"Connected to {self.host}:{self.port}")


            except Exception as e:
                print(f"Error connecting to the server: {e}")
                time.sleep(1)  # Retry after a delay

    def send_data(self, data):
        if self.connected:
            try:
                self.socket.sendall(data.encode())
                print("Data sent")
            except socket.error as e:
                print(f"Error sending data: {e}")
                self.connected = False
                self.socket.close()
        else:
            print("Not connected. Unable to send data.")

    def close_connection(self):
        self.connected = False
        if self.socket:
            self.socket.close()
            print("Connection closed")

# Usage example
if __name__ == '__main__':
    # for running mac to mac
    # client = Event_Sender_Client('127.0.0.1', name='MacBook')
    # for running papapi to mac
    client = Event_Sender_Client(name='MacBook')

    while not client.connected:
        print("Waiting for connection...")
        time.sleep(1)

    print("Client connected, can send data now.")
    while True:
        command = input('Enter Command: ')
        if command.lower() == 'exit': break
        client.send_data(command)
