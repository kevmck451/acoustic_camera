#!/usr/bin/python3

import sys
import time
import pygame
from pygame.locals import QUIT
import pygame.camera

class CameraGUI:
    def __init__(self):
        pygame.init()
        pygame.camera.init()

        self.display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Camera Feed')

        self.cam_list = pygame.camera.list_cameras()
        if not self.cam_list:
            print("No camera found. Exiting...")
            sys.exit(1)

        self.cam = pygame.camera.Camera(self.cam_list[0], (640, 480))
        self.cam.start()

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            frame = self.cam.get_image()
            if frame is not None:
                self.display.blit(frame, (0, 0))

            pygame.display.update()
            clock.tick(30)  # Cap frame rate at 30 FPS

        self.cam.stop()
        pygame.quit()

if __name__ == '__main__':
    gui = CameraGUI()
    gui.run()
