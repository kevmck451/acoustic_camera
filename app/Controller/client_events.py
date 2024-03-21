import socket
import time

class Event_Sender_Client:
    def __init__(self, host='10.0.0.1', port=42069):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
        except Exception as e:
            print(f"Error connecting to the server: {e}")

    def send_data(self, data):
        try:
            self.socket.sendall(data.encode())
            print("Data sent")
        except socket.error as e:
            print(f"Error sending data: {e}")
            self.socket.close()  # Close the old connection
            self.connect()  # Re-establish the connection

    def close_connection(self):
        self.socket.close()
        print("Connection closed")

# To use the client
if __name__ == '__main__':
    client = Event_Sender_Client('127.0.0.1')

    try:
        while True:
            # Example: send data continuously or based on some condition
            data = input("Enter data to send (or type 'exit' to quit): ")
            if data.lower() == 'exit':
                break
            client.send_data(data)
            time.sleep(1)  # Add delay as needed
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        client.close_connection()
