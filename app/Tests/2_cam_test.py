import cv2
import threading

class BufferlessVideoCapture:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.lock = threading.Lock()
        self.latest_frame = None
        threading.Thread(target=self._update_frame, daemon=True).start()

    def _update_frame(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
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
    camera = BufferlessVideoCapture()
    view_camera(camera)
