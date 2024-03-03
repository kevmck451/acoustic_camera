
from PIL import Image, ImageTk
import threading
import queue
import cv2

class Camera:
    def __init__(self, frame_width=580, frame_height=580):
        self.frame_queue = queue.Queue(maxsize=10)
        self.frame_width = frame_width
        self.frame_height = frame_height
        # Example inputs for the square's position and color
        self.square_position = (100, 100)  # (x, y) position of the top-left corner
        self.square_size = 50  # Length of the square's side
        self.square_color = (0, 255, 0)  # Color of the square in BGR (green)
        threading.Thread(target=self.capture_frames, daemon=True).start()

    def overlay_square(self, frame, position, size, color):
        # Calculate bottom right corner of square from top left position and size
        top_left_corner = position
        bottom_right_corner = (position[0] + size, position[1] + size)
        # Draw the square on the frame
        cv2.rectangle(frame, top_left_corner, bottom_right_corner, color, -1)  # -1 fills the rectangle

    def capture_frames(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (self.frame_width, self.frame_height))
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

                # Overlay the square on the frame
                self.overlay_square(frame, self.square_position, self.square_size, self.square_color)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(image=frame)

                if not self.frame_queue.full():
                    self.frame_queue.put(frame)
            else:
                break

        cap.release()

# class Camera:
#     def __init__(self, frame_width=580, frame_height=580):
#         self.frame_queue = queue.Queue(maxsize=10)  # Adjust size as needed
#         self.frame_width = frame_width
#         self.frame_height = frame_height
#         threading.Thread(target=self.capture_frames, daemon=True).start()
#
#     def capture_frames(self):
#         # Placeholder for capturing frames and putting them in the queue
#         cap = cv2.VideoCapture(0)
#         while True:
#             ret, frame = cap.read()
#             if ret:
#                 # Resize the frame to the specified dimensions
#                 frame = cv2.resize(frame, (self.frame_width, self.frame_height))
#                 frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
#                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 frame = Image.fromarray(frame)
#                 frame = ImageTk.PhotoImage(image=frame)
#                 if not self.frame_queue.full():
#                     self.frame_queue.put(frame)
#             else:
#                 break
#
#         # When done, release the capture
#         cap.release()



