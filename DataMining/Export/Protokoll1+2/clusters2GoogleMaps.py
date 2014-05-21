__author__ = 'Lenovo'
import numpy as np
import pandas as pd
import pymaps
import time as ti

#cluster parameters
metric="correlation";
linkage_method="average";
#linkage_method="single";
#linkage_method="complete";
#linkage_method="weighted";

dataFrame = pd.read_csv('results/newEnergyMixGeo_%s_%s.csv' %(linkage_method, metric))
countries = dataFrame.values[:,0]
clusters = dataFrame['Cluster']
numClusters = max(clusters)+1
print 'Number of clusters = ', numClusters

#create pymap
g = pymaps.PyMap()
g.key = "ABQIAAAAQQRAsOk3uqvy3Hwwo4CclBTrVPfEE8Ms0qPwyRfPn-DOTlpaLBTvTHRCdf2V6KbzW7PZFYLT8wFD0A"
g.maps[0].zoom = 2

#create 1 icon per cluster and add marker images
icon1 = pymaps.Icon('icon1')
icon1.image = "marker/marker_blue.png"
icon2 = pymaps.Icon('icon2')
icon2.image = "marker/marker_lightgreen.png"
icon3 = pymaps.Icon('icon3')
icon3.image = "marker/marker_lila.png"
icon4 = pymaps.Icon('icon4')
icon4.image = "marker/marker_yellow.png"
#add shadows
icon1.shadow = "marker/marker_shadow.png"
icon2.shadow = "marker/marker_shadow.png"
icon3.shadow = "marker/marker_shadow.png"
icon4.shadow = "marker/marker_shadow.png"

#add icons to pymap g
g.addicon(icon1)
g.addicon(icon2)
g.addicon(icon3)
g.addicon(icon4)

for c in range(len(countries)):
    print c, countries[c]
    lat     = dataFrame.values[c,8]
    long    = dataFrame.values[c,9]
    print 'lat long = ', lat, long

    #chose the right cluster icon
    if dataFrame.values[c,10]==0:
        icon = 'icon1'
    elif dataFrame.values[c,10]==1:
        icon = 'icon2'
    elif dataFrame.values[c,10]==2:
        icon = 'icon3'
    elif dataFrame.values[c,10]==3:
        icon = 'icon4'

    oil         = dataFrame.values[c,1];
    gas         = dataFrame.values[c,2];
    coal        = dataFrame.values[c,3];
    nuclear     = dataFrame.values[c,4];
    hydro       = dataFrame.values[c,5];
    total2009   = dataFrame.values[c,6];
    description = '%s: Oil:%s Gas:%s Coal:%s Nuclear:%s Hydro:%s Total2009:%s' %(countries[c], oil, gas, coal, nuclear, hydro, total2009)

    #add the points to the map
    p = [lat, long, description, icon]
    print 'point at ', lat, long, 'for ', countries[c], 'with ', icon
    ti.sleep(0.3)
    g.maps[0].setpoint(p)

ti.sleep(5)
#print map.showhtml()
open('clustered_%s_%s.html' %(linkage_method, metric),'wb').write(g.showhtml())   # generate test file