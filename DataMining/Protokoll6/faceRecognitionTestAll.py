import faceRecognition as fr
import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
import tkFileDialog
from PIL import Image

#set directories which contains all training and test images
TrainDir=tkFileDialog.askdirectory(title="Choose Directory of training images")
TestDir =tkFileDialog.askdirectory(title="Choose Directory of test images")

#Choose the file extension of the image files
Extension='png'
numFeatures = 8

#TRAININGPHASE
#get list of full file names
listOfTrainFiles    = fr.parseDirectory(TrainDir,Extension)
listOfTestFiles     = fr.parseDirectory(TestDir,Extension)

#get list of Image objects from filename list
imgTrainList    = fr.generateListOfImgs(listOfTrainFiles)
imgTestList     = fr.generateListOfImgs(listOfTestFiles)

#convert all images into numpy arrays
matrix = fr.convertImgListToNumpyData(imgTrainList)

#calculate the average face of all faces
averageFace = np.average(matrix,0)

#show averageFace
avgFaceImg = averageFace.reshape((220,150))*255
Image.fromarray(avgFaceImg).show()
#save averageFace into file
cv2.imwrite('results/%s_avgFace.png' %(numFeatures), avgFaceImg)

#get averagefree faces
NormedArrayOfFaces = np.subtract(matrix,averageFace)
#calculate eigenfaces
eigenFaces = fr.calculateEigenfaces(NormedArrayOfFaces.T, NormedArrayOfFaces.shape[1], NormedArrayOfFaces.shape[0])
#transform all trainingfaces into eigenface-space
allTransformed = []
for face in NormedArrayOfFaces:
    allTransformed.append(fr.transformToEigenfaceSpace(eigenFaces,face,numFeatures))

allDistances = []

#TESTPHASE
#test every image in test folder
for testImgIdx in range( len(imgTestList) ):
    #get test image
    imgToDetect = imgTestList[testImgIdx]
    #get image file name and remove directory, slash and extension
    imageName = listOfTestFiles[testImgIdx]
    imageName = imageName.replace('.png', '')
    imageName = imageName.replace('\\', '')
    TestDir     = TestDir.replace('/', '')
    imageName = imageName.replace(TestDir, '')

    #append imgToDetect to a list to reuse functions from above
    imageList = []
    imageList.append(imgToDetect)
    #get numpyarray of image
    testFace = fr.convertImgListToNumpyData(imageList)[0]
    #get averagefree face
    NormedTestFace = np.subtract(testFace,averageFace)
    #transform testface into eigenface-space
    transformedToDetect = fr.transformToEigenfaceSpace(eigenFaces,NormedTestFace,numFeatures)

    #set distance to max
    distance = sys.float_info.max
    faceNumber = 0
    #calculate distance from testface to every trainingface and store index if distance is smaller than current distance
    for i, img in enumerate(allTransformed):
        tmpDist = np.linalg.norm(transformedToDetect-img)
        if (tmpDist<distance):
            distance = tmpDist
            faceNumber = i

    #show trainingimage with min distance
    trainFaceImg = matrix[faceNumber].reshape((220,150))*255
    cv2.imwrite('results/%s_%s_%s.png' %(numFeatures, imageName, distance), trainFaceImg)

    #show test image
    #imgToDetect.show()
    #print imageName
    allDistances.append(distance)
    print "Distance of test image and found training image: ",distance

distBox = plt.boxplot(allDistances,0,'rs',0)
plt.title('All Distances')
plt.show()