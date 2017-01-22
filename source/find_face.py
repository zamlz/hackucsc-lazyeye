import cv2
import random

import eye_ml as eml


# Image Sources
#IMAGE_PATH = '../test_data/data_set/'
IMAGE_PATH = '../test_data/new_set/'
#LAZY_FLAG = ['noLazy', 'yesLazy']
LAZY_FLAG = ['lazy0', 'lazy1', 'lazy2']
GLASSES_FLAG = ['noGlasses', 'yesGlasses']
#DIRECTION_FLAG = ['up', 'down', 'left', 'right', 'straight']
DIRECTION_FLAG = ['left', 'right', 'straight']

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

# Classifier Flags
FACE_SCALE_FACTOR = 1.2
FACE_MIN_NEIGHBORS = 5
EYE_SCALE_FACTOR = 1.1
EYE_MIN_NEIGHBORS = 5


# Eye to Face Ratios
FACE_TO_EYE_RATIO = 6


#######################
# Feature Detection
#######################
"""
findFaceAndEyes()
[desc] Detect the faces and eyes within a given image.

[imgPath] Path to image
[imgName] Image name

[ret]   Path to random image.
"""
def findFaceAndEyes(imgPath, imgName):
    img = cv2.imread(imgPath + imgName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the face
    faces = findFaces(gray)

    # Find the eyes in each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
        faceGrayed = gray[y:y + h, x:x + w]
        faceColored = img[y:y + h, x:x + w]
        
        leftEye, rightEye = findEyes(w, faceGrayed, faceColored)
        if leftEye is None:
            continue

        # Pupil Detection
        eyeLocations = packageEyes([leftEye, rightEye], x, y)
        eyeData = eml.cropEye(eyeLocations, imgPath+imgName)
        isLazy, pupilLoc = eml.isEyeLazy(eyeData)
        
        pupilLeftX = x + leftEye[0] + int(leftEye[2]/2) + int(pupilLoc[0][1])
        pupilLeftY = y + leftEye[1]
        pupilRightX = x + rightEye[0] + int(rightEye[2]/2) + int(pupilLoc[1][1])
        pupilRightY = y + rightEye[1]

        cv2.line(img, ( pupilLeftX, pupilLeftY), (pupilLeftX, pupilLeftY + leftEye[3]), (255,0,0))
        cv2.line(img, ( pupilRightX, pupilRightY), (pupilRightX, pupilRightY + rightEye[3]), (255,0,0))
        print isLazy
        
    # Display the image
    cv2.imshow(imgName,img)


"""
findFaces()
[desc]  Detect the faces within a given image.

[gray] Grayscale version of the image.

[ret]   A tuple containing the x, y, width, and height of
        the face box.
"""
def findFaces(gray):
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH + CASCADE_CLASSIFIER_FACE)
    return face_cascade.detectMultiScale(
        gray,
        scaleFactor = FACE_SCALE_FACTOR,
        minNeighbors = FACE_MIN_NEIGHBORS
    )


"""
findEyes()
[desc]  Detect the eyes within a given face. Averages
        several cascade classifiers to find the eye box.

[faceWidth] Width of the face box.
[gray] Grayscale version of the image.
[color] Color version of the image/

[ret]   Two tuples containing the x, y, width, and height of
        the eyes. If no eyes are detected within the face,
        it returns a tuple of Nones.
"""
def findEyes(faceWidth, gray, color):
    eyeList = []

    # Run Haar Cascades for eye detection
    for i in range(len(CASCADE_CLASSIFIER_EYE)):
        classifier = cv2.CascadeClassifier(CASCADE_PATH + CASCADE_CLASSIFIER_EYE[i])
        feature = classifier.detectMultiScale(
            gray,
            scaleFactor=EYE_SCALE_FACTOR,
            minNeighbors=EYE_MIN_NEIGHBORS,
            minSize=determineEyeMinSize(faceWidth)
        )
        eyeList.extend(feature)
        # Outline box
        # for (ex, ey, ew, eh) in feature:
        # cv2.rectangle(color, (ex, ey), (ex + ew, ey + eh), CASCADE_BOX_COLOR[i], 2)

    if len(eyeList) == 0:
        return None, None

    # Find the midline of all detected eye boxes
    midline = findFaceMidline(eyeList)

    # Average eye boxes for both eyes
    eyeL, eyeR = averageEyeBoxes(eyeList, midline)

    # Outline averaged eyes
    cv2.rectangle(color, (eyeL[0], eyeL[1]), (eyeL[0] + eyeL[2], eyeL[1] + eyeL[2]), (255, 255, 255), 2)
    cv2.rectangle(color, (eyeR[0], eyeR[1]), (eyeR[0] + eyeR[2], eyeR[1] + eyeR[2]), (255, 255, 255), 2)

    # (x, y, w, h)
    return (
        (eyeL[0], eyeL[1], eyeL[2], eyeL[3]),
        (eyeR[0], eyeR[1], eyeR[2], eyeR[3])
    )


