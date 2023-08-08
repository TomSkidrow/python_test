import numpy as np
import pandas as pd

arr = np.array([
    [100, 200, 300],
    [750, 850, 900],
    [1200, 1300, 1400]
])

df = pd.DataFrame(arr)


def Add(x):
    return x + 5


result = df.apply(Add)
print(result)
