min = 2
max = 30

i = int(input("Set i: "))

sum = 0
temp = 0
for x in range(i,max+1):
    sum += x
    print("Sum: ",sum)
    print("Temp: ", temp)
    temp = x