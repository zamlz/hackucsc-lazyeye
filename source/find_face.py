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
    glasses = 'yesGlasses'
    dir = random.choice(['up', 'down', 'left', 'right', 'straight'])
    print(path + glasses + '_' + lazy + '_' + dir + '.jpg')
    return path + glasses + '_' + lazy + '_' + dir + '.jpg'

face_cascade = cv2.CascadeClassifier(CASCADE_CLASSIFIER_FACE)
eye_cascade = cv2.CascadeClassifier(CASCADE_CLASSIFIER_EYE)
imgPath = randomImagePath()
img = cv2.imread(imgPath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 5)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()


"""
Testing live video feature
"""

cap = cv2.VideoCapture(1)

while(True):
    ret, frame = cap.read()

    face_cascade = cv2.CascadeClassifier(CASCADE_CLASSIFIER_FACE)
    eye_cascade = cv2.CascadeClassifier(CASCADE_CLASSIFIER_EYE)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()