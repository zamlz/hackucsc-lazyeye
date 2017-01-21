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
CASCADE_CLASSIFIER_GLASSES = 'haarcascades/haarcascade_eye_tree_eyeglasses.xml'

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
    eye_cascade = cv2.CascadeClassifier(CASCADE_CLASSIFIER_EYE)
    img = cv2.imread(imgPath + imgName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100),
            maxSize=(180, 180)
        )
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    cv2.imshow(imgName,img)


def testImagePath(glasses, lazy, dir):
    return glasses + '_' + lazy + '_' + dir + '.jpg'


def testRandomImage():
    lazy = random.choice()
    glasses = random.choice()
    dir = random.choice()
    imgName = testImagePath(glasses, lazy, dir)
    detectFacialFeatures(IMAGE_PATH, imgName)


def testEveryImage():
    for glasses in GLASSES_FLAG:
        for lazy in LAZY_FLAG:
            for dir in DIRECTION_FLAG:
                imgName = testImagePath(glasses, lazy, dir)
                detectFacialFeatures(IMAGE_PATH, imgName)

testEveryImage()

cv2.waitKey(0)
cv2.destroyAllWindows()