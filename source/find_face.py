import cv2
import const
import eye_ml as eml

#######################
# Feature Detection
#######################
"""
findFaceAndEyes()
[desc] Load the file from the location specified and
        and send it to the core function

[imgPath] Path to image
[imgName] Image name

[ret]   Path to random image.
"""
def findFaceAndEyes(imgPath, imgName):
    img = cv2.imread(imgPath + imgName)
    img, _ = findFaceAndEyesCore(img)
    # Display the image
    cv2.imshow(imgName,img)
    
"""
findFaceAndEyesWebcam()
[desc] Get a frame image from the webcam and
        let the core process it like normal.
        

[imgPath] Path to image
[imgName] Image name

[ret]   Path to random image.
"""
def findFaceAndEyesWebcam(img):
    return findFaceAndEyesCore(img)
    

"""
findFaceAndEyesCore()
[desc] Detect the faces and eyes within a given image.

[imgPath] Raw image array

[ret]   Path to random image.
""" 
def findFaceAndEyesCore(img):
    isLazy = False
    imgOriginal = img[:]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the face
    faces = findFaces(gray)

    # Find the eyes in each face
    for face in faces:
        x, y, w, h = face
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
        faceGrayed = gray[y:y + h, x:x + w]
        faceColored = img[y:y + h, x:x + w]

        leftEye, rightEye = findEyes(face, faceGrayed, faceColored)
        if leftEye is None: # Break if only one eye is found
            continue

        # Pupil Detection
        eyeLocations = packageEyes([leftEye, rightEye], x, y)
        eyeData = eml.cropEye(eyeLocations, imgOriginal)
        isLazy, pupilLoc = eml.isEyeLazy(eyeData)
        
        pupilLeftX = x + leftEye[0] + int(leftEye[2]/2) + int(pupilLoc[0][1])
        pupilLeftY = y + leftEye[1]
        pupilRightX = x + rightEye[0] + int(rightEye[2]/2) + int(pupilLoc[1][1])
        pupilRightY = y + rightEye[1]

        redPot =  255 * float(abs(pupilLoc[0][1] - pupilLoc[1][1]))/(eml.LAZY_DELTA*3)
        bluePot = 255 * float(eml.LAZY_DELTA*3 - abs(pupilLoc[0][1] - pupilLoc[1][1]))/(eml.LAZY_DELTA*3)

        redPot = min(max(0,redPot),255)
        bluePot = min(max(0,bluePot),255)

        thick = 3
        cv2.line(img, ( pupilLeftX, pupilLeftY), (pupilLeftX, pupilLeftY + leftEye[3]), (bluePot,0,redPot), thick)
        cv2.line(img, ( pupilRightX, pupilRightY), (pupilRightX, pupilRightY + rightEye[3]), (bluePot,0,redPot), thick)
    
    if isLazy == None:
        return img, False
    return img, isLazy
        

    
"""
findFaces()
[desc]  Detect the faces within a given image.

[gray] Grayscale version of the image.

[ret]   A tuple containing the x, y, width, and height of
        the face box.
"""
def findFaces(gray):
    face_cascade = cv2.CascadeClassifier(const.CASCADE_PATH + const.CASCADE_CLASSIFIER_FACE)
    return face_cascade.detectMultiScale(
        gray,
        scaleFactor = const.FACE_SCALE_FACTOR,
        minNeighbors = const.FACE_MIN_NEIGHBORS
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


def findEyes(face, gray, color):
    x, y, w, h = face
    minEyeBoxSize = determineEyeMinSize(w)
    eyeList = []

    # Run Haar Cascades for eye detection
    for i in range(len(const.CASCADE_CLASSIFIER_EYE)):
        classifier = cv2.CascadeClassifier(const.CASCADE_PATH + const.CASCADE_CLASSIFIER_EYE[i])
        features = classifier.detectMultiScale(
            gray,
            scaleFactor=const.EYE_SCALE_FACTOR,
            minNeighbors=const.EYE_MIN_NEIGHBORS,
            minSize=(minEyeBoxSize,minEyeBoxSize)
        )
        for box in features:
            bx, by, bw, bh = box
            if by < h * const.FACE_IGNORE_LINE:
                eyeList.append(box)
                # Outline box
                if const.TESTING_BOXES:
                    (ex, ey, ew, eh) = box
                    cv2.rectangle(color, (ex, ey), (ex + ew, ey + eh), const.CASCADE_BOX_COLOR[i], 2)

    if len(eyeList) < 2:
        return None, None

    # Find the midline of all detected eye boxes
    midline = findFaceMidline(eyeList)

    # Average eye boxes for both eyes
    eyeL, eyeR = averageEyeBoxes(eyeList, midline)

    if eyeL is None or abs(midline - eyeL[0]) < minEyeBoxSize * const.EYE_BOX_SEPARATION_THRESHOLD:
        return None, None


    # Outline averaged eyes
    cv2.rectangle(color, (eyeL[0], eyeL[1]), (eyeL[0] + eyeL[2], eyeL[1] + eyeL[2]), (255, 255, 255), 2)
    cv2.rectangle(color, (eyeR[0], eyeR[1]), (eyeR[0] + eyeR[2], eyeR[1] + eyeR[2]), (255, 255, 255), 2)

    # (x, y, w, h)
    return (
        (eyeL[0], eyeL[1], eyeL[2], eyeL[3]),
        (eyeR[0], eyeR[1], eyeR[2], eyeR[3])
    )



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
    return faceWidth / const.FACE_TO_EYE_RATIO


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

    if leftCount == 0 or rightCount == 0:
        return None, None

    # Average lists
    for i in range(4):
        eyeL[i] = eyeL[i] / leftCount
        eyeR[i] = eyeR[i] / rightCount

    return eyeL, eyeR


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
    pass

if __name__ == '__main__':
    main()
