
from dataclasses import dataclass
import threading
import socket
import time


# ----------------------------------------------------
# Server Code
# ----------------------------------------------------
# FPGA / Mics giving data | RP / Video giving data

class Video_Server:
    def __init__(self, host='0.0.0.0', port=56565):
        self.host = host
        self.port = port
        print(f"listening at IP {self.host} port {self.port}")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

        self.video_hw = None
        self.send_video_stream = False  # Initially set to False

    def run(self):
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"client accepted from {address}")
            # Handle each client connection in a separate thread
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        try:
            while self.send_video_stream:
                data_bytes = self.video_hw.get_data()
                if data_bytes:
                    client_socket.sendall(data_bytes)
        except Exception as e:
            print(f"Error during video capture: {e}")
        finally:
            client_socket.close()

    # Additional methods for start and stop commands
    def start_streaming(self):
        self.send_video_stream = True

    def stop_streaming(self):
        self.send_video_stream = False


    def set_video_hw(self, video_hw):
        self.video_hw = video_hw

    def stop(self):
        self.server_socket.close()

# To run the server
if __name__ == '__main__':
    server = Video_Server('0.0.0.0')
    server.send_video_stream = True
    run_thread = threading.Thread(target=server.run, daemon=True).start()

    while True:
        time.sleep(0.1)






# First Draft

# from dataclasses import dataclass
# import threading
# import socket
# import time
#

# ----------------------------------------------------
# Server Code
# ----------------------------------------------------
# FPGA / Mics giving data | RP / Video giving data

# class Video_Server:
#     def __init__(self, host='0.0.0.0'):
#         self.host = host # self._get_ip()
#         self.port = 56565
#         print(f"listening at IP {self.host} port {self.port}")
#
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.bind((self.host, self.port))
#         self.server_socket.listen(1)
#
#         self.video_hw = None
#         self.send_video_stream = True
#
#
#     @staticmethod
#     def _get_ip():
#         # https://stackoverflow.com/a/28950776
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.settimeout(0)
#         try:
#             # doesn't even have to be reachable
#             s.connect(('10.254.254.254', 1))
#             IP = s.getsockname()[0]
#         except Exception:
#             IP = '127.0.0.1'
#         finally:
#             s.close()
#         return IP
#
#
#     def run(self):
#         try:
#             while True:
#                 (client_socket, address) = self.server_socket.accept()
#                 try:
#                     self.capture(client_socket)
#                     print("client said goodbye")
#                 except (ConnectionResetError, ConnectionAbortedError,
#                         BrokenPipeError):
#                     print("client left rudely")
#                 finally:
#                     client_socket.close()
#         finally:
#             self.server_socket.close()
#
#
#     def set_video_hw(self, video_hw):
#         self.video_hw = video_hw
#
#
#     def capture(self, sock):
#         print("Video Stream is Ready!")
#
#         while True:
#             try:
#                 if self.send_video_stream:
#                     data_bytes = self.video_hw.get_data()
#                     if not data_bytes:
#                         print("No data received, waiting...")
#                         time.sleep(0.1)
#                         continue
#
#                     print(f"Sending {len(data_bytes)} bytes of video data")
#
#                     # Send the data in chunks to the client
#                     bytes_sent = 0
#                     while bytes_sent < len(data_bytes):
#                         sent = sock.send(data_bytes[bytes_sent:bytes_sent + 4096])
#                         if sent == 0:
#                             print("Connection probably broken")
#                             return
#                         bytes_sent += sent
#
#             except Exception as e:
#                 print(f"Error during video capture: {e}")
#                 break
#
#             time.sleep(0.1)  # Give some delay to prevent overloading the network
#
#         print("Video capture ended")
#
#
#     def stop(self):
#         self.server_socket.close()
#
# # To run the server
# if __name__ == '__main__':
#     server = Video_Server('0.0.0.0')
#     server.send_video_stream = True
#     run_thread = threading.Thread(target=server.run, daemon=True).start()
#
#     while True:
#         time.sleep(0.1)