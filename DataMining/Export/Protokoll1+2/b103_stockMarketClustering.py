"""
Created on 26.02.2012

@author: maucher

This version applies cleaned data provided by matplotlib.finance

In the cleaned data also the "open" value is adjusted w.r.t. splits and dividends

"""

print __doc__


import datetime
from matplotlib import finance
import numpy as np
from matplotlib import pyplot as plt

from sklearn import cluster
from sklearn import metrics


# Choose a time period reasonnably calm (not too long ago so that we get
# high-tech firms, and before the 2008 crash)
d1 = datetime.datetime(2003, 01, 01)
d2 = datetime.datetime(2008, 01, 01)

symbol_dict = {
        'TOT'  : 'Total',
        'XOM'  : 'Exxon',
        'CVX'  : 'Chevron',
        'COP'  : 'ConocoPhillips',
        'VLO'  : 'Valero Energy',
        'MSFT' : 'Microsoft',
        'IBM'  : 'IBM',
        'TWX'  : 'Time Warner',
        'CMCSA': 'Comcast',
        'CVC'  : 'Cablevision',
        'YHOO' : 'Yahoo',
        'DELL' : 'Dell',
        'HPQ'  : 'Hewlett-Packard',
        'AMZN' : 'Amazon',
        'TM'   : 'Toyota',
        'CAJ'  : 'Canon',
        'MTU'  : 'Mitsubishi',
        'SNE'  : 'Sony',
        'F'    : 'Ford',
        'HMC'  : 'Honda',
        'NAV'  : 'Navistar',
        'NOC'  : 'Northrop Grumman',
        'BA'   : 'Boeing',
        'KO'   : 'Coca Cola',
        'MMM'  : '3M',
        'MCD'  : 'Mc Donalds',
        'PEP'  : 'Pepsi',
        #'KFT'  : 'Kraft Foods',
        'K'    : 'Kellogg',
        'UN'   : 'Unilever',
        'MAR'  : 'Marriott',
        'PG'   : 'Procter Gamble',
        'CL'   : 'Colgate-Palmolive',
        #'NWS'  : 'News Corporation',
        'GE'   : 'General Electrics',
        'WFC'  : 'Wells Fargo',
        'JPM'  : 'JPMorgan Chase',
        'AIG'  : 'AIG',
        'AXP'  : 'American express',
        'BAC'  : 'Bank of America',
        'GS'   : 'Goldman Sachs',
        'AAPL' : 'Apple',
        'SAP'  : 'SAP',
        'CSCO' : 'Cisco',
        'TXN'  : 'Texas instruments',
        'XRX'  : 'Xerox',
        'LMT'  : 'Lookheed Martin',
        'WMT'  : 'Wal-Mart',
        'WAG'  : 'Walgreen',
        'HD'   : 'Home Depot',
        'GSK'  : 'GlaxoSmithKline',
        'PFE'  : 'Pfizer',
        'SNY'  : 'Sanofi-Aventis',
        'NVS'  : 'Novartis',
        'KMB'  : 'Kimberly-Clark',
        'R'    : 'Ryder',
        'GD'   : 'General Dynamics',
        'RTN'  : 'Raytheon',
        'CVS'  : 'CVS',
        'CAT'  : 'Caterpillar',
        'DD'   : 'DuPont de Nemours',
    }

symbols, names = np.array(symbol_dict.items()).T

print "----------------------------Symbols---------------------------------------"
print symbols

print "----------------------------Names---------------------------------------"
print names

quotes = [finance.quotes_historical_yahoo(symbol, d1, d2, asobject=True)
                for symbol in symbols]

print "----------------------------Quotes---------------------------------------"
print "Number of quotes:        ",len(quotes)


print "--------------------------open and close-----------------------------------"
#volumes = np.array([q.volume for q in quotes]).astype(np.float)
open    = np.array([q.open   for q in quotes]).astype(np.float)
close   = np.array([q.close  for q in quotes]).astype(np.float)


ocDiff = close - open
#print ocDiff

eMatrix = np.corrcoef(ocDiff)
print eMatrix

affinity = cluster.AffinityPropagation()
affinity.fit(eMatrix)

print affinity.labels_
cluster0 = []
cluster1 = []
cluster2 = []
cluster3 = []
cluster4 = []
cluster5 = []
cluster6 = []
cluster7 = []
cluster8 = []
cluster9 = []
cluster10 = []
cluster0names = []
cluster1names = []
cluster2names = []
cluster3names = []
cluster4names = []
cluster5names = []
cluster6names = []
cluster7names = []
cluster8names = []
cluster9names = []
cluster10names = []

