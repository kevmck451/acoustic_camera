
from PIL import Image, ImageTk
import threading
import queue
import cv2




# class Camera:
#     def __init__(self):
#         self.frame_queue = queue.Queue(maxsize=10)  # Adjust size as needed
#         threading.Thread(target=self.capture_frames, daemon=True).start()
#
#     def capture_frames(self):
#         # Placeholder for capturing frames and putting them in the queue
#         cap = cv2.VideoCapture(0)
#         while True:
#             ret, frame = cap.read()
#             if ret:
#                 frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
#                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 frame = Image.fromarray(frame)
#                 frame = ImageTk.PhotoImage(image=frame)
#                 if not self.frame_queue.full():
#                     self.frame_queue.put(frame)
#             else:
#                 break


class Camera:
    def __init__(self, frame_width=600, frame_height=600):
        self.frame_queue = queue.Queue(maxsize=10)  # Adjust size as needed
        self.frame_width = frame_width
        self.frame_height = frame_height
        threading.Thread(target=self.capture_frames, daemon=True).start()

    def capture_frames(self):
        # Placeholder for capturing frames and putting them in the queue
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                # Resize the frame to the specified dimensions
                frame = cv2.resize(frame, (self.frame_width, self.frame_height))

                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(image=frame)
                if not self.frame_queue.full():
                    self.frame_queue.put(frame)
            else:
                break

        # When done, release the capture
        cap.release()