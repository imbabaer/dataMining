import newsfeatures as nf
import numpy as np
# get all words of all feeds, all words per article, all article titles and all article description
feedData= nf.getarticlewords()

# get article/word-matrix and wordvec
matrixData = nf.makematrix(feedData[0],feedData[1])

#write matrixData into file
f = open('WordInArt.txt', 'w')
for word in matrixData[0]:
    f.write(word + ',')
f.write('\n')
for art in matrixData[1]:
    for i in range(len(art)):
        f.write(str(art[i])+',')
    f.write('\n')

# create numpy matrix of the article/word-matrix
npWordmatrix = np.matrix(matrixData[1])


# helper function to get indices of zerolines
def getZeroLines(matrix):
    rows = matrix.shape[0]
    cols = matrix.shape[1]
    rowind = 0
    zerolines = []

    for i in range(rows):
        allzero = True
        for j in range(cols):
            if matrix.item(i,j) > 0:
                allzero = False
        if allzero:
            zerolines.append(rowind)
        rowind += 1
    return zerolines

#get zeroline indices
zerolines = getZeroLines(npWordmatrix)

#delte zerolines from the matrix and the articletitlelist
iterations = 0
for line in range(len(zerolines)):
    npWordmatrix = np.delete(npWordmatrix, zerolines[line] - iterations ,0)
    feedData[2] = np.delete(feedData[2], zerolines[line] - iterations )
    iterations +=1
zerolines = getZeroLines(npWordmatrix)

#get W and H
wh = nf.nnmf(npWordmatrix, 10, 15)

#print featurematrix, weightmatrix, and articles with given features.
nf.showfeatures(wh[0], wh[1], feedData[2], matrixData[0], [1,2,3])