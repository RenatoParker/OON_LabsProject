list1 = [1,5,3,5,2,4,24]
list2 = [5,2,5,10,5,3,6,5]

list = list()

for i in list1:
    if i%2 == 1:
        list.append(i)
for i in list2:
    if i%2== 0:
        list.append(i)

print(list)