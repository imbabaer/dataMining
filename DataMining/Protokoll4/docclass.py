def getwords(doc, min, max):
        tmp = {}
        dict = {}
        array = doc.lower().replace(".","").replace(",","").replace("-","").split(" ")
        #array = doc.lower().split(" ")
        for i in range(len(array)):
            if (not (array[i].__len__() < min) and (not array[i].__len__() > max)):
                dict[array[i]] = 1
        print dict
        return dict


class Classifier:

    def __init__(self, functionptr, min, max):
        self.fc = {}
        self.cc = {}
        self.getfeatures = functionptr
        self.min = min
        self.max = max

    def incf(self,f,cat):
        if f in self.fc:
            if cat in self.fc[f]:
                self.fc[f][cat] += 1
            else:
                self.fc[f][cat] = {}
                self.fc[f][cat] = 1
        else:
            self.fc[f]= {}
            self.fc[f][cat] = 1


    def incc(self,cat):
        if cat in self.cc:
            self.cc[cat] += 1
        else:
            self.cc[cat] = 1


    def fcount(self,f,cat):
        if f in self.fc:
            if cat in self.fc[f]:
                return self.fc[f][cat]

        return 0



    def catcount(self,cat):
        return self.cc[cat]

    def totalcount(self):
        total = 0
        for i in self.cc:
            total += self.cc[i]
        return total


    def train(self,item,cat):
        words = self.getfeatures(item, self.min, self.max)
        for f in words:
            self.incf(f,cat)
        self.incc(cat)

    def fprob(self,f,cat):
        ret = float(self.fcount(f,cat))/float(self.catcount(cat))
        return ret

    def weightedprob(self,f,cat):
        initprob = 0.5
        count = 0
        if f in self.fc:
            for c in self.fc[f]:
                count += self.fc[f][c]

        return ((initprob + count * self.fprob(f,cat))/(1.0 + count))

    def prob(self,item,cat):
        words = self.getfeatures(item, self.min, self.max)
        ret = 1.0
        for f in words:
            ret *= self.weightedprob(f,cat)
        ret *= (float(self.catcount(cat))/float(self.totalcount()))
        return ret


    def getCat(self,item):
        prob = 0
        catname = ''
        for cat in self.cc:
            case =  self.prob(item,cat)
            if prob < case:
                prob = case
                catname = cat

        return (catname,prob)
