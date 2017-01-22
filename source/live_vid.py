import cv2
import time
import find_face as ff
from collections import deque


# Classifiers
CASCADE_CLASSIFIER_FACE = 'haarcascades/haarcascade_frontalface_default.xml'
CASCADE_CLASSIFIER_EYE = 'haarcascades/haarcascade_eye.xml'

CAMERA = 0
BUFFER = deque([])
BUFFER_SIZE = 30
BUFFER_THRESH_PERCENT = 50

for i in xrange(BUFFER_SIZE):
    BUFFER.append(1)

def startWebcamService():
    while(True):
        cap = cv2.VideoCapture(CAMERA)
        ret, frame = cap.read()
        startFrame = 1
        endFrame = 5
        count = 0
        
        while cap.isOpened():
            success, frame = cap.read()
            
            if success and endFrame > count > startFrame:
                count+=1
                frame, isLazy = ff.findFaceAndEyesWebcam(frame)
                averageBuffer(isLazy)
                cv2.imshow('frame', frame)
                if(count is endFrame):
                    count = 0
            else:
                if success:
                    cv2.imshow('frame', frame)
                    count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        exit(0)      
                


def averageBuffer(isLazy):
    BUFFER.popleft()
    if(isLazy):
        BUFFER.append(0)
    else:
        BUFFER.append(1)
    avg = 0
    for buf in BUFFER:
        avg += buf
    print 100*float(avg)/BUFFER_SIZE, "%"




"""
[desc]  This function captures footage from the webcam and makes it readable from the 'frame' variable

"""
def trackFromWebcam():
    while(True):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        startFrame = 10
        endFrame = 15
        count = 0
        isLazy = False

        while cap.isOpened():
            success, frame = cap.read()
            if success and endFrame > count > startFrame :

                count+=1
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
                if(count is endFrame):
                    count = 0
            else:
                if success:
                    cv2.imshow('frame', frame)
                    count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        exit(0)

        
if __name__ == '__main__':
    startWebcamService()
    #trackFromWebcam()