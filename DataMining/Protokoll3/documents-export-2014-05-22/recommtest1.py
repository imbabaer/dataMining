import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance as sci
import recommendations as rec

dict = rec.topMatches(rec.critics, person='Toby', similarity='sim_euclid')
print "euklid"
print dict

print "_"*80

dict = rec.topMatches(rec.critics, person='Toby', similarity='sim_pearson')
print "pearson"
print dict

recommendations = rec.getRecommendations(rec.critics, 'Toby', 'sim_pearson')
print "Rec"
print recommendations


print "UCF"
print rec.critics

transCritics = rec.transformCritics(rec.critics, 'sim_euclid')

print "ICF"
print transCritics

#print rec.topMatches(transCritics, 'Lady in the Water', 'sim_pearson')

print rec.calculateSimilarItems(transCritics, 'sim_pearson')

#print rec.topMatches(transCritics, 'Snakes on a Plane', 'sim_pearson')
