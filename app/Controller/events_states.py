
from enum import Enum, auto


# Define the events
class Event(Enum):
    ON_CLOSE = auto()
    SETTINGS = auto()
    START_CAMERA = auto()
    STOP_CAMERA = auto()
    SETTINGS_BUTTON_1 = auto()
    SETTINGS_BUTTON_2 = auto()
    TAKE_PICTURE = auto()
    RECORD_VIDEO = auto()
    DUMMY_BUTTON = auto()
    DETECT_SOUNDS = auto()
    DETECT_DRONES = auto()
    CLASSIFY_DRONES = auto()
    DETECT_VEHICLES = auto()
    CLASSIFY_VEHICLES = auto()
    OVERLAY_COLOR_RED = auto()
    OVERLAY_COLOR_BLUE = auto()
    OVERLAY_COLOR_GREEN = auto()
    OVERLAY_THRESHOLD_WINDOW = auto()
    INCREASE_THRESHOLD = auto()
    DECREASE_THRESHOLD = auto()



# Define the states using an enumeration
class State(Enum):
    IDLE = auto()
    SHUTTING_DOWN = auto()
    SETTINGS_OPEN = auto()
    DEMO_IN_PROGRESS = auto()