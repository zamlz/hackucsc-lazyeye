"""
	Yoinked from BenjaminPoilive public repo on gist.github.com

"""

import operator
import numpy as np
import math
import cv2
#from config import config -------------------------- CRAL

kGradientThreshold = 10.0
kWeightBlurSize = 5
maxEyeSize=8

def computeGradient(img):
    out = np.zeros((img.shape[0],img.shape[1]),dtype=np.float32) #create a receiver array
    if img.shape[0] < 2 or img.shape[1] < 2: # TODO I'm not sure that secure out of range
        print "EYES too small"
        return out
    for y in xrange(0,out.shape[0]):
        out[y][0]=img[y][1]-img[y][0]
        for x in xrange(1,out.shape[1]-1):
            out[y][x]=(img[y][x+1]-img[y][x-1])/2.0
        out[y][out.shape[1]-1]=img[y][out.shape[1]-1]-img[y][out.shape[1]-2]
    return out



def testPossibleCentersFormula(x, y, weight, gx, gy, out):
    for cy in xrange(0,out.shape[0]):
        for cx in xrange(0,out.shape[1]):
            if x==cx and y==cy:
                continue
            dx= x-cx
            dy= y-cy
            magnitude= math.sqrt(dx*dx+dy*dy)
            dx=dx/magnitude
            dy=dy/magnitude
            dotProduct=dx*gx+dy*gy
            dotProduct=max(0.0, dotProduct)
            out[cy][cx]+=dotProduct*dotProduct*weight[cy][cx]




def findEyeCenter(eyeImg):
    eyeImg = eyeImg.astype(np.float32)
    scaleValue=1.0
    if(eyeImg.shape[0]>maxEyeSize or eyeImg.shape[1]>maxEyeSize ):
        scaleValue=max(maxEyeSize/float(eyeImg.shape[0]),maxEyeSize/float(eyeImg.shape[1]))
        eyeImg=cv2.resize(eyeImg,None, fx=scaleValue,fy= scaleValue, interpolation = cv2.INTER_AREA)

    gradientX= computeGradient(eyeImg)
    gradientY= np.transpose(computeGradient(np.transpose(eyeImg)))
    gradientMatrix=matrixMagnitude(gradientX, gradientY)
        
    gradientThreshold=computeDynamicThreshold(gradientMatrix,kGradientThreshold)
    #Normalisation
    for y in xrange(0,eyeImg.shape[0]):  #Iterate through rows
        for x in xrange(0,eyeImg.shape[1]):  #Iterate through columns
            if(gradientMatrix[y][x]>gradientThreshold):
                gradientX[y][x]=gradientX[y][x]/gradientMatrix[y][x]
                gradientY[y][x]=gradientY[y][x]/gradientMatrix[y][x]
            else:
                gradientX[y][x]=0.0
                gradientY[y][x]=0.0

    #Invert and blur befor algo
    weight = cv2.GaussianBlur(eyeImg,(kWeightBlurSize,kWeightBlurSize),0)
    for y in xrange(0,weight.shape[0]):  #Iterate through rows
        for x in xrange(0,weight.shape[1]):  #Iterate through columns
            weight[y][x]=255-weight[y][x]

    outSum = np.zeros((eyeImg.shape[0],eyeImg.shape[1]),dtype=np.float32) #create a receiver array
    for y in xrange(0,outSum.shape[0]):  #Iterate through rows
        for x in xrange(0,outSum.shape[1]):  #Iterate through columns
            if(gradientX[y][x]==0.0 and gradientY[y][x]==0.0):
                continue
            testPossibleCentersFormula(x, y, weight, gradientX[y][x], gradientY[y][x], outSum)

    #scale all the values down, basically averaging them
    numGradients = (weight.shape[0]*weight.shape[1])
    out= np.divide(outSum, numGradients*10)
    #find maxPoint
    (minval, maxval,mincoord,maxcoord) = cv2.minMaxLoc(out)
    maxcoord=(int(maxcoord[0]),int(maxcoord[1]))
    return (int(maxcoord[0]/scaleValue), int(maxcoord[1]/scaleValue))



def matrixMagnitude(gradX,gradY):
    mags = np.zeros((gradX.shape[0],gradX.shape[1]),dtype=np.float32) #create a receiver array
    for y in xrange(0,mags.shape[0]):
        for x in xrange(0,mags.shape[1]):
            gx=gradX[y][x]
            gy=gradY[y][x]
            magnitude=math.sqrt(gx*gx+gy*gy)
            mags[y][x]=magnitude
    return mags


def computeDynamicThreshold(gradientMatrix, DevFactor):
    (meanMagnGrad, meanMagnGrad) = cv2.meanStdDev(gradientMatrix)
    stdDev=meanMagnGrad[0]/math.sqrt(gradientMatrix.shape[0]*gradientMatrix.shape[1])
    return DevFactor*stdDev+meanMagnGrad[0]