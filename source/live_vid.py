import cv2
import find_face as ff
import const
import win32api

for i in xrange(const.BUFFER_SIZE):
    const.BUFFER.append(1)

def startWebcamService():
    const.stateLocked = False
    while(True):
        cap = cv2.VideoCapture(const.CAMERA)
        startFrame = 1
        endFrame = 5
        count = 0
        
        while cap.isOpened():
            success, frame = cap.read()
            
            if success and endFrame > count > startFrame:
                count+=1
                frame, isLazy = ff.findFaceAndEyesWebcam(frame)
                averageBuffer(isLazy)
                cv2.imshow(const.TEAM_NAME, frame)
                if(count is endFrame):
                    count = 0
            else:
                if success:
                    cv2.imshow(const.TEAM_NAME, frame)
                    count += 1
            if cv2.waitKey(1) & const.disableCamera:
                break
        cap.release()
        cv2.destroyAllWindows()
        return


def toggleMedia():
    win32api.keybd_event(const.VK_MEDIA_PLAY_PAUSE, const.HWCODE)


def averageBuffer(isLazy):
    const.BUFFER.popleft()
    if(isLazy):
        const.BUFFER.append(0)
    else:
        const.BUFFER.append(1)
    avg = 0
    for buf in const.BUFFER:
        avg += buf
    avg =  100*float(avg)/const.BUFFER_SIZE
    #print avg,"%"
    return stateMachine(avg)


def stateMachine(percent):
    if (percent < const.STATE_LOW_THRESH and const.stateLocked == False):
        const.stateLocked = True
        toggleMedia()
        const.systemTrayIcon.fireAlertMessage(const.LAZY_EYE_DETECTED, const.LAZY_EYE_ALERT_TIME)
    elif (percent > const.STATE_HIGH_THRESH and const.stateLocked == True):
        const.stateLocked = False
        toggleMedia()
        const.systemTrayIcon.fireAlertMessage(const.LAZY_EYE_FIXED, const.LAZY_EYE_FIX_TIME)


def main():
    startWebcamService()


if __name__ == '__main__':
    main()
