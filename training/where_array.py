import numpy as np

arr = np.array([10, 20, 30, 40, 50])

result = arr[arr >= 30]
print('ข้อมูล: ', result)
print('-----------------')

result2 = arr[arr >= 100]
print('ข้อมูล: ', result2)
print('-----------------')

result3 = np.where(arr >= 20, arr, 'น้อยกว่า 20')
print('ข้อมูล: ', result3)
print('-----------------')

result4 = np.where(arr > 100, arr, 0)
print('ข้อมูล: ', result4)
print('-----------------')

arr1 = np.array([[100, 200], [300, 400]])
arr2 = np.array([[1000, 2000], [3000, 4000]])

arr_append = np.append(arr1, arr2)
print(arr_append)
print('-----------------')

arr_append1 = np.append(arr1, arr2, axis=0)
print(arr_append1)
print('-----------------')

arr_append2 = np.append(arr1, arr2, axis=1)
print(arr_append2)
print('-----------------')
