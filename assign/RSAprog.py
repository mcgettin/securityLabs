'''
    for getting the gcd and quotiants of a and b via extended gcd method
'''
def extended_gcd(a, b):
    lastremainder, remainder = abs(a), abs(b) #disregard minus signs
    x, lastx, y, lasty = 0, 1, 1, 0 #init egcd variables
    while remainder: #until remainder = 0
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if a < 0 else 1), lasty * (-1 if b < 0 else 1)

'''
    uses the extended gcd to find the mod inverse given a number e and a mod m 
'''
def modinv(e, m):
    g, x, y = extended_gcd(e, m) #gets x and y quotient and also the gcd (hopefully=1)
    if g != 1: #something went wrong if the gcd != 1
        raise ValueError
    return x % m # x is e^-1 from extended gcd , so x mod m = d (what we want)
 

def gcd(a,b):
    while b is not 0: 
       tmp = b
       b = a % b
       a = tmp
    return a

def isprime(n):
# make sure n is a positive integer
    n = abs(int(n))
# 0 and 1 are not primes
    if n < 2:
        return False
# 2 is the only even prime number
    if n == 2:
        return True
# all other even numbers are not primes
    if not n & 1:
        return False
# range starts with 3 and only needs to go up the squareroot of n
# for all odd numbers
    for x in range(3, int(n**0.5)+1, 2):
        if n % x == 0:
            return False
    return True


import random

bits=55
### GENERATE  p,q ###
p=0
q=0

while not isprime(p):
    p=random.getrandbits(bits)
print("p: "+str(p))

while not isprime(q):
    q=random.getrandbits(bits)

print("q: "+str(q))

### Calc n= p*q ###
n=p*q
print("n: "+str(n))

### Calc y= (p-1)(q-1) ###
y=(p-1)*(q-1)
print("y: "+str(y))

### Generate e (gcd(e,y)=1) ###
e=2**bits #small values for e does not affect security of RSA
while gcd(e,y)!=1:
    e+=1
print("e: "+str(e))

### Generate d (de=1 mod (y)) ###
d = modinv(e,y)
print("d: "+str(d))

print("\nPublic Key (n,e): ({}, {})".format(n,e))
print("Private Key (n,d): ({}, {})".format(n,d))

