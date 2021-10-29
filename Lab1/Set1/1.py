import test

product = test.product(2,5)
print("product:", product)
n1 = int(input("Enter a number:"))
n2 = int(input("Enter a number:"))

product = test.product(n1, n2)

print("Product=", product)

if product > 1000:
    print("Sum:", (n1+n2))