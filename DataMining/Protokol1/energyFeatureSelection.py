import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, svm
from sklearn.feature_selection import SelectPercentile, f_classif
import sklearn as skl
from sklearn.feature_selection import SelectKBest

dataFrame = pd.DataFrame(pd.read_csv('EnergyMixGeo.csv'))
#print dataFrame

countries = dataFrame.values[:,1]
target = dataFrame.values[:,8]
#print countries
dataFrame = dataFrame.drop("Country", 1)
dataFrame = dataFrame.drop("Total2009", 1)
dataFrame = dataFrame.drop("CO2Emm", 1)

def f_regression(X,Y):
   import sklearn
   return sklearn.feature_selection.f_regression(X,Y,center=False) #center=True (the default) would not work ("ValueError: center=True only allowed for dense data") but should presumably work in general

from sklearn.feature_selection import SelectKBest
featureSelector = SelectKBest(f_regression,3)
featureSelector.fit(dataFrame.values,target)

print featureSelector.scores_
print featureSelector.pvalues_
print featureSelector.k