import socket
import threading
import time

class Event_Sender_Client:
    def __init__(self, host='10.0.0.1', port=42069, name='Pi App'):
        self.host = host
        self.port = port
        self.name = name
        self.connected = False
        self.socket = None
        self.connect_thread = threading.Thread(target=self.ensure_connection, daemon=True)
        self.connect_thread.start()
        self.heartbeat_thread = None
        self.connected = False
        self.heartbeat_attempt = 0

    def ensure_connection(self):
        print('Attempting to Connect with Pi Hardware')
        while not self.connected:
            print("Waiting for connection...")
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                handshake_message = f'{self.name}'
                self.socket.sendall(handshake_message.encode())
                response = self.socket.recv(1024)
                if not response.decode('utf-8') == 'ack': continue
                print(f"Connected to {self.host}:{self.port}")
                self.heartbeat_thread = threading.Thread(target=self.heartbeat, daemon=True)
                self.heartbeat_thread.start()
                self.connected = True

            except Exception as e:
                print(f"Error connecting to the server: {e}")
                time.sleep(1)  # Retry after a delay

    def heartbeat(self):
        print('heartbeat')
        wait_time = 1
        burst_time = 0.1

        while self.connected == True:

            try:
                self.socket.sendall('heartbeat'.encode())
                time.sleep(burst_time)
                self.socket.sendall('heartbeat'.encode())
                time.sleep(burst_time)
                self.socket.sendall('heartbeat'.encode())
                self.heartbeat_attempt = 0
            except socket.error as e:
                self.heartbeat_attempt += 1

            if self.heartbeat_attempt == 5:
                self.connected = False
                self.connect_thread = threading.Thread(target=self.ensure_connection, daemon=True)
                self.connect_thread.start()

            time.sleep(wait_time)

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
        # print("Waiting for connection...")
        time.sleep(1)

    print("Client connected, can send data now.")
    while True:
        command = input('Enter Command: ')
        if command.lower() == 'exit': break
        client.send_data(command)
