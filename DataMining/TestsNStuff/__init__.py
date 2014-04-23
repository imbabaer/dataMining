import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

nparray = np.array([1,2,3,5,5])
print nparray

s = pd.Series([1,3,5,np.nan,6,8])
print s
indices = ["never","gonna","give","you","up"]
df = pd.DataFrame(nparray,index=indices,columns=list('A'))
print df
print df.A
print df['A']
print df[0:1]
print df['never':'give']
print df
print df.loc[indices[0]]
print df.iloc[3]

df['f']=[0,0,0,0,0]
print df
df.sort_index(axis=0, ascending=True)
print df

s = pd.Series([1, 3, 5, np.nan, 6, 8])
print "print s"
print s

dates = pd.date_range('20130101',periods=6)
print "print dates"
print dates

df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
print df

print df.sort(columns='A')
df.sort_index(axis=1, ascending=False)
print df
df.to_csv('foo.csv')

