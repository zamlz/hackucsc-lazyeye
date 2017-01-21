import cv2
import random
import numpy as np

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

# Image Sources
IMAGE_PATH = '../test_data/data_set/'
LAZY_FLAG = ['noLazy', 'yesLazy']
GLASSES_FLAG = ['noGlasses', 'yesGlasses']
#DIRECTION_FLAG = ['up', 'down', 'left', 'right', 'straight']
DIRECTION_FLAG = ['straight']

# Eye to Face Ratios
FACE_TO_EYE_RATIO = 6


"""
destroyKresge()
[desc]  I endorse this.
"""
def destroyKresge():
    cv2.destroyAllWindows()


"""
randomImagePath()
[desc]  Returns a random image path.

[ret]   Path to random image.
"""
def randomImagePath():
    lazy = random.choice(LAZY_FLAG)
    glasses = random.choice(GLASSES_FLAG)
    dir = random.choice(DIRECTION_FLAG)
    return IMAGE_PATH + glasses + '_' + lazy + '_' + dir + '.jpg'


"""
detectFace()
[desc]
"""
def detectFaceAndEyes(imgPath, imgName):
    cropEyeLocations = []
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH + CASCADE_CLASSIFIER_FACE)
    img = cv2.imread(imgPath + imgName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyeList = []

        # Run Haar Cascades for eye detection
        for i in range(len(CASCADE_CLASSIFIER_EYE)):
            eyeList.extend(runCascadeClassifier(
                cv2.CascadeClassifier(CASCADE_PATH + CASCADE_CLASSIFIER_EYE[i]),
                roi_gray,
                CASCADE_BOX_COLOR[i],
                w
            ))

        # Find the midline of all detected eye boxes
        totalX = 0
        for box in eyeList:
            ex, ey, _, _ = box
            totalX += ex
        avgX = totalX / len(eyeList)

        # Find the average box of each eye
        leftCount = 0
        eyeL = [0,0,0,0]
        rightCount = 0
        eyeR = [0,0,0,0]
        for box in eyeList:
            eye = [0,0,0,0]
            eye[0], eye[1], eye[2], eye[3] = box
            if eye[0] < avgX: # Image left eye
                leftCount += 1
                for i in range(4):
                    eyeL[i] += eye[i]
            else: # Image right eye
                rightCount += 1
                for i in range(4):
                    eyeR[i] += eye[i]
        for i in range(4):
            eyeL[i] = eyeL[i] / leftCount
            eyeR[i] = eyeR[i] / rightCount

        # Print averaged eyes
        cv2.rectangle(roi_color, (eyeL[0], eyeL[1]), (eyeL[0] + eyeL[2], eyeL[1] + eyeL[2]), (255,255,255), 2)
        cv2.rectangle(roi_color, (eyeR[0], eyeR[1]), (eyeR[0] + eyeR[2], eyeR[1] + eyeR[2]), (255,255,255), 2)
        cropEyeLocations.append((x+eyeL[0], x+eyeL[0]+eyeL[2], y+eyeL[1], y+eyeL[1]+eyeL[2]))
        cropEyeLocations.append((x+eyeR[0], x+eyeR[0]+eyeR[2], y+eyeR[1], y+eyeR[1]+eyeR[2]))
    cv2.imshow(imgName,img)
    return cropEyeLocations


def determineEyeMinSize(faceWidth):
    return (faceWidth / FACE_TO_EYE_RATIO, faceWidth / FACE_TO_EYE_RATIO)


def runCascadeClassifier(cascade, grayScale, boxColor, faceWidth):
    feature = cascade.detectMultiScale(
        grayScale,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize = determineEyeMinSize(faceWidth)
    )
    # Print out box
    #for (ex, ey, ew, eh) in feature:
        #cv2.rectangle(color, (ex, ey), (ex + ew, ey + eh), boxColor, 2)
    return feature


def testImagePath(glasses, lazy, dir):
    return glasses + '_' + lazy + '_' + dir + '.jpg'


def testRandomImage():
    lazy = random.choice(LAZY_FLAG)
    glasses = random.choice(GLASSES_FLAG)
    dir = random.choice(DIRECTION_FLAG)
    imgName = testImagePath(glasses, lazy, dir)
    detectFaceAndEyes(IMAGE_PATH, imgName)
    cv2.waitKey(0)
    destroyKresge()


def testEveryImage():
    for glasses in GLASSES_FLAG:
        for lazy in LAZY_FLAG:
            for dir in DIRECTION_FLAG:
                imgName = testImagePath(glasses, lazy, dir)
                eyeLocations = detectFaceAndEyes(IMAGE_PATH, imgName)
                cropEyeImgData = cropEye(eyeLocations, IMAGE_PATH+imgName)
                for cropSingleEye in cropEyeImgData:
                    cv2.imshow('cropeye',findPupils(cropSingleEye))
                    #cv2.imshow('cropeye',findPupils(cropSingleEye))
                    cv2.waitKey(0)
                cv2.waitKey(0)
                destroyKresge()
                

"""
    cropEye() - Takes in eye location data and
                and the original image data
    cropEyeLoc - Contains a list of tuples with
                 the eye locations. tuples are
                 of the form (x1,x2,y1,y2)
    imgData - Image data to crop eyes from
"""
def cropEye(cropEyeLoc, imgDirLocation):
    imgData = cv2.imread(imgDirLocation)
    print(imgData)
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
    #img = cv2.cvtColor(eyeImg, cv2.COLOR_BGR2GRAY)
    #img = cv2.medianBlur(img,5)
    #cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    #circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,150,
    #                        param1=50,param2=60,minRadius=0,maxRadius=0)
    image = eyeImg.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe = cl1.apply(gray)
    blur = cv2.medianBlur(clahe, 7)
    
    circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,2,150,
                            param1=50,param2=30,minRadius=0,maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)
    return image


def main():
    testEveryImage()
        
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    main()



