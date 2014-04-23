import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.svm as skl

dataFrame = pd.DataFrame(pd.read_csv('EnergyMix.csv'))

classifier = skl.SVC(gamma=0.001)
print classifier
