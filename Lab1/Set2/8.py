rollNumber = [47, 64, 69, 37, 76, 83, 95, 97]
sampleDict = {"Jhon":47, "Emma":69, "Kelly":76, "Jason":97}

for num in rollNumber:
    isPresent = False
    for element in sampleDict.values():
        if element == num:
            isPresent = True
    if not isPresent:
        rollNumber.remove(num)

print(rollNumber)


