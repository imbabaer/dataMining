import numpy as np
import scipy.spatial.distance as sci
from scipy.cluster import hierarchy
from matplotlib import pyplot as plt
from matplotlib import axes
from pylab import find
from sklearn.preprocessing import scale
import pandas as pd

#cluster parameters
metric="correlation";
#linkage_method="average";
#linkage_method="single";
linkage_method="complete";
#linkage_method="weighted";
n_clusters  = 4

print 'Open file EnergyMixGeo.csv ...'
energyData = pd.DataFrame(pd.read_csv('EnergyMixGeo.csv'));

print 'Separate Energy Data into File Ids and Features ...'
countries = energyData.values[:,0]
print 'Number of Countries to Cluster = ', len(countries)

#copy dataFrame and modify it
features = energyData.copy();
features = features.drop("Country", 1)
features = features.drop("Total2009", 1)
features = features.drop("CO2Emm", 1)
features = features.drop("Lat", 1)
features = features.drop("Long", 1)

#standardisation without subtracting the mean
print 'Scale Energy Data Features ...'
scaledFeatures = scale(features, with_mean=False)

#calculate distance matrix
print '-'*30, 'Calculate distance Matrix by metric = ', metric, '-' *30
distMatrix  = sci.pdist(scaledFeatures,metric=metric)

#do the hierarchical clustering
print '-'*30, 'Do Hierarchical Clustering into %s, method = %s' %(n_clusters, linkage_method), '-' *30
hierclust   = hierarchy.linkage(distMatrix, method=linkage_method)

#assign cluster labels to instances (countries)
clustlabels = hierarchy.fcluster(hierclust, t=n_clusters, criterion="maxclust")
clustlabels = clustlabels-1
print 'Number of Clusters = ', n_clusters

#one subplot for each cluster
subplots    = np.array([411, 412, 413, 414])
resources   = np.array(["Oil", "Gas", "Coal", "Nuclear", "Hydro"])
colors      = np.array(['#b266b2', '#58a618', '#00aaee', '#0c1dee', '#2a0d0d', '#108070', '#FF8080', '#CC0066', '#FFFF00'])

#individualClusters = plt.figure(1);

#create subplots
for cl in range(n_clusters):
    print '------------------------Cluster '+str(cl)+' -----------------'

    currentCluster = plt.figure(cl+2)

    totalResources = np.zeros(len(resources))
    currentColor = 0;

    #find all countries for current cluster
    ind=find(clustlabels==cl)
    maxInResources = 0;
    #print out data of country and add resources
    for a in ind:
        print a, ' ', countries[a];
        if currentColor == len(colors):
            #restart from the beginning
            currentColor = 0;
        #print 'scaled   Features(Oil, Gas, Coal, Nuclear, Hydro) = ', scaledFeatures[a:a+1]
        print 'Energy consumption (Oil, Gas, Coal, Nuclear, Hydro) = ', energyData.values[a, 1:6]

        #sum together all resource
        for r in range(5):
            #use this when using scaled Features
            #print 'totalResources[', r, '] += scaledFeatures[',a, ',', r, '] : %s += %s' % (totalResources[r], scaledFeatures[a:a+1][:,r] ) ;
            #totalResources[r] += scaledFeatures[a:a+1][:,r];
            #use this when using original Features
            #print 'totalResources[', r, '] += features[',a, ',', r, '] : %s += %s' % (totalResources[r], features[a:a+1][resources[r]] ) ;
            add = features[a:a+1][resources[r]];
            if maxInResources < max(add):
                maxInResources =  max(add);
                print maxInResources
            totalResources[r] += add;

        #plot labels
        plt.xticks([0,1,2,3,4], resources, fontsize=11)
        plt.yticks(fontsize=8)
        plt.title('Cluster %s' %(cl))
        #set y range to (maximum value of cluster + 50%)
        plt.ylim(0,maxInResources)
        plt.xlim(0,len(resources)-1);

        #plot energy data of current Country into subplot
        plt.plot(energyData.values[a,1:6], colors[currentColor],label=countries[a])
        plt.tight_layout()

        currentColor+=1;

    for r in range(5):
        print 'total Resources of cluster %s = %s' % (cl, totalResources[r])
    #plt.plot(totalResources, 'b-.', linewidth=1.0, label='total Resources')
    if cl == 3:
        plt.legend(loc=9,prop={'size':12});
    elif cl == 1:
        plt.legend(loc=1,prop={'size':9});
    else:
        plt.legend(loc=1,prop={'size':12});
    #save plots to file

#set dendrogram parameters
plt.figure(7)
plt.title("Dendrogram")
plt.xlabel("Distance")
#set x lim according to linkage-method used
if(linkage_method=='average'):
    plt.xlim(0, 1.2)
elif(linkage_method=='complete'):
    plt.xlim(0, 2.0)
elif(linkage_method=='single'):
    plt.xlim(0, 0.28)
else:
    #weighted
    plt.xlim(0, 1.4);

#create dendrogram
hierarchy.dendrogram(hierclust, orientation='left', labels=countries,
                     count_sort=False, distance_sort=False, color_list=None, link_color_func=None,
                     leaf_font_size=6.5, leaf_label_func=None)

#save dendrogram to file
plt.tight_layout()
plt.savefig('dendrogram_%s_%s.png' %(linkage_method, metric));
plt.show()

#add Cluster labels to data
energyData['Cluster'] = pd.Series(clustlabels);
#save dataFrame to csv file
energyData.to_csv('EnergyMixGeo.csv' %(linkage_method, metric), index=False);