import cv2
import threading

class Camera:
    def __init__(self, camera_index=0, width=580, height=580, fps=30, color=True, skip_frames=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.width = width
        self.height = height
        self.fps = fps
        self.color = color
        self.skip_frames = skip_frames
        self.lock = threading.Lock()
        self.frame_count = 0
        self.running = True

        # Set camera resolution and frame rate
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        self.latest_frame = None # (640, 480, 3) uint8
        threading.Thread(target=self._update_frame, daemon=True).start()

    def _update_frame(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    if self.skip_frames > 0 and self.frame_count % (self.skip_frames + 1) != 0:
                        self.frame_count += 1
                        continue

                    # frame = cv2.resize(frame, (self.width, self.height))
                    if not self.color:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    self.frame_count += 1
                    self.latest_frame = frame
                    # print(self.latest_frame)

    def read(self):
        with self.lock:
            return self.latest_frame

    def release(self):
        self.running = False
        self.cap.release()

    def set_color(self, color):
        with self.lock:
            self.color = color

    def set_skip_frames(self, skip_frames):
        with self.lock:
            self.skip_frames = skip_frames
            self.frame_count = 0  # Reset frame count to immediately apply skip effect

    def start_viewing(self):
        cv2.namedWindow('Camera Feed', cv2.WINDOW_AUTOSIZE)
        while self.running:
            frame = self.read()
            if frame is not None:
                cv2.imshow('Camera Feed', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        self.release()
        cv2.destroyAllWindows()








if __name__ == "__main__":
    camera = Camera(color=True, skip_frames=1)
    camera.start_viewing()