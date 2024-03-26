

import numpy as np
import socket
import time


# ----------------------------------------------------
# Server Code
# ----------------------------------------------------
# FPGA / Mics giving data | RP / Video giving data

class Video_Server:
    def __init__(self):
        self.host = self._get_ip()
        self.port = 56565
        print(f"listening at IP {self.host} port {self.port}")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", self.port))
        server_socket.listen(1)

        self.video_hw = None

        try:
            while True:
                (client_socket, address) = server_socket.accept()
                try:
                    self.capture(client_socket)
                    print("client said goodbye")
                except (ConnectionResetError, ConnectionAbortedError,
                        BrokenPipeError):
                    print("client left rudely")
                finally:
                    client_socket.close()
        finally:
            server_socket.close()

    @staticmethod
    def _get_ip(self):
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

    def set_video_hw(self, video_hw):
        self.video_hw = video_hw


    def capture(self, sock):
        print("Video capture is starting!")

        while True:
            try:
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


# ----------------------------------------------------
# Client Code
# ----------------------------------------------------
# RP using data/video for something






if __name__ == "__main__":

    mode = input('Are you s or c? ')

    if mode == 's':
        server()
    else: client()

