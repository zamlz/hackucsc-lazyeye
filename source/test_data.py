import const
import cv2
import find_face
import random

#######################
# Tester Functions
#######################
"""
testRandomImage()
[desc]  Tests a random image from the sample set. Will be
        removed when we interface with the webcam.
"""
def testRandomImage():
    lazy = random.choice(const.LAZY_FLAG)
    glasses = random.choice(const.GLASSES_FLAG)
    dir = random.choice(const.DIRECTION_FLAG)
    imgName = glasses + '_' + dir + '_' + lazy + '.jpg'
    find_face.findFaceAndEyes(const.IMAGE_PATH, imgName)
    cv2.waitKey(0)
    find_face.destroyKresge()


"""
testEveryImage()
[desc]  Tests every image from the sample set. Will be
        removed when we interface with the webcam.
"""
def testEveryImage():
    for glasses in const.GLASSES_FLAG:
        for dir in const.DIRECTION_FLAG:
            for lazy in const.LAZY_FLAG:
                imgName = glasses + '_' + dir + '_' + lazy + '.jpg'
                find_face.findFaceAndEyes(const.IMAGE_PATH, imgName)
                cv2.waitKey(0)
                find_face.destroyKresge()

#######################
# Main
#######################
def main():
    testEveryImage()

if __name__ == '__main__':
    main()
