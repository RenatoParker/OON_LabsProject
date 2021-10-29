sampleList = [11, 45, 8, 23, 14, 12, 78, 45, 89]

count = {}
for i in sampleList:
    if i in count.keys():
        count[i] += 1
    else:
        count[i] = 1
print(count)