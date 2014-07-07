from os.path import isdir,join,normpath
from os import listdir
from PIL import Image
import sys
import matplotlib.pyplot as plt

import numpy as np
from numpy import asfarray,dot,argmin,zeros
from numpy import average,sort,trace
from numpy.linalg import svd,eigh
from numpy import concatenate, reshape
from math import sqrt

import tkFileDialog

def parseDirectory(directoryName,extension):
    '''This method returns a list of all filenames in the Directory directoryName. 
    For each file the complete absolute path is given in a normalized manner (with 
    double backslashes). Moreover only files with the specified extension are returned in 
    the list.
    '''
    if not isdir(directoryName): return
    imagefilenameslist=sorted([
        normpath(join(directoryName, fname))
        for fname in listdir(directoryName)
        if fname.lower().endswith('.'+extension)            
        ])
    return imagefilenameslist

#####################################################################################
# Implement required functions here
#
#
#
def generateListOfImgs(listOfTrainFiles):
    result = []
    for file in listOfTrainFiles:
        img = Image.open(file)
        print img.size
        result.append(img)

    return result

def convertImgListToNumpyData(imgList):
    shape = (1, imgList[0].size[0]*imgList[0].size[1])
    col= shape[1]
    row= len(imgList)
    matrix = np.zeros((row,col))
    #print matrix.shape
    count = 0
    for img in imgList:
        np_im=np.asfarray(img)
        np_im = np_im.reshape(shape)
        max = np_im[0,np.argmax(np_im)]
        for i in range(col):
            np_im[0,i] = np_im[0,i]/float(max)

        matrix[count] = np_im
        #np.insert(matrix, count , np_im, 0)
        count += 1
    return matrix

def calculateEigenfaces(adjfaces, width, height):
    matrix = adjfaces.T.dot(adjfaces)
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    u = adjfaces.dot(eigenvectors)
    index = eigenvalues.argsort()[::-1]
    u=u[:, index]
    return u

def transformToEigenfaceSpace(eigenfaces, face, numFeatures):
    pointToEigenspace = np.zeros(shape=(numFeatures))
    for i in range(numFeatures):
        pointToEigenspace[i]=dot((eigenfaces[:,i:i+1].T), face)
    return pointToEigenspace
####################################################################################
#Start of main programm

#Choose Directory which contains all training images 
TrainDir=tkFileDialog.askdirectory(title="Choose Directory of training images")
#Choose the file extension of the image files
Extension='png'

####################################################################################
# Implement required functionality of the main programm here


listOfTrainFiles = parseDirectory(TrainDir,Extension)
print "x"*40
imgList = generateListOfImgs(listOfTrainFiles)
print "x"*40
matrix = convertImgListToNumpyData(imgList)
print "x"*40
averageFace = np.average(matrix,0)
Image.fromarray(averageFace.reshape((220,150))*255).show()

NormedArrayOfFaces = np.subtract(matrix,averageFace)
eigenFaces = calculateEigenfaces(NormedArrayOfFaces.T, NormedArrayOfFaces.shape[1], NormedArrayOfFaces.shape[0])

allTransformed = []
for face in NormedArrayOfFaces:
    allTransformed.append(transformToEigenfaceSpace(eigenFaces,face,6))


#Choose the image which shall be recognized
testImageDirAndFilename=tkFileDialog.askopenfilename(title="Choose Image to detect")
imgToDetect = Image.open(testImageDirAndFilename)
imageList = []
imageList.append(imgToDetect)

testFace = convertImgListToNumpyData(imageList)[0]
NormedTestFace = np.subtract(testFace,averageFace)
transformedToDetect = transformToEigenfaceSpace(eigenFaces,NormedTestFace,6)

distance = sys.float_info.max
faceNumber = 0
for i, img in enumerate(allTransformed):
    tmpDist = np.linalg.norm(transformedToDetect-img)
    if (tmpDist<distance):
        distance = tmpDist
        faceNumber = i
Image.fromarray(matrix[faceNumber].reshape((220,150))*255).show()
imgToDetect.show()