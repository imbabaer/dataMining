import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pylab import *

dataNuclear = pd.DataFrame(pd.read_csv('EnergyMix.csv'), columns=['Nuclear'])

dataNuclear.describe()

print dataNuclear


dataFrame = pd.DataFrame(pd.read_csv('EnergyMix.csv'))

o = dataFrame['Oil'].describe()
g = dataFrame['Gas'].describe()
c = dataFrame['Coal'].describe()
n = dataFrame['Nuclear'].describe()
h = dataFrame['Hydro'].describe()

boxplot(o,0,'rs',0)
plt.title('Oil')
plt.show()

boxplot(g,0,'rs',0)
plt.title('Gas')
plt.show()

boxplot(c,0,'rs',0)
plt.title('Coal')
plt.show()

boxplot(n,0,'rs',0)
plt.title('Nuclear')
plt.show()

boxplot(h,0,'rs',0)
plt.title('Hydro')
plt.show()
