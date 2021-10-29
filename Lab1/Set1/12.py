s1 = "Ciao questa è una stringa"
count = {}
for i in s1:
    if i in count.keys():
        count[i] += 1
    else:
        count[i] = 1

print(count)