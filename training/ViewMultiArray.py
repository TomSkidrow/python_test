import numpy as np
import pandas as pd

arr = np.array([[100, 200, 300],
                [750, 850, 900],
                [1200, 1300, 1400]], np.int_)

print(pd.DataFrame(arr))
