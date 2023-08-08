import numpy as np
import pandas as pd

# data = [100, 200, 400, 800]
# data = [20.3, 3.14, 22.6, 50]
data = [5, 10, 15, 20]
ndata = np.array(data)
ps = pd.Series(data)

print('-------------------')
print(ps)
print(type(ps))
