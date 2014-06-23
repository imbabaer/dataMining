#Input a string text, the function lowers at first all characters. Then the characters '.' ',' and '-' are removed
# (optimization so words at the end of a sentence are not recognized as independent words.
#Then the single words are stored in a dictionary with the word as the key and 1 as value
# if they are between the min and max length.
def getwords(doc, min, max):
        tmp = {}
        dict = {}
        array = doc.lower().replace(".","").replace(",","").replace("-","").split(" ")
        for i in range(len(array)):
            if (not (array[i].__len__() < min) and (not array[i].__len__() > max)):
                dict[array[i]] = 1
        return dict


class Classifier:
    #if a classifier object is instanciated then
    #   a functionptr to a 'getwords'-function,
    #   the min length and
    #   the max length of the words that shall be considered
    # must be specified
    def __init__(self, functionptr, min, max):
        self.fc = {}
        self.cc = {}
        self.getfeatures = functionptr
        self.min = min
        self.max = max

    #this function increases the count of a specific word in a specific category
    #this function is called in the learning process
    def incf(self,f,cat):
        #if the word already exists in the dictionary
        if f in self.fc:
            #if the category already exists at this word increase the count by 1
            if cat in self.fc[f]:
                self.fc[f][cat] += 1
            #if the category does not already exist at this word, create entry with count 1
            else:
                self.fc[f][cat] = {}
                self.fc[f][cat] = 1
        #if the word does not already exist in the dictionary, create entry with category and count 1
        else:
            self.fc[f]= {}
            self.fc[f][cat] = 1

    #this function increases the count of documents in a category
    def incc(self,cat):
        #if the category already exists in the dictionary
        if cat in self.cc:
            self.cc[cat] += 1
        #if the category does not already exist, create entry with count 1
        else:
            self.cc[cat] = 1

    #this function returns the count of a specific word in a specific category.
    def fcount(self,f,cat):
        if f in self.fc:
            if cat in self.fc[f]:
                return self.fc[f][cat]
        #only if the word is not found in the dictionary or the word does not appear in that category this return
        # statement is reached and returns 0
        return 0


    # return the count of documents specified in a category
    def catcount(self,cat):
        return self.cc[cat]

    # return the total count of all documents
    def totalcount(self):
        total = 0
        for i in self.cc:
            total += self.cc[i]
        return total

    #training method which is called for each document in the trainingset
    def train(self,item,cat):
        #at first the string is splitted into single words with the function set in the constructor of the object.
        words = self.getfeatures(item, self.min, self.max)
        #for each word the incf-function is called with the corresponding category
        for f in words:
            self.incf(f,cat)
        #the count of documents in the specific category is increased
        self.incc(cat)

    #calculate the conditional probability of a word with the given category
    def fprob(self,f,cat):
        #the count of the word in the category is devided by the count of documents in that category
        ret = float(self.fcount(f,cat))/float(self.catcount(cat))
        return ret

    #function for optimazing values of the fprob-function for words
    # that do not appear often/at all in the trained documents
    def weightedprob(self,f,cat):
        initprob = 0.5
        count = 0
        #if the word exists already the count in all categories is computed
        if f in self.fc:
            for c in self.fc[f]:
                count += self.fc[f][c]

        return ((initprob + count * self.fprob(f,cat))/(1.0 + count))

    #method which is called to get the probability a document/string is in a specific category
    def prob(self,item,cat):
        #at first the string is splitted into single words with the function set in the constructor of the object.
        words = self.getfeatures(item, self.min, self.max)
        ret = 1.0
        for f in words:
            #the product of all probabilities of all words with this category is computed
            #if a word does not appear at all in the training set the product
            # of probabilities would be 0 because the single probability would be 0 (veto rights of a single word)
            # to avoid this the function weightedprob is called to avoid this
            ret *= self.weightedprob(f,cat)
        #the product is multiplied with the probability of the category
        ret *= (float(self.catcount(cat))/float(self.totalcount()))
        return ret

    #convenience method so that you have not to try out all categorys of a word
    def getCat(self,item):
        #tmp max value of the probability
        prob = 0
        #tmp category name of the according max value
        catname = ''
        #for every category the prob-function is called
        for cat in self.cc:
            case =  self.prob(item,cat)
            #if the probability in this category is higher then the stored max value (in the beginning 0) then this
            # probability is stored in the max value and the according category name is stored to
            if prob < case:
                prob = case
                catname = cat
        #a tuple of categoryname and probability value is returned
        return (catname,prob)
