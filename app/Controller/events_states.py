
from enum import Enum, auto


# Define the events
class Event(Enum):
    ON_CLOSE = auto()
    SETTINGS = auto()
    START_CAMERA = auto()
    SETTINGS_BUTTON_1 = auto()
    SETTINGS_BUTTON_2 = auto()
    TAKE_PICTURE = auto()
    RECORD_VIDEO = auto()
    DEMO = auto()
    DUMMY_BUTTON = auto()
    ACOUSTIC_VIEWER = auto()
    CAMERA_VIEWER = auto()
    ACOUSTIC_CAMERA_VIEWER = auto()



# Define the states using an enumeration
class State(Enum):
    IDLE = auto()
    SHUTTING_DOWN = auto()
    SETTINGS_OPEN = auto()
    DEMO_IN_PROGRESS = auto()