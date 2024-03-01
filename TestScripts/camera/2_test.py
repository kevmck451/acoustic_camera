#!/usr/bin/python3

import sys
import time
import numpy as np
import cv2
import pygame
from pygame.locals import QUIT
from picamera2 import Picamera2, Preview

class CameraGUI:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Camera Feed')

        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration())
        self.picam2.start_preview(Preview.QTGL)
        self.picam2.start()

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            frame = self.picam2.get_preview_frame()  # Corrected method
            if frame is not None:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = np.rot90(frame)
                frame = pygame.surfarray.make_surface(frame)
                self.display.blit(frame, (0, 0))

            pygame.display.update()
            clock.tick(30)  # Cap frame rate at 30 FPS

        self.picam2.stop()
        pygame.quit()

if __name__ == '__main__':
    gui = CameraGUI()
    gui.run()
