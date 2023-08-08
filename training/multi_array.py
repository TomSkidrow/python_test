import numpy as np
arr = np.array([[100, 200, 300], [2000, 4000, 6000]], np.int_)

print(arr.shape)
print(type(arr))
print('-----------------')
arr2 = np.array([[10, 20, 30],
                [100, 200, 300]])
result = np.sum(arr2)
print('ผลรวม :', result)
print('-----------------')
result2 = np.sum(arr2, axis=0)
print('ผลรวม :', result2)
print('-----------------')

arr3 = np.zeros(5)
print('ข้อมูล: ', arr3)
print('ชนิดข้อมูล', type(arr3))
print('-----------------')

arr4 = np.zeros((2, 4))
print('ข้อมูล: ', arr4)
print('ชนิดข้อมูล', type(arr4))
print('-----------------')

arr5 = np.zeros((2, 4), dtype=int)
print('ข้อมูล : ', arr5)
print('ชนิดข้อมูล : ', arr5.dtype)
print('-----------------')

arr6 = np.zeros((2, 3), dtype=[('x', 'int'), ('y', 'float')])
print('ข้อมูล :', arr6)
print('ชนิดข้อมูล :', arr6.dtype)
print('-----------------')

arr7 = np.ones(5)
print('ข้อมูล :', arr7)
print('ชนิดข้อมูล :', type(arr7))
print('-----------------')

arr8 = np.ones((2, 4), dtype=int)
print('ข้อมูล :', arr8)
print('ชนิดข้อมูล :', arr8.dtype)
print('-----------------')

arr9 = np.ones((2, 3), dtype=[('x', 'int'), ('y', 'float')])
print('ข้อมูล :', arr9)
print('ชนิดข้อมูล :', arr9.dtype)
print('-----------------')
