from pylab import scatter,text,show
from sklearn import manifold, datasets
import pandas as pd

digits = pd.DataFrame(pd.read_csv('EnergyMix.csv'))
X = pd.DataFrame(pd.read_csv('EnergyMix.csv'), columns=['Oil','Gas','Coal','Nuclear','Hydro'])
target = digits['Country']

Y = manifold.Isomap(5, 2).fit_transform(X)

scatter(Y[:,0], Y[:,1], c='k', alpha=0.3, s=10)
for i in range(Y.shape[0]):
 text(Y[i, 0], Y[i, 1], str(target[i]))

show()

