speed = {"Jan":47, "Feb":52, "March":47, "April":44, "May":52, "June":53, "July":54, "Aug":44, "Sept":54}

myList = []

for i in speed.values():
    if myList.count(i) == 0:
        myList.append(i)

print(myList)

