import numpy as np

a = np.arange(8).reshape(4, 2)
print(a)

b = np.arange(100, 200, 10).reshape(5, 2)
print(b)

array = np.array([[11, 22, 33], [44, 55, 66], [77, 88, 99]])
print(array.__class__)
c = array[:,2]
print(c)

array2 = np.array([[3 ,6, 9, 12], [15 ,18, 21, 24], [27 ,30, 33, 36], [39 ,42, 45, 48], [51 ,54, 57, 60]])
d= array2[1:15:2,:]
e= array2[: , 0:15:2]
final = np.concatenate((d.ravel(),e.ravel()))
print(final)

array3 = np.array([[5, 6, 9], [21 ,18, 27]])
array4 = np.array([[15 ,33, 24], [4 ,7, 1]])

array5 = array4 + array3
array5 = np.sqrt(array5)
print(array5)

array6 = np.array([[34,43,73],[82,22,12],[53,94,66]])
array6 = np.sort(array6)
print(array6)

array7 = np.array([[34,43,73],[82,22,12],[53,94,66]])
print(array7[0,:].min())
print(array7[1,:].max())

array8 = np.array([[34,43,73],[82,22,12],[53,94,66]])
new_column = [10,10,10]
array8[:,1] = new_column
print(array8)