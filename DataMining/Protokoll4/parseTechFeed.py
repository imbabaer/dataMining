import feedparser
import docclass as doc


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


trainTech=['http://rss.chip.de/c/573/f/7439/index.rss',
           #commented out so that we have equal size of training samples of tech and nonTech documents
           #'http://feeds.feedburner.com/netzwelt',
           #'http://rss1.t-online.de/c/11/53/06/84/11530684.xml',
           'http://www.computerbild.de/rssfeed_2261.xml?node=13',
           'http://www.heise.de/newsticker/heise-top-atom.xml']

trainNonTech=['http://newsfeed.zeit.de/index',
              'http://newsfeed.zeit.de/wirtschaft/index',
              'http://www.welt.de/politik/?service=Rss',
              'http://www.spiegel.de/schlagzeilen/tops/index.rss',
              'http://www.sueddeutsche.de/app/service/rss/alles/rss.xml'
              ]
test=[
        "http://rss.golem.de/rss.php?r=sw&feed=RSS0.91",
        #'http://newsfeed.zeit.de/politik/index',
        #'http://www.welt.de/?service=Rss'
           ]

countnews={}
countnews['tech']=0
countnews['nontech']=0
countnews['test']=0

#create classifier with function 'getwords', minlength = 3, maxlength = 20
classifier = doc.Classifier(doc.getwords,3,20)

countTechCat = 0
countNonTechCat = 0

print "--------------------News from trainTech------------------------"
for feed in trainTech:
    f=feedparser.parse(feed)
    for e in f.entries:
      print '\n---------------------------'
      fulltext=stripHTML(e.title+' '+e.description)
      print fulltext
      #train the classifier with fulltext and category 'Tech'
      classifier.train(fulltext,'Tech')
      countnews['tech']+=1
print "----------------------------------------------------------------"
print "----------------------------------------------------------------"
print "----------------------------------------------------------------"

print "--------------------News from trainNonTech------------------------"
for feed in trainNonTech:
    f=feedparser.parse(feed)
    for e in f.entries:
      print '\n---------------------------'
      fulltext=stripHTML(e.title+' '+e.description)
      print fulltext
      #train the classifier with fulltext and category 'NonTech'
      classifier.train(fulltext,'NonTech')
      countnews['nontech']+=1
print "----------------------------------------------------------------"
print "----------------------------------------------------------------"
print "----------------------------------------------------------------"

print "--------------------News from test------------------------"
for feed in test:
    f=feedparser.parse(feed)
    for e in f.entries:
      print '\n---------------------------'
      fulltext=stripHTML(e.title+' '+e.description)
      print fulltext
      #get the category and the probability of the fulltext
      ret = classifier.getCat(fulltext)
      #count the tech and nonTech categorized documents
      if ret[0]=='Tech':
            countTechCat +=1
      else:
          countNonTechCat +=1
      print ret
      countnews['test']+=1
print "----------------------------------------------------------------"
print "----------------------------------------------------------------"
print "----------------------------------------------------------------"

print 'Number of used trainings samples in categorie tech',countnews['tech']
print 'Number of used trainings samples in categorie notech',countnews['nontech']
print 'Number of used test samples',countnews['test']
print '--'*30
#print the categorized test documents
print "count Tech:", countTechCat, " [",(float(countTechCat)/float((countTechCat+countNonTechCat)))*100,"% ]"
print "count NonTech:", countNonTechCat, " [",(float(countNonTechCat)/float((countTechCat+countNonTechCat)))*100,"% ]"

