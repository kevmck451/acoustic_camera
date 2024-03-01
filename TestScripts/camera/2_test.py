#!/usr/bin/python3

import sys
import time
import numpy as np
import cv2
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from picamera2 import Picamera2, Preview

class CameraThread(QThread):
    frame_signal = pyqtSignal(np.ndarray)

    def run(self):
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration())
        picam2.start_preview(Preview.QTGL)
        picam2.start()

        while True:
            frame = picam2.get_frame()
            if frame is not None:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                self.frame_signal.emit(frame)
            time.sleep(0.01)

class CameraGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.camera_thread = CameraThread()
        self.camera_thread.frame_signal.connect(self.update_frame)
        self.camera_thread.start()

    def init_ui(self):
        self.setWindowTitle('Camera Feed')
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def update_frame(self, frame):
        h, w, c = frame.shape
        bytes_per_line = c * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        self.camera_thread.quit()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraGUI()
    window.show()
    sys.exit(app.exec_())
