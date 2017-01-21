import numpy as np
import cv2
import random

"""
    Test program from open_cv website
    http://docs.opencv.org/trunk/d7/d8b/tutorial_py_face_detection.html
"""

# Classifiers
CASCADE_CLASSIFIER_FACE = 'haarcascades/haarcascade_frontalface_default.xml'
CASCADE_CLASSIFIER_EYE = 'haarcascades/haarcascade_eye.xml'
CASCADE_CLASSIFIER_EYE_GLASSES = 'haarcascades/haarcascade_eye_tree_eyeglasses.xml'
CASCADE_CLASSIFIER_LEFT_EYE = 'haarcascades/haarcascade_lefteye_2splits.xml'
CASCADE_CLASSIFIER_RIGHT_EYE = 'haarcascades/haarcascade_righteye_2splits.xml'


# Image Sources
IMAGE_PATH = '../test_data/data_set/'
LAZY_FLAG = ['noLazy', 'yesLazy']
GLASSES_FLAG = ['noGlasses', 'yesGlasses']
DIRECTION_FLAG = ['up', 'down', 'left', 'right', 'straight']


def randomImagePath():
    path = '../test_data/data_set/'
    lazy = random.choice(['noLazy', 'yesLazy'])
    glasses = random.choice(['noGlasses', 'yesGlasses'])
    dir = random.choice(['up', 'down', 'left', 'right', 'straight'])
    return path + glasses + '_' + lazy + '_' + dir + '.jpg'
    
def isProportional(fWidth, eWidth):
    wRatio = fWidth / eWidth
    return True if (2.5 <= wRatio <= 6) else False


def detectFacialFeatures(imgPath, imgName):
    face_cascade = cv2.CascadeClassifier(CASCADE_CLASSIFIER_FACE)
    img = cv2.imread(imgPath + imgName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        testCascadeClassifier(
            cv2.CascadeClassifier(CASCADE_CLASSIFIER_EYE),
            roi_gray,
            roi_color,
            (255, 0, 0) # BLUE
        )
        testCascadeClassifier(
            cv2.CascadeClassifier(CASCADE_CLASSIFIER_EYE_GLASSES),
            roi_gray,
            roi_color,
            (0, 255, 0) # GREEN
        )
        testCascadeClassifier(
            cv2.CascadeClassifier(CASCADE_CLASSIFIER_LEFT_EYE),
            roi_gray,
            roi_color,
            (0, 0, 255) # RED
        )
        testCascadeClassifier(
            cv2.CascadeClassifier(CASCADE_CLASSIFIER_RIGHT_EYE),
            roi_gray,
            roi_color,
            (0, 255, 255) # YELLOW
        )

    cv2.imshow(imgName,img)


def testCascadeClassifier(cascade, gray, color, boxColor):
    feature = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(75, 75)
    )
    for (ex, ey, ew, eh) in feature:
        cv2.rectangle(color, (ex, ey), (ex + ew, ey + eh), boxColor, 2)



def testImagePath(glasses, lazy, dir):
    return glasses + '_' + lazy + '_' + dir + '.jpg'


def testRandomImage():
    lazy = random.choice(LAZY_FLAG)
    glasses = random.choice(GLASSES_FLAG)
    dir = random.choice(DIRECTION_FLAG)
    imgName = testImagePath(glasses, lazy, dir)
    detectFacialFeatures(IMAGE_PATH, imgName)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def testEveryImage():
    for glasses in GLASSES_FLAG:
        for lazy in LAZY_FLAG:
            for dir in DIRECTION_FLAG:
                imgName = testImagePath(glasses, lazy, dir)
                detectFacialFeatures(IMAGE_PATH, imgName)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

testEveryImage()

cv2.waitKey(0)
cv2.destroyAllWindows()

