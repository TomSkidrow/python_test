import pandas as pd
# import xlsxwriter

# df = pd.DataFrame(
#     {
#         'ProductCost': [80, 220, 240],
#         'ProductPrice': [100, 250, 280],
#         'ProductList': ['Python', 'PHP', 'Javascript']
#     }
# )

# writer = pd.ExcelWriter('newproduct.xlsx', engine='xlsxwriter')
# df.to_excel(writer, sheet_name='สินค้า')
# writer._save()

# df = pd.read_excel('Product.xlsx', sheet_name='รายชื่อสินค้า')

# result = df.to_csv(index=False)
# print(result)

# df = pd.read_excel('Product.xlsx', sheet_name='รายชื่อสินค้า')
# result = df.to_json(orient='records', force_ascii=False)
# print(result)

df = pd.read_excel('Product.xlsx', sheet_name='รายชื่อสินค้า')
result = df.to_html()
print(result)
