import numpy as np
import pandas as pd

arr = np.array([
    [100, 200, 300],
    [750, 850, 900],
    [1200, 1300, 1400]
])

df = pd.DataFrame(arr)
result = df.apply(lambda x: x+1)
print(result)


df2 = pd.DataFrame({
    'A': [100, 200],
    'B': [5, 10]
})

print('---------แกน x------------')
result2 = df2.apply(np.sum, axis=0)
print(result2)
print('---------แกน y------------')
result2 = df2.apply(np.sum, axis=1)
print(result2)
