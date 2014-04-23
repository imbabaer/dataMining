import pandas as pd
import numpy as np
ran = np.arange(10)
print ran
print "//////////////////"
indices = ["here","are","your","indices","!"]

var = pd.DataFrame(ran, index=indices,columns=list('A'))

print var