firstSet = {57, 83, 29}
secondSet = {57, 83, 29, 67, 73, 43, 48}

if firstSet.issubset(secondSet):
    for i in firstSet:
        secondSet.remove(i)

print(secondSet)