'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, svm
from sklearn.feature_selection import SelectPercentile, f_classif
import sklearn as skl
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import *
from sklearn.utils.multiclass import unique_labels


dataFrame = pd.DataFrame(pd.read_csv('EnergyMixGeo.csv'))
#print dataFrame

countries = dataFrame.values[:,1]
target = dataFrame.values[:,8]
#print countries
dataFrame = dataFrame.drop("Country", 1)
dataFrame = dataFrame.drop("Total2009", 1)
dataFrame = dataFrame.drop("CO2Emm", 1)

from sklearn.feature_selection import SelectKBest
featureSelector = SelectKBest(f_regression,3)
featureSelector.fit(dataFrame.values,target)

print featureSelector.scores_
print featureSelector.pvalues_
print featureSelector.k
'''

import pandas as pd
import numpy as np
from sklearn.feature_selection import *
from sklearn.utils.multiclass import unique_labels

digits = pd.DataFrame(pd.read_csv('EnergyMix.csv'))
print digits
X = (np.array(pd.DataFrame(pd.read_csv('EnergyMix.csv'), columns=['Oil','Gas','Coal','Nuclear','Hydro']).values))
target = (np.array(digits['CO2Emm'].values))

print X
print '----------'
print target

selector = SelectKBest(f_regression, k=3)
selector.fit(X, target)

print selector.scores_
#score = selector.scores(X, target)

#print score