for i in range(len(affinity.labels_)):
    if affinity.labels_[i] == 0:
        cluster0.append(quotes[i])
        cluster0names.append(names[i])
    elif affinity.labels_[i] == 1:
        cluster1.append(quotes[i])
        cluster1names.append(names[i])
    elif affinity.labels_[i] == 2:
        cluster2.append(quotes[i])
        cluster2names.append(names[i])
    elif affinity.labels_[i] == 3:
        cluster3.append(quotes[i])
        cluster3names.append(names[i])
    elif affinity.labels_[i] == 4:
        cluster4.append(quotes[i])
        cluster4names.append(names[i])
    elif affinity.labels_[i] == 5:
        cluster5.append(quotes[i])
        cluster5names.append(names[i])
    elif affinity.labels_[i] == 6:
        cluster6.append(quotes[i])
        cluster6names.append(names[i])
    elif affinity.labels_[i] == 7:
        cluster7.append(quotes[i])
        cluster7names.append(names[i])
    elif affinity.labels_[i] == 8:
        cluster8.append(quotes[i])
        cluster8names.append(names[i])
    elif affinity.labels_[i] == 9:
        cluster9.append(quotes[i])
        cluster9names.append(names[i])
    elif affinity.labels_[i] == 10:
        cluster10names.append(names[i])
        cluster10.append(quotes[i])

print cluster0names
print cluster1names
print cluster2names
print cluster3names
print cluster4names
print cluster5names
print cluster6names
print cluster7names
print cluster8names
print cluster9names
print cluster10names

for j in range(len(cluster0)):
    plt.plot(cluster0[j].close,label = cluster0names[j] )
plt.title("Cluster0")
plt.xlabel("Days")
plt.ylabel("$")
plt.legend(loc='upper center')
plt.tight_layout()
plt.show()

for j in range(len(cluster1)):
    plt.plot(cluster1[j].close,label = cluster1names[j] )
plt.title("Cluster1")
plt.xlabel("Days")
plt.ylabel("$")
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

for j in range(len(cluster2)):
    plt.plot(cluster2[j].close,label = cluster2names[j] )
plt.title("Cluster2")
plt.xlabel("Days")
plt.ylabel("$")
plt.legend(loc='upper center')
plt.tight_layout()
plt.show()

for j in range(len(cluster3)):
    plt.plot(cluster3[j].close,label = cluster3names[j] )
plt.title("Cluster3")
plt.xlabel("Days")
plt.ylabel("$")
plt.legend(loc='upper center')
plt.tight_layout()
plt.show()

for j in range(len(cluster4)):
    plt.plot(cluster4[j].close,label = cluster4names[j] )
plt.title("Cluster4")
plt.xlabel("Days")
plt.ylabel("$")
plt.legend(loc='center')
plt.tight_layout()
plt.show()

for j in range(len(cluster5)):
    plt.plot(cluster5[j].close,label = cluster5names[j] )
plt.title("Cluster5")
plt.xlabel("Days")
plt.ylabel("$")
plt.legend(loc='upper center')
plt.tight_layout()
plt.show()

for j in range(len(cluster6)):
    plt.plot(cluster6[j].close,label = cluster6names[j] )
plt.title("Cluster6")
plt.xlabel("Days")
plt.ylabel("$")
plt.legend(loc='lower center')
plt.tight_layout()
plt.show()

for j in range(len(cluster7)):
    plt.plot(cluster7[j].close,label = cluster7names[j] )
plt.title("Cluster7")
plt.xlabel("Days")
plt.ylabel("$")
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

for j in range(len(cluster8)):
    plt.plot(cluster8[j].close,label = cluster8names[j] )
plt.title("Cluster8")
plt.xlabel("Days")
plt.ylabel("$")
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

for j in range(len(cluster9)):
    plt.plot(cluster9[j].close,label = cluster9names[j] )
plt.title("Cluster9")
plt.xlabel("Days")
plt.ylabel("$")
plt.legend(loc='upper center')
plt.tight_layout()
plt.show()

for j in range(len(cluster10)):
    plt.plot(cluster10[j].close,label = cluster10names[j] )
plt.title("Cluster10")
plt.xlabel("Days")
plt.ylabel("$")
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()