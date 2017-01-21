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

# Image Sources

def randomImagePath():
    path = '../test_data/data_set/'
    lazy = random.choice(['noLazy', 'yesLazy'])
    glasses = random.choice(['noGlasses', 'yesGlasses'])
    dir = random.choice(['up', 'down', 'left', 'right', 'straight'])
    return path + glasses + '_' + lazy + '_' + dir + '.jpg'

"""
    cropEye() - Takes in eye location data and
                and the original image data
    cropEyeLoc - Contains a list of tuples with
                 the eye locations. tuples are
                 of the form (x1,x2,y1,y2)
    imgData - Image data to crop eyes from
"""
def cropEye(cropEyeLoc, imgData):
    croppedEyes = []
    for (x1,x2,y1,y2) in cropEyeLoc:
        croppedEyes.append(imgData[y1:y2, x1:x2])
    return croppedEyes

cropEyeLocations = []
    

face_cascade = cv2.CascadeClassifier(CASCADE_CLASSIFIER_FACE)
eye_cascade = cv2.CascadeClassifier(CASCADE_CLASSIFIER_EYE)
imgPath = randomImagePath()
img = cv2.imread(imgPath)
imgOriginal = cv2.imread(imgPath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 5)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        cropEyeLocations.append((x+ex, x+ex+ew, y+ey, y+ey+eh))        
cv2.imshow('img',img)

cv2.waitKey(0)

cropEyeImgData = cropEye(cropEyeLocations, imgOriginal)
for cropSingleEye in cropEyeImgData:
    cv2.imshow('cropEye',cropSingleEye)
    cv2.waitKey(0)


cv2.destroyAllWindows()

