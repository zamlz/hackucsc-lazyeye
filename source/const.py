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

#######################
# Feature Detection
#######################

# Image Sources
IMAGE_PATH = '../test_data/data_set/'
LAZY_FLAG = ['noLazy', 'yesLazy']
GLASSES_FLAG = ['noGlasses', 'yesGlasses']
DIRECTION_FLAG = ['up', 'down', 'left', 'right', 'straight']

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
FACE_SCALE_FACTOR = 1.1
FACE_MIN_NEIGHBORS = 5
EYE_SCALE_FACTOR = 1.1
EYE_MIN_NEIGHBORS = 5

# Eye to Face Ratios
FACE_TO_EYE_RATIO = 6