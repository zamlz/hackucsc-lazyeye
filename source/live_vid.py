import cv2
import find_face as ff
import const
import win32api
from collections import deque

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
            if cv2.waitKey(1) & const.disableCamera:
                break
        cap.release()
        cv2.destroyAllWindows()
        return


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


def main():
    startWebcamService()


if __name__ == '__main__':
    main()
