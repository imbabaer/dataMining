import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib, json, csv
import time as ti


#print pd.read_csv('EnergyMix.csv')
dataFrame = pd.DataFrame(pd.read_csv('EnergyMix.csv'))
print dataFrame

oil = dataFrame['Oil']
print oil.size
gas = dataFrame['Gas']
coal = dataFrame['Coal']
nuclear = dataFrame['Nuclear']
hydro = dataFrame['Hydro']
total2009 = dataFrame['Total2009']
co2emm = dataFrame['CO2Emm']
countries = dataFrame['Country']


print coal.value_counts()

index = np.arange(oil.size)
plt.bar(index,oil,linewidth=1)
plt.title('Oil')
plt.ylabel('Oelenergieverbrauch in Mio Tonnen (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
#plt.show()

index = np.arange(gas.size)
plt.bar(index,gas,linewidth=1)
plt.title('Gas')
plt.ylabel('Gasenergieverbrauch in Mio Tonnen Oelequivalent (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
#plt.show()

index = np.arange(coal.size)
plt.bar(index,coal,linewidth=1)
plt.title('Coal')
plt.ylabel('Kohleenergieverbrauch in Mio Tonnen Oelequivalent  (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
#plt.show()

index = np.arange(nuclear.size)
plt.bar(index,nuclear,linewidth=1)
plt.title('Nuclear')
plt.ylabel('Nuklearenergieverbrauch in Mio Tonnen Oelequivalent  (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
#plt.show()


index = np.arange(hydro.size)
plt.bar(index,hydro,linewidth=1)
plt.title('Hydro')
plt.ylabel('Wasserenergieverbrauch in Mio Tonnen Oelequivalent  (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
#plt.show()

index = np.arange(total2009.size)
plt.bar(index,total2009,linewidth=1)
plt.title('total2009')
plt.ylabel('Summe Verbrauch aller Energieformen in Mio Tonnen Oelequivalent  (p.a.)')
plt.xlim(0,65)
plt.xticks(np.arange(65)+0.5,countries,rotation=90)
plt.tight_layout()
plt.show()


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

print countries
print type(countries)
print len(countries)

def geocode(addr):
	url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %   (urllib.quote(addr.replace(' ', '+')))
	data = urllib.urlopen(url).read()
	info = json.loads(data).get("results")[0].get("geometry").get("location")
	#A little ugly I concede, but I am open to all advices :) '''
	return info


latitudes   = np.zeros((len(countries)))
longitudes  = np.zeros((len(countries)))


for c in range(len(countries)):
    r = geocode(countries[c])
    #if (c%5 == 0):
    ti.sleep(0.5)
    #print "wait 0.5 s"
    latitudes[c] = r['lat'];
    longitudes[c] = r['lng'];
    print "%s has lat %s and long %s" % (countries[c], r['lat'], r['lng'])




dataFrame['Lat'] = pd.Series(latitudes)
dataFrame['Long'] = pd.Series(longitudes)
print "------------------------------"
print dataFrame
dataFrame.to_csv("EnergyMixGeo.csv")