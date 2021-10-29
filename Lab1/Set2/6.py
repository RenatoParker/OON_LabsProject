firstList = [2, 3, 4, 5, 6, 7, 8]
secondList = [57, 83, 29, 67, 73, 43, 48]

mySet= set()

for i in firstList:
    mySet.add((i, secondList[firstList.index(i)]))
print(mySet)
