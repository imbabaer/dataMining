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

# get all words of all feeds, all words per article, all article titles and all article description
def getarticlewords():
    #instantiate new lists and dictionaries
    result = []
    allwords = {}
    articlewords = []
    articletitles = []
    articledexription = []
    i = 0

    #parse every feed
    for feed in feedlist:
        f=feedparser.parse(feed)
        #for every article in the feed
        for e in f.entries:
            articlewords.append({})
            #remove html tags
            title=stripHTML(e.title)
            #remove html tags
            description = stripHTML(e.description)
            #concatinate title and description to one string
            fulltext = title + " " + description
            #get array of the single words
            seperatedWords = seperatewords(fulltext)

            #increase counter of word in allwords and articlewords, if not existent create entry
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


    #concatinate result array
    result.append(allwords)
    result.append(articlewords)
    result.append(articletitles)
    result.append(articledexription)
    return result

def makematrix(allw, articlew):
    #instantiate arrays
    result = []
    wordvec= []
    wordInArt = []
    totalArticles = len(articlew)

    #check every word if conditions are met for adding to the wordvec
    for word in allw:
        wordCount = 0
        for art in articlew:
            if word in art:
                wordCount +=1
        if allw[word]>=4 and float(wordCount)/float(totalArticles) <= 0.6:
            wordvec.append(word)

    #create article/word-matrix
    for art in articlew:
        tmpLine = []
        for word in wordvec:
            if word in art:
                tmpLine.append(art[word])
            else:
                tmpLine.append(0)

        wordInArt.append(tmpLine)


    #concatinate result
    result.append(wordvec)
    result.append(wordInArt)
    return result

# calculate sum of the squared difference of matrix A and B
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
    #instantiate H,W
    result = []
    H = np.random.rand(m, A.shape[1])
    W = np.random.rand(A.shape[0], m)
    print H.shape
    print W.shape
    i = 0

    #adjust H,W after calculating costs if limit is not met
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

#helping function for sorting tuples
def getKey(item):
    return item[0]

def showfeatures(w, h, titles, wordvec, featureIndices, nWords=6, nFeatures = 3, nArticles = 3):
    # Show results of featurematrix with given conditions
    print "Merkmalsmatrix:"
    print "x"*60
    selectedFeatureList = []
    for i in range(h.shape[0]):
        mList = []
        #collect list of words and its quantitiy
        for j in range(len(h[i])):
            mList.append((h[i][j] ,wordvec[j]))
        #reverse sort list
        mList = sorted(mList, key=getKey, reverse=True)

        # print number of desired words per feature and append the words to tmpList
        tmpList = []
        for f in range(nWords):
            print mList[f]
            tmpList.append(mList[f])
        print ".."*30

        #add list with reduced amount of words
        selectedFeatureList.append(tmpList)

    # Show results of weightmatrix with given conditions
    print "Gewichtsmatrix:"
    print "x"*60
    allArticles = []
    for artIndex in range(w.shape[0]):
        gList = []
        allFeatures = []
        #collect list of weight, article title, featurevector and feature index
        for featureInd in range(len(w[artIndex])):
            gList.append((w[artIndex][featureInd],titles[artIndex], selectedFeatureList[featureInd], featureInd))
        #reverse sort list
        gList = sorted(gList, key=getKey,reverse=True)

        #print number of desired features per article
        print titles[artIndex] + ": \n"
        #show n best Features for articles
        for f in range(nFeatures):
            allFeatures.append(gList[f][3])
            #show feature words
            output = ""
            for word in gList[f][2]:
                output += word[1] + ", "
            print output
        print ".."*30
        allArticles.append((gList,allFeatures))

    # show number of desired articles containing given features and their features
    print "Zusatsaufgabe: "
    #for every given featureIndex
    for featureIndex in range(len(featureIndices)):
        featureWords = ""
        #get feature words
        for word in selectedFeatureList[featureIndices[featureIndex]]:
            featureWords += word[1] + ", "
        print "_"*50
        print "Die Merkmale "
        print featureWords
        print "sind in folgenden Artikeln enthalten:\n"

        allArticlesWithFeature = []
        #search for every article that contains the specific feature
        for article in allArticles:
            for feature in article[1]:
                #if featureIndex is contained in the article, append article to allArticlesWithFeature
                if featureIndices[featureIndex] == feature:
                    #add article title to list
                    allArticlesWithFeature.append(article[0][1][1])


        #show desired number of allArticles
        for i in range(nArticles):
            print allArticlesWithFeature[i]
        print ''
        print ''
