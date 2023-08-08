import pandas as pd

dic = {'สมศรี': 167, 'พิมพ์พร': 170, 'สุดใจ': 165, 'สมหญิง': 164}
ps = pd.Series(dic)

print('--------------------------')
print(type(dic))
# print(ps)
# print(ps[0])
# print(ps[3])
# print(ps['พิมพ์พร'])
print(ps[-1])
print(ps[-2])


data = [100, 150, 200, 300]
ps2 = pd.Series(data)

print('--------------------------')
print(ps2[2])
