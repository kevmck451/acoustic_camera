#!/usr/bin/python3

import sys
import pygame
from pygame.locals import QUIT
from picamera import PiCamera


class CameraGUI:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Camera Feed')

        self.camera = PiCamera()
        self.camera.resolution = (800, 600)
        self.camera.start_preview()

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Capture a frame from the camera
            self.camera.capture('/tmp/frame.jpg')

            # Load the captured frame
            frame = pygame.image.load('/tmp/frame.jpg')

            # Display the frame
            self.display.blit(frame, (0, 0))
            pygame.display.update()

            clock.tick(30)  # Cap frame rate at 30 FPS

        self.camera.stop_preview()
        self.camera.close()
        pygame.quit()


if __name__ == '__main__':
    gui = CameraGUI()
    gui.run()
