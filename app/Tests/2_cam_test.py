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

class BufferlessVideoCapture:
    def __init__(self, camera_index=0, width=580, height=580, fps=30, color=True, skip_frames=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.width = width
        self.height = height
        self.fps = fps
        self.color = color
        self.skip_frames = skip_frames

        # Set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        self.lock = threading.Lock()
        self.latest_frame = None
        threading.Thread(target=self._update_frame, daemon=True).start()

    def _update_frame(self):
        frame_count = 0
        while True:
            ret, frame = self.cap.read()
            if ret:
                if self.skip_frames > 0 and frame_count % (self.skip_frames + 1) != 0:
                    frame_count += 1
                    continue
                frame_count += 1

                if not self.color:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if self.width != frame.shape[1] or self.height != frame.shape[0]:
                    frame = cv2.resize(frame, (self.width, self.height))

                with self.lock:
                    self.latest_frame = frame

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
            cv2.imshow('Camera Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    camera_instance.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera = BufferlessVideoCapture(color=True, skip_frames=1)  # Example usage
    view_camera(camera)
