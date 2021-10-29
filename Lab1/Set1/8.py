s1 = "ciao questa è una stringa"
s2= "ciao questa è un'altra stringa"

len1 = int(len(s1)/2 - 1)
len2 = int(len(s2)/2 - 1)

s3 = s1[0] + s1[len1] + s1[-1] + s2[0] + s2[len2] + s2[-1]
print(s3)