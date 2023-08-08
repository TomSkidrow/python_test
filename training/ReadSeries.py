import pandas as pd

data = [100, 150, 200, 300, 280, 513, 410]
ps = pd.Series(data)

print('------------------------')
print(ps[:])
print(ps[1:4])
print(ps[2:])
print(ps[4:])
