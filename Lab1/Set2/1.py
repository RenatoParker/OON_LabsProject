listOne = [2, 6, 9 ,12, 15, 18, 21]
listTwo = [4,8,12,16,20,24,28]
listThree = []

for i in listOne[::2]:
    listThree.append(i)
for i in listTwo[1::2]:
    listThree.append(i)


print(listThree)