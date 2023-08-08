import pandas as pd

# male = ['สมชาย', 'วีระชัย', 'พรชัย', 'วีระ']
# heightmale = [180, 183, 185, 184]
data = [
    ['สมชาย', 185, 16000], ['วีระชัย', 175, 17500],
    ['พรชัย', 182, 20000], ['วีระ', 183, 19900]
]
# data = list(zip(male, heightmale))
colsname = ['ชื่อ', 'ส่วนสูง', 'เงินเดือน']
# colsname = ['ชื่อ', 'ส่วนสูง']
df = pd.DataFrame(data, columns=colsname)

print('----------------')
print(type(df))
print(df)
# print(df.shape)
print(df.index)
print(df.columns)
print(df.values)
print(type(df.values))
print(df.dtypes)
