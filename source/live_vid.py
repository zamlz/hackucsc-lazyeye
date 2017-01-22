import cv2
import time
import find_face as ff
import platform
import win32api
from collections import deque

# Classifiers
CASCADE_CLASSIFIER_FACE = 'haarcascades/haarcascade_frontalface_default.xml'
CASCADE_CLASSIFIER_EYE = 'haarcascades/haarcascade_eye.xml'

#Neccesary vars
VK_MEDIA_PLAY_PAUSE = 0xB3
hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE,0)

# Camera is set to 0. This is the default camera it looks at.
# We should reference a setting file for this, but we will handle
# that later
CAMERA = 0
BUFFER = deque([])
BUFFER_SIZE = 30

# State Machine Variables
STATE_LOW_THRESH = 25
STATE_HIGH_THRESH = 45

for i in xrange(BUFFER_SIZE):
    BUFFER.append(1)

def startWebcamService():
    STATE_LOCKED = False
    while(True):
        cap = cv2.VideoCapture(CAMERA)
        ret, frame = cap.read()
        startFrame = 1
        endFrame = 5
        count = 0
        isLazy = False
        
        while cap.isOpened():
            success, frame = cap.read()
            
            if success and endFrame > count > startFrame:
                count+=1
                frame, isLazy = ff.findFaceAndEyesWebcam(frame)
                STATE_LOCKED = averageBuffer(isLazy, STATE_LOCKED)
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
                
def toggleMedia():
    print "Toggled"
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)



def averageBuffer(isLazy, STATE_LOCKED):
    BUFFER.popleft()
    if(isLazy):
        BUFFER.append(0)
    else:
        BUFFER.append(1)
    avg = 0
    for buf in BUFFER:
        avg += buf
    avg =  100*float(avg)/BUFFER_SIZE
    print avg,"%"
    return stateMachine(avg, STATE_LOCKED)


def stateMachine(percent, STATE_LOCKED):
    if (percent < STATE_LOW_THRESH and STATE_LOCKED is False):
        STATE_LOCKED = True
        toggleMedia()
    if (percent > STATE_HIGH_THRESH and STATE_LOCKED is True):
        STATE_LOCKED = False
        toggleMedia()
    return STATE_LOCKED


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
