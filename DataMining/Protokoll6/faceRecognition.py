from os.path import isdir,join,normpath
from os import listdir
from PIL import Image
import numpy as np
import cv2
from numpy import asfarray,dot,argmin,zeros

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
#open all images of the listOfTrainFiles, and return a list of Image objects
def generateListOfImgs(listOfTrainFiles):
    result = []
    for file in listOfTrainFiles:
        img = Image.open(file)
        print img.size
        result.append(img)

    return result

#gets a list of Image objects, returns the images as numpy arrays in a list
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
        #norm the values in range of 0..1
        for i in range(col):
            np_im[0,i] = np_im[0,i]/float(max)
        matrix[count] = np_im
        count += 1
    return matrix

#returns the eigenfaces of the input matrix
def calculateEigenfaces(adjfaces, width, height):
    matrix = adjfaces.T.dot(adjfaces)
    #gets eigenfaces of XT*X
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    #mulitply the eigenvectors with X for getting the eigenvectors of X
    u = adjfaces.dot(eigenvectors)
    #"change" order of the sort
    index = eigenvalues.argsort()[::-1]
    u=u[:, index]
    return u

#returns the transformed face in eigenface-space, gets eigenfaces, the face that should be transformed and the number of relevant eigenfaces
def transformToEigenfaceSpace(eigenfaces, face, numFeatures):
    pointToEigenspace = np.zeros(shape=(numFeatures))
    for i in range(numFeatures):
        pointToEigenspace[i]=dot((eigenfaces[:,i:i+1].T), face)
    return pointToEigenspace