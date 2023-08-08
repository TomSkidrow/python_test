import pandas as pd

# df = pd.read_excel('Product.xlsx', sheet_name='Sheet1')
# df = pd.read_excel('Product.xlsx')
# print(type(df))
# print(df)
# print(df['ชื่อสินค้า'])

# df = pd.read_excel('Product.xlsx', sheet_name='รายชื่อสินค้า',
#                    usecols=['รหัสสินค้า', 'ชื่อสินค้า'])

# df = pd.read_excel('Product.xlsx', sheet_name='รายชื่อสินค้า')
# # print(df)
# print(df.columns)

df = pd.read_excel('Product.xlsx')
print(df[0:3])
