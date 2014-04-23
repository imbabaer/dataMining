import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
s = pd.Series([1, 3, 5, np.nan, 6, 8])
print "print s"
print s

dates = pd.date_range('20130101',periods=6)
print "print dates"
print dates

df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
print "print df"
print df

df2 = pd.DataFrame({ 'A' : 1.,
                     'B' : pd.Timestamp('20130102'),
                     'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                     'D' : np.array([3] * 4,dtype='int32'),
                     'E' : 'foo' })

print "print df2"
print df2

print "print df2.dtypes"
print df2.dtypes

print "print df.head()"
print df.head()

print "print df.tail(2)"
print df.tail(2)

print "print df.index"
print df.index

print "print df.columns"
print df.columns

print "print df.values"
print df.values

print "print df.describe()"
print df.describe()

print "print df.T"
print df.T

print "print df.sort(columns='B')"
print df.sort(columns='B')

print "print df['A']"
print df['A']

print "print df[0:3]"
print df[0:3]

print "print df['20130102':'20130104']"
print df['20130102':'20130104']

print "print df.loc[dates[0]]"
print df.loc[dates[0]]

print "print df.loc[:,['A','B']]"
print df.loc[:,['A','B']]

print "print df.loc['20130102':'20130104',['A','B']]"
print df.loc['20130102':'20130104',['A','B']]

print "print df.loc['20130102',['A','D']]"
print df.loc['20130102',['A','D']]

print "print df.iloc[3:5,0:2]"
print  df.iloc[3:5,0:2]

print "print x = list('abcdef')"
x = list('abcdef')
print x


print "print s1 = pd.Series([1,2,3,4,5,6],index=pd.date_range('20130102',periods=6))"
s1 = pd.Series([1,2,3,4,5,6],index=pd.date_range('20130102',periods=6))
print s1

df1 = df.reindex(index=dates[0:4],columns=list(df.columns) + ['E'])

print "print  pd.isnull(df1)"
print  pd.isnull(df1)

print "print df.mean()"
print df.mean()

print "print df.apply(np.cumsum)"
print df.apply(np.cumsum)

s = pd.Series(np.random.randint(0,7,size=10))
print "print s"
print s

print "s.value_counts()"
print s.value_counts()

s = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat'])
print "print s.str.lower()"
print s.str.lower()

df = pd.DataFrame(np.random.randn(10, 4))
print "print df"
print df

pieces = [df[:3], df[3:7], df[7:]]
print "print pd.concat(pieces)"
print pd.concat(pieces)

left = pd.DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]})
right = pd.DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})

print "print left and right"
print left
print right

print "pd.merge(left, right, on='key')"
print pd.merge(left, right, on='key')

ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
print "print ts.plot()"
print ts.plot()
plt.show()

'''
df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index,
                    columns=['A', 'B', 'C', 'D'])

df = df.cumsum()
print "print plt.figure()"
print plt.figure()
print "print plt.plot()"
print df.plot()
print "print plt.legend(loc='best')"
print plt.legend(loc='best')'''