#######################
# Tester Functions
#######################
"""
testRandomImage()
[desc]  Tests a random image from the sample set. Will be
        removed when we interface with the webcam.
"""
def testRandomImage():
    lazy = random.choice(LAZY_FLAG)
    glasses = random.choice(GLASSES_FLAG)
    dir = random.choice(DIRECTION_FLAG)
    imgName = glasses + '_' + dir + '_' + lazy + '.jpg'
    findFaceAndEyes(IMAGE_PATH, imgName)
    cv2.waitKey(0)
    destroyKresge()


"""
testEveryImage()
[desc]  Tests every image from the sample set. Will be
        removed when we interface with the webcam.
"""
def testEveryImage():
    for glasses in GLASSES_FLAG:
        for dir in DIRECTION_FLAG:
            for lazy in LAZY_FLAG:
                imgName = glasses + '_' + dir + '_' + lazy + '.jpg'
                findFaceAndEyes(IMAGE_PATH, imgName)
                cv2.waitKey(0)
                destroyKresge()



#######################
# Utility Functions
#######################
"""
[desc]  Takes the eye tuples and x,y reference point of the
        face to put the touple in global coordinate form.
        
[eyes]  The eyes tuple. It is constructed with local coordinates

[x]     The starting x coordinate of the face

[y]     The starting y coordinate of the face

[ret]   Returns the corrected eye tuples
"""
def packageEyes(eyes,x,y):
    pkgEye = []
    for (ex,ey,ew,eh) in eyes:
        pkgEye.append((x+ex, x+ex+ew, y+ey, y+ey+eh ))
    return pkgEye
    

"""
determineEyeMinSize()
[desc]  Returns the minimum size of an eye box given a face
        size. Currently based on hard coded ratios.

[faceWidth] Width of the face box.

[ret]   Tuple containing the minimum size of the eye box.
"""
def determineEyeMinSize(faceWidth):
    minSize = faceWidth / FACE_TO_EYE_RATIO
    return (minSize, minSize)


"""
findFaceMidline()
[desc]  Finds the 'middle' of a face (between their eyes
        from the list of eye boxes.

[eyeList] List of eye boxes

[ret]   X line of the middle of the face.
"""
def findFaceMidline(eyeList):
    total = 0
    for box in eyeList:
        x, _, _, _ = box
        total += x
    return total / len(eyeList)


"""
averageEyeBoxes()
[desc]  Averages the eye boxes for each eye to find a more
        accurate eye box.

[eyeList] List of eye boxes.
[midline] Middle line of face used to determine which eye
          the box belongs to.

[ret]   Two lists containing the x, y, width, and height
        of the averaged eye boxes.
"""
def averageEyeBoxes(eyeList, midline):
    eyeL = [0, 0, 0, 0]
    eyeR = [0, 0, 0, 0]
    leftCount = 0
    rightCount = 0
    for box in eyeList:
        eye = [0, 0, 0, 0]  # [x, y, w, h]
        eye[0], eye[1], eye[2], eye[3] = box

        # Add box to proper list for averaging
        if eye[0] < midline:  # Image left eye
            leftCount += 1
            for i in range(4):
                eyeL[i] += eye[i]
        else:  # Image right eye
            rightCount += 1
            for i in range(4):
                eyeR[i] += eye[i]

    # Average lists
    for i in range(4):
        eyeL[i] = eyeL[i] / leftCount
        eyeR[i] = eyeR[i] / rightCount

    return (eyeL, eyeR)


"""
destroyKresge()
[desc]  I endorse this.
"""
def destroyKresge():
    cv2.destroyAllWindows()


#######################
# Main
#######################
def main():
    testEveryImage()


if __name__ == '__main__':
    main()
