import pandas as pd
import math

df = pd.DataFrame(
    {
        'A': [25, 100],
        'B': [4, 9]
    })

result = df.applymap(math.sqrt)
print(result)
