import numpy as np
import random as rd

data = np.random.rand(5)
data2 = rd.randint(0, 10)

num1 = rd.randrange(100)
print('เลขจำนวนเต็ม: ', num1)
num2 = rd.randrange(10, 50)
print('เลขจำนวนเต็ม: ', num2)
num3 = rd.randrange(1, 100, 5)
print('เลขจำนวนเต็ม: ', num3)

# print('-------------------')
# print(data)
# print(type(data))
# print('-------------------')
# print('เลขจำนวนเต็ม', data2)


data3 = []
for i in range(0, 10):
    data3.append(rd.randint(1, 100))

print('-----------------')
print(data3)
print(type(data3))
