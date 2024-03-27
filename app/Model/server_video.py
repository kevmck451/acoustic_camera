
from dataclasses import dataclass
import threading
import socket
import time


# ----------------------------------------------------
# Server Code
# ----------------------------------------------------
# FPGA / Mics giving data | RP / Video giving data

class Video_Server:
    def __init__(self, host='0.0.0.0'):
        self.host = host # self._get_ip()
        self.port = 56565
        print(f"listening at IP {self.host} port {self.port}")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

        self.video_hw = None
        self.send_video_stream = False


    @staticmethod
    def _get_ip():
        # https://stackoverflow.com/a/28950776
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP


    def run(self):
        try:
            while True:
                (client_socket, address) = self.server_socket.accept()
                try:
                    self.capture(client_socket)
                    print("client said goodbye")
                except (ConnectionResetError, ConnectionAbortedError,
                        BrokenPipeError):
                    print("client left rudely")
                finally:
                    client_socket.close()
        finally:
            self.server_socket.close()


    def set_video_hw(self, video_hw):
        self.video_hw = video_hw


    def capture(self, sock):
        print("Video capture is starting!")

        while True:
            try:
                if self.send_video_stream:
                    data_bytes = self.video_hw.get_data()
                    if not data_bytes:
                        print("No data received, waiting...")
                        time.sleep(0.1)
                        continue

                    print(f"Sending {len(data_bytes)} bytes of video data")

                    # Send the data in chunks to the client
                    bytes_sent = 0
                    while bytes_sent < len(data_bytes):
                        sent = sock.send(data_bytes[bytes_sent:bytes_sent + 4096])
                        if sent == 0:
                            print("Connection probably broken")
                            return
                        bytes_sent += sent

            except Exception as e:
                print(f"Error during video capture: {e}")
                break

            time.sleep(0.1)  # Give some delay to prevent overloading the network

        print("Video capture ended")


    def stop(self):
        self.server_socket.close()

# To run the server
if __name__ == '__main__':
    server = Video_Server('0.0.0.0')
    run_thread = threading.Thread(target=server.run, daemon=True).start()

    while True:
        time.sleep(0.1)




# 1st draft
# class Video_Server:
#     def __init__(self, host='10.0.0.1', port=55555):
#         self.host = host
#         self.port = port
#         self.BUFFER_SIZE = 65536
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFFER_SIZE)
#         self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.socket.bind((self.host, self.port))
#         self.socket.listen()
#         self.running = True
#         self.client_list = []
#         self.overlay = None
#         self.sending_video = False
#         self.transmission_rate = 0.5
#
#         print(f"Server listening on {self.host}:{self.port}")
#
#     def set_hardware(self, overlay):
#         self.overlay = overlay
#
#     def handle_client(self, client_socket):
#         # print(f'Handing Client: {client_socket}')
#         with client_socket:
#             while True:
#                 data = client_socket.recv(1024)
#                 if not data:
#                     break
#                 message = data.decode()
#                 print(f'Data Received: {message}')
#                 if message == 'start':
#                     # start stream thread
#                     self.sending_video = True
#                     video_stream_thread = threading.Thread(target=self.send_video_stream, args=(client_socket,), daemon=True)
#                     video_stream_thread.start()
#
#                 elif message == 'stop':
#                     # stop stream thread
#                     self.sending_video = False
#
#     def run(self):
#         while True:
#             client_socket, addr = self.socket.accept()
#             print('client accepted')
#             # time.sleep(0.1)
#             name = client_socket.recv(1024).decode()
#             # check if client name already exists and remove them
#             for client_x in self.client_list:
#                 if client_x.name == name:
#                     print('Duplicated Client Discovered and Removing')
#                     self.client_list.remove(client_x)
#
#             client = Client(name=name, socket=client_socket, ip_addr=addr[0], port=addr[1])
#             self.client_list.append(client)
#
#             print(f"Connection from {client.name} with address: {addr}")
#             # print(f'Client List: {self.client_list}')
#             client_socket.sendall('ack'.encode())
#             client_handle_thread = threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True)
#             client_handle_thread.start()
#
#     def stop(self):
#         self.running = False
#
#
#     def send_video_stream(self, client_socket):
#         print('send video stream function')
#         while self.sending_video:
#             print(f'attempting to stream video to {client_socket}')
#             client_socket.sendall('Testing'.encode())
#
#             # client_socket.sendall(self.overlay.total_overlay_compressed)
#             time.sleep(self.transmission_rate)
#
#
#
# @dataclass
# class Client:
#     name: str
#     socket: object
#     ip_addr: str
#     port: int
#
#
#
#
# # To run the server
# if __name__ == '__main__':
#     server = Video_Server('0.0.0.0')
#     run_thread = threading.Thread(target=server.run, daemon=True).start()
#
#     while True:
#         time.sleep(0.1)


