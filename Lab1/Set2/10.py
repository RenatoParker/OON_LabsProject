sampleList = [87, 52, 44, 53, 54, 87, 52, 53]


for i in sampleList:
    if sampleList.count(i) > 1:
        sampleList.remove(i)
print(sampleList)

myTuple = sampleList

myTuple.sort()
print(myTuple[0], myTuple[-1])