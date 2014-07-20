import faceRecognition as fr
import tkFileDialog
import numpy as np
import sys
from PIL import Image
import cv2

#Choose Directory which contains all training images
TrainDir=tkFileDialog.askdirectory(title="Choose Directory of training images")
#Choose the file extension of the image files
Extension='png'
numFeatures = 8

#TRAININGPHASE
#get list of full filenames
listOfTrainFiles = fr.parseDirectory(TrainDir,Extension)
#get list of Image objects from filename list
imgList = fr.generateListOfImgs(listOfTrainFiles)
#convert all images into numpy arrays
matrix = fr.convertImgListToNumpyData(imgList)
#calculate the average face of all faces
averageFace = np.average(matrix,0)
#show averageFace and save to file
avgFaceImg = averageFace.reshape((220,150))*255
Image.fromarray(avgFaceImg).show()
cv2.imwrite('results/%s_avgFace.png' %(numFeatures), avgFaceImg)

#get averagefree faces
NormedArrayOfFaces = np.subtract(matrix,averageFace)
'''
#show all averagefree training faces
for face in NormedArrayOfFaces:
    Image.fromarray(face.reshape((220,150))*255).show()
'''
#calculate eigenfaces
eigenFaces = fr.calculateEigenfaces(NormedArrayOfFaces.T, NormedArrayOfFaces.shape[1], NormedArrayOfFaces.shape[0])
#transform all trainingfaces into eigenface-space
allTransformed = []
for face in NormedArrayOfFaces:
    allTransformed.append(fr.transformToEigenfaceSpace(eigenFaces,face,numFeatures))


#TESTPHASE
#Choose the image which shall be recognized
testImageDirAndFilename=tkFileDialog.askopenfilename(title="Choose Image to detect")
imgToDetect = Image.open(testImageDirAndFilename)
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

#show training image with min distance and save to file
trainFaceImg = matrix[faceNumber].reshape((220,150))*255
Image.fromarray(trainFaceImg).show()
cv2.imwrite('results/%s_best_match_%s.png' %(numFeatures, distance), trainFaceImg)
#show test image
imgToDetect.show()
#show distance
print "Distance of test image and found training image: ",distance