
import cv2
import numpy as np
import matplotlib.pyplot as plt



DEBUG_FLAG = False
LAZY_DELTA = 5


"""
isEyeLazy()
[desc]  Takes a list which contains the images of the
        left and right eye and returns a bool for it
        the eyes are lazy or not
        
[eyeImageData] This is simple a list of size two. It
        should contain the 2D Numpy array of the left
        and right eyes.
        
[ret]   Returns a true if lazy and false if not.
"""
def isEyeLazy(eyeImageData): 
    modelData = []
    for singleEye in eyeImageData:
        h, w, _ = singleEye.shape
        
        top_pad=0.3
        bot_pad=0.8
        left_pad=0.1
        right_pad=0.9
        
        # crop the eye images to really get a precision on the eyes and
        # grayscale the image.
        singleEyeTrim = singleEye[int(h*top_pad):int(h*bot_pad),int(w*left_pad):int(w*right_pad)]
        singleEyeGreyScale = createGreyScaleImg(singleEyeTrim)
        
        if (DEBUG_FLAG):
            cv2.imshow('cropeye',singleEyeGreyScale)
        
        intensity, vectorIndex = intensityDataColumnWise(singleEyeGreyScale)
        modelData.append((intensity, vectorIndex))
    
    pupilLoc = intensityVectorTrain(modelData)
    
    # Identify what the relative offset is for the pupils and determine
    # if it is within the threshold.
    if (abs(pupilLoc[0][1] - pupilLoc[1][1]) > LAZY_DELTA):
        return True, pupilLoc
    return False, pupilLoc
    

    
    
"""
intensityVectorTrain()
[desc]  Takes a dataset that contains a 1D vector of
        intensities and applies polynomial regression
        learning to find the best fit to the data. It
        returns what it believes to be the be pupil
        location
        
[dataset] This is a tuple of size two that contains
        two 1D vectors of the same size. First item
        of the tuple is the intensities vector and
        the second item is simply a list from 0 to n
        of the same size.
        
[ret]  A list of two tuples of size two that is the 
       pupil locations.
"""
def intensityVectorTrain(dataset):
    polyDegree = 6
    pupilLocations = []
    for (intensity,vectorIndex) in dataset:
        model = np.polyfit(vectorIndex, intensity, polyDegree)
        minPts, maxPts = findModelMaxMin(model)
        
        pupilLocations.append(guessPupilLocation(maxPts,float(len(vectorIndex))/2))
        
        if(DEBUG_FLAG):
            print model  
            print minPts
            print maxPts
            
            modelFunc = np.poly1d(model)
            phi = []
            for item in vectorIndex:
                phi.append(modelFunc(item))
            plt.plot(vectorIndex, intensity)
            plt.plot(vectorIndex, phi)
            plt.show()
        
    if(DEBUG_FLAG):
        print pupilLocations
        
    return pupilLocations


    
"""
guessPupilLocation()
[desc]  Takes Maxima points and the finds the
        closest value to the midpoint.
        
[maxPoints] A list of local Maxima

[midLineIndex] The value of the midpoint. Its
        a virtual vertical line that cuts the
        data plot in half.
        
[ret]   Returns the closest Maxima to the the
        midpoint
"""
def guessPupilLocation(maxPoints,midLineIndex):
    minPt = 0  
    minOffset = float(200)
    for pt in maxPoints:
        if (abs(pt - midLineIndex) < abs(minOffset)):
            minOffset = pt - midLineIndex
            minPt = pt
    return (minPt, minOffset)
        
 

"""
findModelMaxMin()
[desc]  Using the first and second derivative tests to 
        identify the local maxima and minima of the 
        model function provided and returns them as a
        touple of lists.
        
[model] A list of coefficients made in the form
        [a,b,c,...,z] ==> ax^n + bx^(n-1) + ... + z 
        
[ret]   Returns a list of maximas and minimas in a 
        tuple.
"""
def findModelMaxMin(model):
    screenMaxWidth = 150
    model = model[::-1]
    modelD0 = np.polynomial.polynomial.Polynomial(model)
    modelD1 = modelD0.deriv()
    modelD2 = modelD1.deriv()
    points = []
    for root in modelD1.roots():
        if (0 <= root <= screenMaxWidth):
            points.append(root)
    maxPoints = []
    minPoints = []
    for pt in points:
        if (modelD2(pt) > 0 and pt.imag == 0):
            minPoints.append(pt.real)
        elif (modelD2(pt) < 0 and pt.imag == 0):
            maxPoints.append(pt.real)
    return minPoints, maxPoints
                

"""
cropEye()
[desc]  Takes in eye location data and
        and the original image data
        
[cropEyeLoc] Contains a list of tuples with
        the eye locations. tuples are
        of the form (x1,x2,y1,y2)
    
[imgDirLocation] Original image location

[ret]   returns a list of the cropeed eyes.
"""
def cropEye(cropEyeLoc, imgOriginal):
    croppedEyes = []
    for (x1,x2,y1,y2) in cropEyeLoc:
        croppedEyes.append(imgOriginal[y1:y2, x1:x2])
    return croppedEyes


    
"""
createGreyScaleImg()
[desc]  Takes a image array and returns a greyscale
        version of it
        
[eyeImg]A color image array
        
[ret]   Returns a greyscale image of the array.
"""
def createGreyScaleImg(eyeImg):
    eyeImg = cv2.cvtColor(eyeImg, cv2.COLOR_BGR2GRAY)
    return eyeImg


"""
intensityDataColumnWise()
[desc]  Takes a greyscale image and returns a vector
        of column sum of intensities
        
[img]   Greyscale image
        
[ret]   Vector of column sum of intensities
"""
def intensityDataColumnWise(img):
    color = 0.0
    y, x = img.shape
    vectorIndex = []
    intensity = []
    for i in range(x):
        color = 0
        vectorIndex.append(i)
        for j in range(y):
            color += float(255 - int(img[j,i]))/255
        intensity.append(color)
    return intensity,vectorIndex
    

    
"""
intensityDataRowWise()
[desc]  Takes a greyscale image and returns a vector
        of row sum of intensities
        
[img]   Greyscale image
        
[ret]   Vector of column row of intensities
"""
def intensityDataRowWise(img):
    color = 0
    y, x = img.shape
    vectorIndex = []
    intensity = []
    for j in range(y):
        color = 0
        vectorIndex.append(j)
        for i in range(x):
            color += float(255 - int(img[j,i]))/255
        intensity.append(color)
    return intensity,vectorIndex
