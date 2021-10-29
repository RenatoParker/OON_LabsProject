s1 = "ho vinto 10 euro il 20 04"

sum: int = 0
for i in s1:
    if i.isdigit():
        sum += int(i)

print(sum)