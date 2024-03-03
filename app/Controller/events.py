
from enum import Enum, auto


# Define the events
class Event(Enum):
    ON_CLOSE = auto()
    SETTINGS = auto()
    START_CAMERA = auto()
    SETTINGS_BUTTON_1 = auto()
    SETTINGS_BUTTON_2 = auto()
