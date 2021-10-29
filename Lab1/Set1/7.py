s1 = "ciao questa è una stringa"
s2= "ciao questa è un'altra stringa"

len = int (s1.count("")/2) -1
s3 = s1[0:len] + s2 +  s1[len+1:]
print(s3)