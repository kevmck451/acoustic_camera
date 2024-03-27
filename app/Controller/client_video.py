
import threading
import socket
import queue
import time


# ----------------------------------------------------
# Client Code
# ----------------------------------------------------
# RP using data/video for something


import socket
import cv2
import numpy as np

class VideoClient:
    def __init__(self, host='0.0.0.0', port=56565, sock=None):
        self.host = host
        self.port = port
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self):
        self.sock.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def receive_video_data(self):
        """
        Receive video data from the server.
        """
        data = b''
        try:
            while True:
                # Receive data in chunks
                chunk = self.sock.recv(4096)
                if not chunk:
                    break  # No more data
                data += chunk

                # Process received data if it's the end of a frame
                if self.is_end_of_frame(data):
                    frame = self.process_video_data(data)
                    data = b''  # Reset buffer for next frame

                    # Now `frame` contains the uncompressed image data
                    # which can be used for further processing
                    # For demonstration, we will just show the frame
                    cv2.imshow('Video Frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        except Exception as e:
            print(f"Error receiving video data: {e}")
        finally:
            self.close()

    @staticmethod
    def is_end_of_frame(data):
        """
        Check if the received data indicates the end of a video frame.
        This function assumes that the data ends with a specific marker or
        the length of data reaches a certain threshold (e.g., size of a compressed frame).
        Adjust the logic based on your actual data format and protocol.
        """
        # This is a placeholder function; you should implement the actual logic
        # For example, check for a JPEG end-of-file marker (0xFFD9) if using JPEG compression
        return data.endswith(b'\xff\xd9')  # JPEG EOF marker

    @ staticmethod
    def process_video_data(data):
        """
        Process the received video data.
        This function decodes the video data into image frames.
        """
        # Decode the image data
        frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        return frame

    def close(self):
        cv2.destroyAllWindows()
        self.sock.close()
        print("Connection closed")

if __name__ == "__main__":
    host = '10.0.0.1'  # Change to your server's IP address
    port = 56565        # Change to your server's port

    client = VideoClient(host, port)
    client.connect()
    client.receive_video_data()







# # 1st Draft
# class Video_Sender_Client:
#     def __init__(self, host='10.0.0.1', port=55555, name='Pi App Video'):
#         self.host = host
#         self.port = port
#         self.name = name
#         self.BUFFER_SIZE = 65536
#         self.connected = False
#         self.socket = None
#         self.connect_thread = threading.Thread(target=self.ensure_connection, daemon=True)
#         self.connect_thread.start()
#         self.connected = False
#         self.frame_queue = queue.Queue(maxsize=10)
#         self.receive_video_thread = None
#
#
#     def ensure_connection(self):
#         print('Attempting to Connect with Video Server')
#         while not self.connected:
#             print("Waiting for Video Connection...")
#             try:
#                 self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFFER_SIZE)
#                 self.socket.connect((self.host, self.port))
#                 handshake_message = f'{self.name}'
#                 self.socket.sendall(handshake_message.encode())
#                 response = self.socket.recv(1024)
#                 if not response.decode('utf-8') == 'ack': continue
#                 print(f"Connected to {self.host}:{self.port}")
#                 self.connected = True
#                 self.receive_video_thread = threading.Thread(target=self.get_video_stream, daemon=True)
#                 self.receive_video_thread.start()
#
#             except Exception as e:
#                 # print(f"Error connecting to the server: {e}")
#                 self.connected = False
#                 time.sleep(1)  # Retry after a delay
#
#
#     def send_data(self, data):
#         if self.connected:
#             try:
#                 self.socket.sendall(data.encode())
#                 print("Sending Start/Stop Command")
#             except socket.error as e:
#                 print(f"Error sending data: {e}")
#                 self.connected = False
#                 self.socket.close()
#         else:
#             print("Video Server Not Connected. Unable to send data.")
#
#
#     def get_video_stream(self):
#         while not self.connected:
#             print('Getting Video Frame')
#             frame = self.socket.recv(1024)
#             frame = frame.decode()
#             print(f'Frame: {frame}')
#             # if not self.frame_queue.full():
#             #     self.frame_queue.put(frame)
#
#
#     def close_connection(self):
#         self.connected = False
#         if self.socket:
#             self.socket.close()
#             print("Connection closed")
#
# # Usage example
# if __name__ == '__main__':
#     # for running mac to mac
#     # client = Event_Sender_Client('127.0.0.1', name='MacBook')
#     # for running papapi to mac
#     client = Video_Sender_Client()
#
#     while not client.connected:
#         # print("Waiting for connection...")
#         time.sleep(1)
#
#     print("Client connected, can send data now.")
#     while True:
#         command = input('Enter Command: ')
#         if command.lower() == 'exit': break
#         client.send_data(command)
#







