s1 = (input("Type a string: "))
countLow: int = 0
countUpper: int = 0
countDigit: int = 0
countSpecial: int = 0
for i in s1:
    if i.islower():
        countLow += 1
    else:
        if i.isupper():
            countUpper += 1
        else:
            if i.isdigit():
                countDigit += 1
            else:
                countSpecial += 1

print("Lower cases: ", countLow)
print("Upper cases: ", countUpper)
print("Digit cases: ", countDigit)
print("Special cases: ", countSpecial)
