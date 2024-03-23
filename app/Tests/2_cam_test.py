# import cv2
# import threading
#
# class BufferlessVideoCapture:
#     def __init__(self, camera_index=0):
#         self.cap = cv2.VideoCapture(camera_index)
#         self.lock = threading.Lock()
#         self.latest_frame = None
#         threading.Thread(target=self._update_frame, daemon=True).start()
#
#     def _update_frame(self):
#         while True:
#             ret, frame = self.cap.read()
#             if ret:
#                 with self.lock:
#                     self.latest_frame = frame
#
#     def read(self):
#         with self.lock:
#             return self.latest_frame
#
#     def release(self):
#         self.cap.release()
#
# def view_camera(camera_instance):
#     cv2.namedWindow('Camera Feed', cv2.WINDOW_AUTOSIZE)
#     while True:
#         frame = camera_instance.read()
#         if frame is not None:
#             cv2.imshow('Camera Feed', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#     camera_instance.release()
#     cv2.destroyAllWindows()
#
# if __name__ == "__main__":
#     camera = BufferlessVideoCapture()
#     view_camera(camera)


import cv2
import threading
import time

class BufferlessVideoCapture:
    def __init__(self, camera_index=0, resolution=(640, 480), frame_rate=30, color=True, skip_frames=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.cap.set(cv2.CAP_PROP_FPS, frame_rate)
        self.color = color
        self.skip_frames = skip_frames
        self.frame_count = 0
        self.lock = threading.Lock()
        self.latest_frame = None
        threading.Thread(target=self._update_frame, daemon=True).start()

    def _update_frame(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                self.frame_count += 1
                if self.frame_count <= self.skip_frames:
                    continue  # Skip this frame
                self.frame_count = 0  # Reset frame count after skipping

                if not self.color:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                with self.lock:
                    self.latest_frame = frame
            else:
                time.sleep(0.01)  # Relax the cycle if no frame is captured

    def read(self):
        with self.lock:
            return self.latest_frame

    def release(self):
        self.cap.release()

def view_camera(camera_instance):
    cv2.namedWindow('Camera Feed', cv2.WINDOW_AUTOSIZE)
    while True:
        frame = camera_instance.read()
        if frame is not None:
            if len(frame.shape) == 2:  # Check if the frame is in grayscale
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            cv2.imshow('Camera Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    camera_instance.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera = BufferlessVideoCapture(
        camera_index=0,
        resolution=(640, 480),
        frame_rate=20,
        color=True,  # Change to True for color
        skip_frames=0  # Increase to skip more frames
    )
    view_camera(camera)