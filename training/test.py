# Cell 1
import pandas as pd

# Cell 2
data1 = [
    ['สมชาย', 185, 16000],
    ['วีระชัย', 175, 17500],
    ['พรชัย', 182, 20000],
    ['วีระ', 183, 19900]
]

# Cell 3
data2 = [
    ['ดวงใจ', 165, 17800],
    ['วิไล', 163, 19300]
]

# Cell 4
colsname = ['ชื่อ', 'ส่วนสูง', 'เงินเดือน']
df1 = pd.DataFrame(data1, columns=colsname)
df2 = pd.DataFrame(data2, columns=colsname)

# Cell 5
df = df1._append(df2, ignore_index=True)
print(df)
