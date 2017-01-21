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
    
def colorAvg(img):
    color = 0
    y, x = img.shape
    for i in range(x):
        for j in range(y):
            color += int(img[-j,i])
    return color/(x * y)


def createContrastedImg(eyeImg):
    eyeImg = cv2.cvtColor(eyeImg, cv2.COLOR_BGR2GRAY)   
    averageColor = colorAvg(eyeImg)
    ret,eyeContrast = cv2.threshold(eyeImg,averageColor,255,cv2.THRESH_BINARY)
    #  histeq = cv2.equalizeHist(cropSingleEye)
    # cv2.imshow('gray',cropSingleEye)
    return eyeContrast

    
def findPupils(eyeImg):
    eyeImg = createContrastedImg(eyeImg)
    img = cv2.cvtColor(eyeImg, cv2.COLOR_BGR2GRAY) 
    #cimg = createContrastedImg(eyeImg)
    #cimg = cv2.cvtColor(eyeImg,cv2.COLOR_GRAY2BGR)
    img = cv2.medianBlur(img,5)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
    return img
    
    
cropEyeLocations = []
    

face_cascade = cv2.CascadeClassifier(CASCADE_CLASSIFIER_FACE)
eye_cascade = cv2.CascadeClassifier(CASCADE_CLASSIFIER_EYE)
imgPath = randomImagePath()
print imgPath
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
    cv2.imshow('cropeye',createContrastedImg(cropSingleEye))
    #cv2.imshow('cropeye',findPupils(cropSingleEye))
    cv2.waitKey(0)


cv2.destroyAllWindows()

