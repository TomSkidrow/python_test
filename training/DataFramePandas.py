import pandas as pd

colsname = ['รายได้']
# data = [20, 25, 28, 31, 45, 53]
# data = [20, 10.3, 5.7, 11.6, 22, 12]
data = ['Visual C#', 'Python', 'Javascript', 'ASP.NET Core']
df = pd.DataFrame(data)
# df = pd.DataFrame(data, columns=colsname)

print('--------------------')
print(type(df))
# print(df)
print(df.dtypes)
