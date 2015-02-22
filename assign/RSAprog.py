import random
import math
import sys

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
 

'''
    get the gcd of a and b
'''
def gcd(a,b):
    while b is not 0: 
       tmp = b
       b = a % b
       a = tmp
    return a

'''
#used in isprime
'''
def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True # n  is definitely composite

'''
 #uses Miller-Rabin_primality_test, since other methods for generating
 #128-bit(40-digit) primes and testing them take ludicrous amounts of time
'''
def isprime(n, _precision_for_huge_n=16):
    if n in _known_primes or n in (0, 1):
        return True
    if any((n % p) == 0 for p in _known_primes):
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467: 
        if n == 3215031751: 
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # otherwise
    return not any(_try_composite(a, d, n, s) 
                   for a in _known_primes[:_precision_for_huge_n])

 #for use with isprime for faster checking
_known_primes = [2, 3]
_known_primes += [x for x in range(5, 1000, 2) if isprime(x)]

### GENERATE  p,q ###
p=4
q=4
bits=128

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

