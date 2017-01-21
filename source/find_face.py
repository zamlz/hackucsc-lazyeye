import cv2
import random

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
DIRECTION_FLAG = ['up', 'down', 'left', 'right', 'straight']

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
    cv2.imshow(imgName,img)


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
                detectFaceAndEyes(IMAGE_PATH, imgName)
                cv2.waitKey(0)
                destroyKresge()
                
                
def main():
    testEveryImage()
        
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    main()


