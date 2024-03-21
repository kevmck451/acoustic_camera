import numpy as np

from .filter_audio import Filter_Audio


class Overlay:
    def __init__(self, audio, video):
        self.height, self.width = 580, 580
        self.overlay = np.zeros((self.height, self.width))

    @staticmethod
    def mode(event):
        if event == 'rms':
            pass
        elif event == 'detect_drone':
            pass
        elif event == 'detect_drone':
            pass
        else:
            pass