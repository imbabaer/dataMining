import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.svm as skl
from sklearn.feature_selection import *
#from sklearn.utils.multiclass import unique_labels
from sklearn.cross_validation import cross_val_score
from sklearn import metrics

digits = pd.DataFrame(pd.read_csv('EnergyMixGeo.csv'))
#print digits
features = (np.array(pd.DataFrame(digits, columns=['Oil','Gas','Coal','Nuclear','Hydro']).values))
target = (np.array(digits['CO2Emm'].values))

iwas = []

#for durchl in range(10):
print"\n\n############## Approach 4: SVM-Regression with 10-fold crossvalidation #########################"
regressor4 = skl.SVR(kernel='linear', C=100, epsilon=0.4)
print'----- Mean Square Error Score for SVM Regression ------------'
scores = cross_val_score(regressor4, features,target,cv=10,score_func=metrics.mean_squared_error,verbose=50)
print scores
    #iwas.append(scores)

#print iwas



print "Cross Validation Score: %0.3f (+/- %0.3f)" % (scores.mean(), scores.std() / 2)
regressor4.fit(features,target)
print "####Koeffizienten####"
print regressor4.coef_
print regressor4.intercept_
print "####Target####"
print target


print "####Prediction####"
pred = regressor4.predict(features)
print pred
error=pred-target
plt.stem(np.arange(len(target)),error)
plt.title('Prediction Error')
plt.show()

print '####MAD####'
mad = 1.0/len(target) *metrics.pairwise.manhattan_distances(pred,target)
print "%2.30f" % mad
