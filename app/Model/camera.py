
from PIL import Image, ImageTk
import threading
import queue
import cv2



class Camera:
    def __init__(self, frame_width=580, frame_height=580):
        self.frame_queue = queue.Queue(maxsize=10)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.squares = []  # Initialize an empty list for squares
        threading.Thread(target=self.capture_frames, daemon=True).start()

    def add_square(self, position, size, color, transparency):
        self.squares.append({
            'position': position,
            'size': size,
            'color': color,
            'transparency': transparency
        })

    def clear_squares(self):
        self.squares.clear()  # Clears the list of squares

    def overlay_squares(self, frame):
        for square in self.squares:
            overlay = frame.copy()
            # Ensure top_left_corner and bottom_right_corner are tuples of integers
            top_left_corner = (int(square['position'][0]), int(square['position'][1]))
            bottom_right_corner = (int(top_left_corner[0] + square['size']), int(top_left_corner[1] + square['size']))

            # Use the corrected points to draw the rectangle
            cv2.rectangle(overlay, top_left_corner, bottom_right_corner, square['color'], -1)
            cv2.addWeighted(overlay, square['transparency'], frame, 1 - square['transparency'], 0, frame)

    def capture_frames(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (self.frame_width, self.frame_height))
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

                # Overlay squares on the frame
                self.overlay_squares(frame)

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
#         self.frame_queue = queue.Queue(maxsize=10)
#         self.frame_width = frame_width
#         self.frame_height = frame_height
#         # Example inputs for the square's position and color
#         self.square_position = (100, 100)  # (x, y) position of the top-left corner
#         self.square_size = 50  # Length of the square's side
#         self.square_color = (0, 100, 200)  # Color of the square in BGR (green)
#         self.square_transparency = 0  # Transparency of the square
#         threading.Thread(target=self.capture_frames, daemon=True).start()
#
#     def overlay_square(self, frame, position, size, color, transparency):
#         overlay = frame.copy()
#         top_left_corner = position
#         bottom_right_corner = (position[0] + size, position[1] + size)
#         cv2.rectangle(overlay, top_left_corner, bottom_right_corner, color, -1)
#
#         # Blend the original frame and the overlay with the square
#         cv2.addWeighted(overlay, transparency, frame, 1 - transparency, 0, frame)
#
#     def capture_frames(self):
#         cap = cv2.VideoCapture(0)
#         while True:
#             ret, frame = cap.read()
#             if ret:
#                 frame = cv2.resize(frame, (self.frame_width, self.frame_height))
#                 frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
#
#                 # Overlay the square on the frame
#                 self.overlay_square(frame, self.square_position, self.square_size, self.square_color, self.square_transparency)
#
#                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 frame = Image.fromarray(frame)
#                 frame = ImageTk.PhotoImage(image=frame)
#
#                 if not self.frame_queue.full():
#                     self.frame_queue.put(frame)
#             else:
#                 break
#
#         cap.release()





