import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.svm as skl
from sklearn.feature_selection import *
from sklearn.utils.multiclass import unique_labels
from sklearn.cross_validation import cross_val_score
from sklearn import metrics

digits = pd.DataFrame(pd.read_csv('EnergyMix.csv'))
#print digits
features = (np.array(pd.DataFrame(pd.read_csv('EnergyMix.csv'), columns=['Oil','Gas','Coal','Nuclear','Hydro']).values))
target = (np.array(digits['CO2Emm'].values))

print"\n\n############## Approach 4: SVM-Regression with 10-fold crossvalidation #########################"
regressor4 = skl.SVR(kernel='linear', C=1, epsilon=0.1)
print'----- Mean Square Error Score for SVM Regression ------------'
scores = cross_val_score(regressor4, features,target,cv=10,score_func=metrics.mean_squared_error)
print scores
print "Cross Validation Score: %0.3f (+/- %0.3f)" % (scores.mean(), scores.std() / 2)
regressor4.fit(features,target)
print regressor4.coef_
print "####Target####"
print target



print "####Prediction####"
pred = regressor4.predict(features)
print pred

from math import fabs

mediantar = sorted(target)[len(target)//2]
print mediantar
for b in target:
    mad = fabs(b - mediantar)
    print b,mad

medianpred = sorted(pred)[len(pred)//2]
print medianpred
for c in pred:
    madp = fabs(c-medianpred)
    print c,madp

'''
epsilonsvr = skl.SVC(kernel="linear")

print epsilonsvr

from sklearn import cross_validation
kf = cross_validation.KFold(65,n_folds=10)
print len(kf)
print kf
for train_index, test_index in kf:
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = target[train_index], target[test_index]



epsilonsvr.fit(X,target)
#print digits['CO2Emm'].values
print epsilonsvr.predict(X)
'''

'''
weights = [220.01015147, 46.00222955, 378.26688078, 34.57208601, 79.04540111]

classifier.fit(X,target)
print classifier
print classifier.score(X,target)

from sklearn import cross_validation
X = np.array([[1, 2], [3, 4], [1, 2], [3, 4],[5,9],[5,3],[8,1],[6,3],[1,2],[1,7]])
y = np.array([1, 2, 3, 4,5,6,7,8,9,10])
kf = cross_validation.KFold(10, n_folds=10)

print(kf)
for train_index, test_index in kf:
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
'''
