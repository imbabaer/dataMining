from os.path import isdir,join,normpath
from os import listdir
from PIL import Image

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
    matrix = adjfaces.dot(adjfaces.T)
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)

    eigenvalues, eigenvectors = zip(*sorted(zip(eigenvalues, eigenvectors),reverse=True))


    return np.array(eigenvectors)


####################################################################################
#Start of main programm

#Choose Directory which contains all training images 
TrainDir=tkFileDialog.askdirectory(title="Choose Directory of training images")
#Choose the file extension of the image files
Extension='png' 
#Choose the image which shall be recognized
testImageDirAndFilename=tkFileDialog.askopenfilename(title="Choose Image to detect")

####################################################################################
# Implement required functionality of the main programm here


listOfTrainFiles = parseDirectory(TrainDir,Extension)
print "x"*40
imgList = generateListOfImgs(listOfTrainFiles)
print "x"*40
matrix = convertImgListToNumpyData(imgList)
print "x"*40

averageFace = np.average(matrix,0)
print averageFace
print "x"*40
print matrix.shape
print "x"*40
NormedArrayOfFaces = np.subtract(matrix,averageFace)
print NormedArrayOfFaces.shape
print "x"*40
eigenFaces = calculateEigenfaces(NormedArrayOfFaces, NormedArrayOfFaces.shape[1], NormedArrayOfFaces.shape[0])
print eigenFaces.shape

Usub = np.zeros((63,6))
for i in range(6):
    print eigenFaces[i]
    print "o"*40
    Usub[:,i]=eigenFaces[i]

print Usub
print NormedArrayOfFaces.shape

transformed = np.zeros((63,6))
for i in range(63):
    for j in range(6):
        print type(Usub)
        print type(Usub[:,j])
        print Usub[:,j].shape
        print NormedArrayOfFaces[i].shape
        transformed[i,j]= NormedArrayOfFaces[i].reshape(1,33000).dot(Usub[:,j].reshape((63,1)))

print transformed.shape