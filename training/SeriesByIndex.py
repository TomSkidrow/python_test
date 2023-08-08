import pandas as pd

person = ['สมศรี', 'พิมพ์พร', 'สุดใจ', 'สมหญิง']
height = [160, 166, 163, 168]

ps = pd.Series(height, index=person)

print('-------------------')
print(ps)
print(type(ps))
