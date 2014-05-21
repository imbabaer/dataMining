import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error


#read in data as dataframe
dataFrame = pd.DataFrame(pd.read_csv('effectiveRates.csv'))
print dataFrame['YHOO'];

ko      = dataFrame['KO'];
yahoo   = dataFrame['YHOO'];
mcd     = dataFrame['MCD'];
aapl    = dataFrame['AAPL'];
ba      = dataFrame['BA'];
nav     = dataFrame['NAV'];
ford    = dataFrame['F'];
pep     = dataFrame['PEP'];
amazon  = dataFrame['AMZN'];
ibm     = dataFrame['IBM'];

#parameter for sampling data
#
# startTimeDelay                      = 1; #for finding the best timeDelay
startTimeDelay                      = 10; #for finding the best c, eps
endTrainSamples                     = 650;
daysToBePredicted                   = 40;

kernel  = 'rbf'
C       = 1;
eps     = 0.349;
# best C, eps, timedelay
# c = 1, eps = 0.349, timedelay = 10


#bestStartTimeDelay = startTimeDelay # for finding best timeDelay
#bestC = C # for finding best C
#bestMae = 100.1
#bestEps = eps
#for iter in range(len(yahoo)- (endTrainSamples+daysToBePredicted)): #for finding the best timeDelay
#for iter in range(1000):

timeDelay = startTimeDelay;
startDay = endTrainSamples - startTimeDelay + 1;

features = np.zeros( ((endTrainSamples-timeDelay-1),timeDelay)  )
targets = np.zeros( (endTrainSamples-timeDelay-1)  )

for i in range(endTrainSamples-timeDelay-1):
    temp = np.zeros( timeDelay )
    for j in range(timeDelay):
        temp[j] = yahoo[i+j]

    features[i,:] = temp;
    targets[i] = yahoo[i+timeDelay]


print "TRAINING:"
svr_rbf = SVR(kernel=kernel, C=C, epsilon=eps)
svr_rbf.fit(features, targets);



data = [ x for x in yahoo[ :startDay+timeDelay ] ]
#print data
#print "len =", len(data)


for predDay in range(daysToBePredicted):
    date = startDay+predDay

    tmp2 = np.zeros( (timeDelay) )

    for k in range(timeDelay):
        tmp2[k] = data[date+k]

    #print tmp2

    #print "-"*30
    out = svr_rbf.predict(tmp2);
    data.extend(out)

    #print "IST = ", out
    #print "SOLL = ", yahoo[startDay+timeDelay]


#print len(data)
'''
startTimeDelay                      = 24;
endTrainSamples                     = 650;
daysToBePredicted                   = 60;

kernel  = 'rbf'
C       = 10;
eps     = 0.36;
'''
titleString =   "C=", C, " kernel=",kernel," eps=",eps," startTimeDelay=",startTimeDelay," daysToBePredicted=",daysToBePredicted
plt.plot(yahoo)
plt.plot(data)
plt.title(titleString)
plt.xlim(startDay+timeDelay-1,startDay+timeDelay+daysToBePredicted-1)
plt.show()



plt.plot(yahoo)
plt.plot(data)
plt.show()


#MAE
mae = mean_absolute_error(yahoo[ startDay+timeDelay+1 : startDay+timeDelay+daysToBePredicted ],data[ startDay+timeDelay+1 : startDay+timeDelay+daysToBePredicted ])
print "mae: ", mae
'''
if bestMae > mae:
   bestMae = mae
   bestEps = eps
if eps>0.001:
    eps = eps - 0.001
print eps

#for finding the best timeDelay
if bestMae > mae:
    bestMae = mae
    bestStartTimeDelay = startTimeDelay
'''

'''# for finding best C
if bestMae > mae:
    bestMae = mae
    bestC = C
'''

plt.figure(1)
plt.plot(ko,   'b-', label='Coca-Cola')
plt.plot(yahoo,'r-', label='Yahoo!')
plt.plot(mcd,  'g-', label='McDonalds')
plt.plot(pep,  'c-', label='Pepsi')
plt.plot(nav, 'm-', label='Navistar')
#plt.plot(ford, 'm-', label='Ford')
#plt.plot(aapl, 'm-', label='Apple')
#plt.plot(amazon, 'm-', label='Amazon')
#plt.plot(ibm, 'm-', label='IBM')
#plt.plot(ba, 'm-', label='Boeing')

plt.title('Aktienkurse')
plt.xlim(0,len(ko))
#plt.xticks()
plt.legend(loc='upper left')
plt.tight_layout()

plt.figure(2)
plt.xlim(0,len(ko))
plt.plot(yahoo,'m-', label='Yahoo!')
plt.legend(loc='upper left')
plt.tight_layout()

#plt.show()

#startTimeDelay = startTimeDelay + 1 # for finding the best timeDelay
#C = C + 40 # for finding the best C


#print "Best Mae:  ", bestMae, "  with eps:  ", bestEps
