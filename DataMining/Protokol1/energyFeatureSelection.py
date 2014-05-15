import pandas as pd
import numpy as np
from sklearn.feature_selection import *

digits = pd.DataFrame(pd.read_csv('EnergyMixGeo.csv'))
print digits
X = (np.array(pd.DataFrame(digits, columns=['Oil','Gas','Coal','Nuclear','Hydro']).values))
target = (np.array(digits['CO2Emm'].values))

print X
print '----------'
print target

selector = SelectKBest(f_regression, k=3)
selector.fit(X, target)

print selector.scores_
