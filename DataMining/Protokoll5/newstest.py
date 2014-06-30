import newsfeatures as nf
import numpy as np
articlesNStuff= nf.getarticlewords()

something = nf.makematrix(articlesNStuff[0],articlesNStuff[1])


f = open('WordInArt.txt', 'w')

for word in something[0]:
    f.write(word + ',')
f.write('\n')

for art in something[1]:
    for i in range(len(art)):
        f.write(str(art[i])+',')
    f.write('\n')

# 224
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
npWordmatrix = np.matrix(something[1])
#print type(something[1])
#print type(npWordmatrix)



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

#print len(npWordmatrix)
#print len(articlesNStuff[2])

zerolines = getZeroLines(npWordmatrix)
#print zerolines

iterations = 0
for line in range(len(zerolines)):
    npWordmatrix = np.delete(npWordmatrix, zerolines[line] - iterations ,0)
    articlesNStuff[2] = np.delete(articlesNStuff[2], zerolines[line] - iterations )
    iterations +=1
zerolines = getZeroLines(npWordmatrix)
#print zerolines

#print len(npWordmatrix)
#print len(articlesNStuff[2])
#npWordmatrix.shape[0]/2
wh = nf.nnmf(npWordmatrix, 10, 15)

nf.showfeatures(wh[0], wh[1], articlesNStuff[2], something[0], [1,2,3])