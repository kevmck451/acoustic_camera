
import threading
import socket
import queue
import time

class Video_Sender_Client:
    def __init__(self, host='10.0.0.1', port=55555, name='Pi App'):
        self.host = host
        self.port = port
        self.name = name
        self.BUFFER_SIZE = 65536
        self.connected = False
        self.socket = None
        self.connect_thread = threading.Thread(target=self.ensure_connection, daemon=True)
        self.connect_thread.start()
        self.connected = False
        self.frame_queue = queue.Queue(maxsize=10)
        self.receive_video_thread = None


    def ensure_connection(self):
        print('Attempting to Connect with Video Server')
        while not self.connected:
            print("Waiting for Video Connection...")
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFFER_SIZE)
                self.socket.connect((self.host, self.port))
                handshake_message = f'{self.name}'
                self.socket.sendall(handshake_message.encode())
                response = self.socket.recv(1024)
                if not response.decode('utf-8') == 'ack': continue
                print(f"Connected to {self.host}:{self.port}")
                self.connected = True
                self.receive_video_thread = threading.Thread(target=self.video_stream_data, daemon=True)
                self.receive_video_thread.start()

            except Exception as e:
                # print(f"Error connecting to the server: {e}")
                self.connected = False
                time.sleep(1)  # Retry after a delay


    def send_data(self, data):
        if self.connected:
            try:
                self.socket.sendall(data.encode())
                print("Sending Start/Stop Command")
            except socket.error as e:
                print(f"Error sending data: {e}")
                self.connected = False
                self.socket.close()
        else:
            print("Video Server Not Connected. Unable to send data.")


    def video_stream_data(self):
        print('Streaming Video')
        while not self.connected:
            frame = self.socket.recv(1024)
            frame = frame.decode()
            print(frame)
            # if not self.frame_queue.full():
            #     self.frame_queue.put(frame)


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
    client = Video_Sender_Client()

    while not client.connected:
        # print("Waiting for connection...")
        time.sleep(1)

    print("Client connected, can send data now.")
    while True:
        command = input('Enter Command: ')
        if command.lower() == 'exit': break
        client.send_data(command)








