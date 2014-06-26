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
    shape = A.shape
    rows = shape[0]
    cols = shape[1]
    for i in range(rows):
        for j in range(cols):
            result+= (A.item(i,j) - B.item(i,j)) ** 2
    return result

def nnmf(A,m,it):
    result = []
    H = np.random.random_integers(0, 5, (m, A.shape[1]))
    W = np.random.random_integers(0, 5, (A.shape[0],m))
    i = 0
    while i < it:
        B = W.dot(H)
        # a)
        if(cost(A,B)>=5):
            break
        # b)
        WT = W.transpose()
        HArray = np.array(H)* ( np.array(WT)*np.array(A))/(np.array(WT)*np.array(B))
        H = np.matrix(HArray.reshape(H.shape[0],H.shape[1]))

        # c)
        HT = H.transpose()
        WArray = np.array(H)* ( np.array(A)*np.array(HT))/np.array(B)*(np.array(HT))
        W = np.matrix(WArray.reshape(W.shape[0],W.shape[1]))

    result.append(W)
    result.append(H)
    return result