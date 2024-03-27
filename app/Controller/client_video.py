

# First Draft

import threading
import socket
import queue



# ----------------------------------------------------
# Client Code
# ----------------------------------------------------
# RP using data/video for something

import numpy as np
import socket
import time
import cv2


class VideoClient:
    def __init__(self, host='0.0.0.0', port=56565, frame_callback=None, sock=None):
        self.host = host
        self.port = port
        self.gui = None
        self.current_frame = None
        self.stream_video = False
        self.i_loop = 0
        self.num_bytes = 0
        self.timer_speed = time.time()
        self.timer_print = time.time()

        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self):
        self.sock.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")
        video_sender_thread = threading.Thread(target=self.receive_video_data)
        # video_sender_thread = threading.Thread(target=video_sender.demo_overlay_stream)
        video_sender_thread.start()

    def set_gui(self, gui):
        self.gui = gui

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
                    self.current_frame = self.process_video_data(data)
                    data = b''  # Reset buffer for next frame

                    self.calculate_transfer_speed(self.current_frame.nbytes)

                    if self.gui is not None:

                        self.gui.Main_Frame.Center_Frame.update_frame(self.current_frame)


        except Exception as e:
            print(f"Error receiving video data: {e}")
        finally:
            self.close()

    def calculate_transfer_speed(self, frame_bytes):
        self.num_bytes += (frame_bytes / 1000000)
        if time.time() - self.timer_speed > 1:
            if time.time() - self.timer_print > 10:
                print(f'Streaming Video: {int(np.round(self.num_bytes))} MB/s')
                self.timer_print = time.time()
            self.num_bytes = 0
            self.timer_speed = time.time()


    def demo_overlay_stream(self):
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

                    self.calculate_transfer_speed(frame.nbytes)

                    cv2.imshow('Acoustic Camera Overlay', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        except Exception as e:
            print(f"Error receiving video data: {e}")
        except KeyboardInterrupt:
            print('Shutting Down')
            self.close()
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
    # client.receive_video_data()
    client.demo_overlay_stream()