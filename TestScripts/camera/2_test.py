#!/usr/bin/python3

import sys
import time
import numpy as np
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from picamera2 import Picamera2, Preview

class CameraGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration())
        self.picam2.start_preview(Preview.QTGL)
        self.picam2.start()

        self.overlay = np.zeros((300, 400, 4), dtype=np.uint8)
        self.overlay[:150, 200:] = (255, 0, 0, 64)
        self.overlay[150:, :200] = (0, 255, 0, 64)
        self.overlay[150:, 200:] = (0, 0, 255, 64)

        self.picam2.set_overlay(self.overlay)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Camera Feed')
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)  # Update frame every 10 milliseconds

    def update_frame(self):
        frame = self.picam2.get_frame()
        if frame is not None:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # Rotate frame 90 degrees clockwise
            h, w, c = frame.shape
            bytes_per_line = c * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        self.picam2.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraGUI()
    window.show()
    sys.exit(app.exec_())
