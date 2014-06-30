import numpy as np
import feedparser
from nltk.corpus import stopwords
import re
sw = stopwords.words('english')
def seperatewords(text):
    splitter = re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s)>4 and s not in sw]


def stripHTML(h):
  p=''
  s=0
  for c in h:
    if c=='<': s=1
    elif c=='>':
      s=0
      p+=' '
    elif s==0:
      p+=c
  return p

feedlist =[ 'http://feeds.reuters.com/reuters/topNews',
'http://feeds.reuters.com/reuters/businessNews',
'http://feeds.reuters.com/reuters/worldNews',
'http://feeds2.feedburner.com/time/world',
'http://feeds2.feedburner.com/time/business',
'http://feeds2.feedburner.com/time/politics',
'http://rss.cnn.com/rss/edition.rss',
'http://rss.cnn.com/rss/edition_world.rss',
'http://newsrss.bbc.co.uk/rss/newsonline_world_edition/business/rss.xml',
'http://newsrss.bbc.co.uk/rss/newsonline_world_edition/europe/rss.xml',
'http://www.nytimes.com/services/xml/rss/nyt/World.xml'
'http://www.nytimes.com/services/xml/rss/nyt/Economy.xml'
]
'''
for feed in feedlist:
    fp=feedparser.parse(feed)
    print type(fp)
    for e in fp.entries:
        ti=stripHTML(e.title)
        de = stripHTML(e.description)
        print ti
        print de
        print " "
        print "--x"*20
'''

def getarticlewords():
    result = []
    allwords = {}
    articlewords = []
    articletitles = []
    articledexription = []
    i = 0
    for feed in feedlist:
        f=feedparser.parse(feed)
        #print type(f)

        for e in f.entries:
            articlewords.append({})
            title=stripHTML(e.title)
            description = stripHTML(e.description)
            fulltext = title + " " + description
            seperatedWords = seperatewords(fulltext)
            for word in seperatedWords:
                if word in articlewords[i]:
                    articlewords[i][word] += 1
                    allwords[word] += 1
                else:
                    articlewords[i][word] = 1
                    if word in allwords:
                        allwords[word] += 1
                    else:
                        allwords[word] = 1

            articletitles.append(title)
            articledexription.append(description)
            i+=1



    result.append(allwords)
    result.append(articlewords)
    result.append(articletitles)
    result.append(articledexription)
    return result

def makematrix(allw, articlew):
    result = []
    wordvec= []
    wordInArt = []
    totalArticles = len(articlew)

    for word in allw:
        wordCount = 0
        for art in articlew:
            if word in art:
                wordCount +=1
        if allw[word]>=4 and float(wordCount)/float(totalArticles) <= 0.6:
            wordvec.append(word)

    for art in articlew:
        tmpLine = []
        allzero = True
        for word in wordvec:
            if word in art:
                tmpLine.append(art[word])
                allzero = False
            else:
                tmpLine.append(0)

        #if ~allzero:
        wordInArt.append(tmpLine)



    result.append(wordvec)
    result.append(wordInArt)
    return result

def cost(A,B):
    result=0
    rows = A.shape[0]
    cols = A.shape[1]
    for i in range(rows):
        for j in range(cols):
            result+= (A.item(i,j) - B.item(i,j)) ** 2
    #print result
    return result

def nnmf(A,m,it):
    result = []
    H = np.random.rand(m, A.shape[1])
    W = np.random.rand(A.shape[0], m)
    print H.shape
    print W.shape
    i = 0
    while i < it:
        B = W.dot(H)
        k = cost(A,B)
        # a)
        if(k<=5):
            print(k)
            break

        # b)
        temH = H.copy()
        H = np.array(H)*( (np.array(W.T.dot(A))) / (np.array(W.T.dot(W).dot(H))) )

        # c)
        W = np.array(W)*( (np.array(A.dot(H.T))) / (np.array(W.dot(H).dot(H.T))) )
        i+= 1
    result.append(W)
    result.append(H)
    return result

def getKey(item):
    return item[0]

def showfeatures(w, h, titles, wordvec, featureIndices, nWords=6, nFeatures = 3, nArticles = 3):
    # Merkmalsmatrix
    print "Merkmalsmatrix:"
    print "xx"*30
    merkmale = []
    for i in range(h.shape[0]):
        mList = []
        for j in range(len(h[i])):
            mList.append((h[i][j] ,wordvec[j]))

        mList = sorted(mList, key=getKey, reverse=True)
        tmpList = []
        for f in range(nWords):
            print mList[f]
            tmpList.append(mList[f])
        print ".."*30

        merkmale.append(tmpList)
    print " "
    print merkmale
    print " "

    # Gewichtsmatrix
    print "Gewichtsmatrix:"
    print "xx"*30
    allArticles = []
    for artIndex in range(w.shape[0]):
        gList = []
        allFeatures = []
        for featureInd in range(len(w[artIndex])):
            gList.append((w[artIndex][featureInd],(titles[artIndex], merkmale[featureInd], featureInd)))
        gList = sorted(gList, key=getKey,reverse=True)

        print titles[artIndex] + ": \n"
        #show n best Features for articles
        for f in range(nFeatures):
            allFeatures.append(gList[f][1][2])
            #show feature words
            output = ""
            for word in gList[f][1][1]:
                output += word[1] + ", "
            print output
        print ".."*30
        allArticles.append((gList,allFeatures))

    print "Zusatsaufgabe: "
    for featureIndex in range(len(featureIndices)):
        featureWords = ""
        for word in merkmale[featureIndices[featureIndex]]:
            featureWords += word[1] + ", "
        print "_"*50
        print "Die Merkmale "
        print featureWords
        print "sind in folgenden Artikeln enthalten:\n"

        allArticlesWithFeature = []
        for article in allArticles:
            #featureIndex list of the article

            for feature in article[1]:
                #if featureIndex is contained in article[3], append article to allArticlesWithFeature
                if featureIndices[featureIndex] == feature:
                    allArticlesWithFeature.append(article[0][1][1][0])


        #show nArticles of allArticles
        for i in range(nArticles):
            print allArticlesWithFeature[i]
        print ''
        print ''

    return (mList, gList)
