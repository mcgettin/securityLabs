'''
Function to take in two numbers and return the greatest common divisor between them
'''
def gcd(a,b):
    while b is not 0: 
       tmp = b
       b = a % b
       a = tmp
    return a


print("Calculate GCD(a,b):")
a=input("a is: ")
b=input("b is: ")
try:
    a=int(a)
    b=int(b)
except:
    print("Bad input. only ints allowed.")
    exit(1)

if a < b:
    print("Bad input. a must be bigger than b.")
    exit(2)

denom=gcd(a,b)
print("GCD is "+str(denom))
