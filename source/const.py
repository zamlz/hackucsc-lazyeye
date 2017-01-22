from collections import deque
import win32api

# Team Info
TEAM_NAME = "Lazy Eye Watchdog."
TEAM_LOGO = "images/logo_512.png",

#######################
# Tray Constants
#######################
# Tray Constants
TRAY_ICON = [
    "images/logo_tray_inactive.png",
    "images/logo_tray_active.png"
]
TRAY_TOOLTIP = [
    "Who's Lazy? Not Eye! (Inactive - Press to activate)",
    "Who's Lazy? Not Eye! (Active - Press to disable)"
]

# Camera Flags
CAMERA_INACTIVE = 0
CAMERA_ACTIVE = 1

# Alert Messages and Flags
ALERT_TITLE = "Lazy Eye Watchdog"
ALERT_MESSAGE = [
    "Your lazy eye is acting up!",
    "Your lazy eye is fixed!"
]
LAZY_EYE_DETECTED = 0
LAZY_EYE_FIXED = 1
LAZY_EYE_ALERT_TIME = 10000
LAZY_EYE_FIX_TIME = 2500

# Toggle Notification
TOGGLE_MESSAGE_TIME = 1000
TOGGLE_MESSAGE = [
    "Lazy Eye Watchdog disabled.",
    "Lazy Eye Watchdog enabled."
]


#######################
# Feature Detection
#######################
# Test Image Sources
IMAGE_PATH = '../test_data/new_set/'
LAZY_FLAG = ['lazy0', 'lazy1', 'lazy2']
GLASSES_FLAG = ['noGlasses']
DIRECTION_FLAG = ['left', 'right', 'straight']
TESTING_BOXES = False

# Classifiers
# These are currently all provided by opencv
CASCADE_PATH = 'haarcascades/'
CASCADE_CLASSIFIER_FACE = 'haarcascade_frontalface_default.xml'
CASCADE_CLASSIFIER_EYE = [
    'haarcascade_eye.xml',
    'haarcascade_eye_tree_eyeglasses.xml',
    'haarcascade_lefteye_2splits.xml',
    'haarcascade_righteye_2splits.xml'
]
CASCADE_BOX_COLOR = [
    (0, 0, 255),  # RED
    (0, 255, 0),  # GREEN
    (255, 0, 0),  # BLUE
    (0, 255, 255) # YELLOW
]

# Cascade flags
FACE_SCALE_FACTOR = 1.2
FACE_MIN_NEIGHBORS = 5
EYE_SCALE_FACTOR = 1.1
EYE_MIN_NEIGHBORS = 5

# Facial Detection Patches
FACE_IGNORE_LINE = 0.55
EYE_BOX_SEPARATION_THRESHOLD = 0.75

# Eye to Face Ratios
FACE_TO_EYE_RATIO = 6

#######################
# Live Video Tracking
#######################
#Neccesary vars
VK_MEDIA_PLAY_PAUSE = 0xB3
HWCODE = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE,0)

# Camera is set to 0. This is the default camera it looks at.
# We should reference a setting file for this, but we will handle
# that later
CAMERA = 0
BUFFER = deque([])
BUFFER_SIZE = 30

# State Machine Variables
STATE_LOW_THRESH = 25
STATE_HIGH_THRESH = 45


#######################
# Globals
#######################
systemTrayIcon = None
disableCamera = False
stateLocked = False
