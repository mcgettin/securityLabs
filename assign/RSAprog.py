
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

### GENERATE  p,q ###
p=0
q=0
while not isprime(p):
    p=random.getrandbits(8)
print("p: "+str(p))

while not isprime(q):
    q=random.getrandbits(8)
print("q: "+str(q))

### Calc n= p*q ###
n=p*q
print("n: "+str(n))

### Calc y= (p-1)(q-1) ###
y=(p-1)*(q-1)
print("y: "+str(y))

### Generate e (gcd(e,y)=1) ###
e=random.getrandbits(8)
while gcd(e,y)!=1:
    e+=1
print("e: "+str(e))

print("\nPublic Keys (n,e): {}, {}".format(n,e))


### Generate d (de=1 mod (y)) ###
d=random.getrandbits(6)
while d*e % y is not 1:
    d+=1
print("Private Key (d): "+str(d))
