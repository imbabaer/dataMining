import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib, json, csv
import time as ti

#import data from file
dataFrame = pd.DataFrame(pd.read_csv('EnergyMix.csv'))
print dataFrame

#create fields for the different energy forms
oil = dataFrame['Oil']
gas = dataFrame['Gas']
coal = dataFrame['Coal']
nuclear = dataFrame['Nuclear']
hydro = dataFrame['Hydro']
total2009 = dataFrame['Total2009']
co2emm = dataFrame['CO2Emm']
countries = dataFrame['Country']

#plot oil usage
index = np.arange(oil.size)
plt.bar(index,oil,linewidth=1)
plt.title('Oil')
plt.ylabel('Oelenergieverbrauch in Mio Tonnen (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
plt.show()

#plot gas usage
index = np.arange(gas.size)
plt.bar(index,gas,linewidth=1)
plt.title('Gas')
plt.ylabel('Gasenergieverbrauch in Mio Tonnen Oelequivalent (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
plt.show()

#plot coal usage
index = np.arange(coal.size)
plt.bar(index,coal,linewidth=1)
plt.title('Coal')
plt.ylabel('Kohleenergieverbrauch in Mio Tonnen Oelequivalent  (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
plt.show()

#plot nuclear usage
index = np.arange(nuclear.size)
plt.bar(index,nuclear,linewidth=1)
plt.title('Nuclear')
plt.ylabel('Nuklearenergieverbrauch in Mio Tonnen Oelequivalent  (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
plt.show()

#plot hydro usage
index = np.arange(hydro.size)
plt.bar(index,hydro,linewidth=1)
plt.title('Hydro')
plt.ylabel('Wasserenergieverbrauch in Mio Tonnen Oelequivalent  (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
plt.show()

#plot total usage per country
index = np.arange(total2009.size)
plt.bar(index,total2009,linewidth=1)
plt.title('total2009')
plt.ylabel('Summe Verbrauch aller Energieformen in Mio Tonnen Oelequivalent  (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
plt.show()

#plot total usage in total
sums = [sum(coal),sum(gas),sum(oil),sum(hydro),sum(nuclear)]
plt.pie(sums,labels=["coal", "gas", "oil", "hydro", "nuclear"])
plt.tight_layout()
plt.show()
index = np.arange(5)
plt.bar(index,sums,linewidth=5)
plt.title('Total')
plt.xlim(0,5)
plt.ylabel('Summe Verbrauch der einzelnen Energieformen in Mio Tonnen Oelequivalent  (p.a.)')
plt.xticks(np.arange(5)+0.5,["coal", "gas", "oil", "hydro", "nuclear"],rotation=90)
plt.tight_layout()
plt.show()

#geocode function
def geocode(addr):
	url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %   (urllib.quote(addr.replace(' ', '+')))
	data = urllib.urlopen(url).read()
	info = json.loads(data).get("results")[0].get("geometry").get("location")
	#A little ugly I concede, but I am open to all advices :) '''
	return info

#create empty np-arrays
latitudes   = np.zeros((len(countries)))
longitudes  = np.zeros((len(countries)))

#iterate over all countries and get their lat and long
for c in range(len(countries)):
    r = geocode(countries[c])
    #if (c%5 == 0):
    ti.sleep(0.5)
    #print "wait 0.5 s"
    latitudes[c] = r['lat'];
    longitudes[c] = r['lng'];
    print "%s has lat %s and long %s" % (countries[c], r['lat'], r['lng'])

#add lat and long to the dataFrame
dataFrame['Lat'] = pd.Series(latitudes)
dataFrame['Long'] = pd.Series(longitudes)
print dataFrame

#save dataFrame to file
dataFrame.to_csv("EnergyMixGeo.csv", index=False)