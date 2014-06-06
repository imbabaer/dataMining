import docclass as doc

print "Tests for docclass.py"

strings = [ ('nobody owns the, water.', 'g'),
            ('the quick- rabbit jumps fences','g'),
            ('buy pharmaceuticals now','b'),
            ('make quick money at the online casino','b'),
            ('the quick brown fox jumps','g'),
            ('next meeting is at night','g'),
            ('meeting with your superstar','b'),
            ('money like water','b')
]

classifier = doc.Classifier(doc.getwords,3,20)

for s in strings:
    classifier.train(s[0],s[1])

toCheck = 'the money jumps'

probg = classifier.prob(toCheck,'g')
probb = classifier.prob(toCheck,'b')

print probg
print probb

print classifier.getCat(toCheck)
print classifier.getCat('datamining at night')
print classifier.getCat('go to the casino with quick money')