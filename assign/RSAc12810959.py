'''
Tested on : IDLE - python 3.4
Name: Neil McGettigan
Number: C12810959
E-mail: c12810959@mydit.ie
Assignment: RSA Encryptor/Decryptor
Date: 11/03/2015
'''

import tkinter as tk  #try Tkinter for python v2.7
import random

'''
setting p,q Boxes, then using those to set n and y Boxes
'''
def setPQNY(p,q,n,y):
    
    p.set(genPrime(128)) #prime of 128-bits
    q.set(genPrime(128))
    
    n.set(int(p.get())*int(q.get()))
    y.set((int(p.get())-1)*(int(q.get())-1))


'''
setting Encrypt Message Box
'''
def setE(e,y):
    if len(y.get()) < 1: return #must generate y first

    num=2**16 # e doesn't need to be huge, but around this value and beyond is safe
    while gcd(num,int(y.get()))!=1: #keep adding to e until co-prime
        num+=1
        
    e.set(num)


'''
setting Decrypt Cipher Box
'''
def setD(d,e,y):
    if len(e.get()) < 1: return #must generate e first

    num=modinv(int(e.get()),int(y.get())) #get mod inverse to find d

    d.set(num)
    

'''
    for getting the gcd and quotiants of a and b via extended gcd method
'''
def extended_gcd(a, b):
    lastremainder, remainder = abs(a), abs(b) #disregard minus signs
    x, lastx, y, lasty = 0, 1, 1, 0 #init extended-gcd variables
    while remainder: #until remainder = 0
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if a < 0 else 1), lasty * (-1 if b < 0 else 1) #returns gcd,x,y


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
    for using the public key to encrypt a plaintext message
'''
def encryptText(e,n,usrIn,cipher):
    if len(usrIn.get()) <1: return # if the message box is empty
    
    encr="" #init the encrypted string
    for ch in usrIn.get():
        ch=int(ord(ch)) #convert char to ascii
        ch=pow(ch,int(e.get()),int(n.get())) #encrypt
        encr+=str(ch)+" " #add to encrypted string

    cipher.set(encr) #set using the full encrypted string


'''
    for using private key to decrypt cipher into plaintext
'''
def decryptText(d,n,cipher,plain):
    if len(cipher.get()) <1: return # if haven't encrypted yet
    try: # will fail if new primes are generated without new e,d values generated too
        decr="" 
        for line in cipher.get().split(" "):
            if len(line) < 1: break
            line=pow(int(line),int(d.get()),int(n.get()))
            line=chr(line)
            decr+=line
    except:
        print("Warning: Generate new private key! (primes changed)")
        return #avoid returning decr to plain box
    plain.set(decr)



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
 #large primes and testing them take ludicrous amounts of time
 #precision of 16 passes removes any reasonable doubt of being prime
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


'''
for generating a prime number of desired bit length
'''
def genPrime(bits):
    p=4
    while not isprime(p):
        p=random.getrandbits(bits)
    return p


'''
program starts here, initializing Tk()
'''
main = tk.Tk()
main.configure(background='lightblue')

'''
Setting up variables i'll need for widgets later
'''
#using a list of primes, for use in primality test (Miller-Rabin)
_known_primes = [2, 3]
_known_primes += [x for x in range(5, 1000, 2) if isprime(x)]

usrIn=tk.StringVar() # user's input into box
p = tk.StringVar()  # prime p
q = tk.StringVar() # prime q
n = tk.StringVar() # n = p*q
y = tk.StringVar() # y = (p-1)*(q-1)
e = tk.StringVar() # generate e where: (gcd(e,y)=1)
d = tk.StringVar() # generate d where: (de=1 mod (y))
cipher = tk.StringVar() # encoded message
plain = tk.StringVar() # decoded message


'''
Here I am declaring all the widgets i'll need for the gui
'''
usrLab=tk.Label(main,text="Input message to encrypt: ",bg='yellow')
usrIn=tk.Entry(main,width=50)

genPrimes=tk.Button(main,text="Generate Primes",command=lambda: setPQNY(p,q,n,y))
pLab=tk.Label(main,text="p (1st prime): ")
qLab=tk.Label(main,text="q (2nd prime): ")
pBox=tk.Message(main, textvariable=p,width=300,bg='white')
qBox=tk.Message(main,textvariable=q,width=300,bg='white')

nLab=tk.Label(main,text="n (n=p*q): ")
yLab=tk.Label(main,text="y (y=(p-1)*(q-1)): ")
nBox=tk.Message(main, textvariable=n,width=500,bg='white')
yBox=tk.Message(main,textvariable=y,width=500,bg='white')

genPublic=tk.Button(main,text="Generate Public key",command=lambda: setE(e,y))
eLab=tk.Label(main,text="e (gcd(e,y)=1): ",pady=20)
eBox=tk.Message(main, textvariable=e,width=50,bg='white')

genPrivate=tk.Button(main,text="Generate Private key",command=lambda: setD(d,e,y))
dLab=tk.Label(main,text="d (de=1 mod (y)): ",pady=20)
dBox=tk.Message(main, textvariable=d,width=500,bg='white')


encrMsg=tk.Button(main,text="Encrypt Message",command=lambda: encryptText(e,n,usrIn,cipher))
encrBox=tk.Message(main, textvariable=cipher,width=800,bg='white')

decrMsg=tk.Button(main,text="Decrypt Cipher",command=lambda: decryptText(d,n,cipher,plain))
decrBox=tk.Message(main, textvariable=plain,width=300,bg='white')


'''
Here I place my widgets I've created
'''
usrLab.grid(row=0,column=0)
usrIn.grid(row=0,column=2,columnspan=2,pady=10)

genPrimes.grid(row=4,column=0,rowspan=2)
pLab.grid(row=4,column=1)
pBox.grid(row=4, column=2)
qLab.grid(row=5,column=1)
qBox.grid(row=5, column=2)

nLab.grid(row=6,column=1)
nBox.grid(row=6, column=2,columnspan=2)
yLab.grid(row=7,column=1)
yBox.grid(row=7, column=2,columnspan=2,padx=5)

genPublic.grid(row=8,column=0)
eLab.grid(row=8,column=1)
eBox.grid(row=8,column=2)
genPrivate.grid(row=9,column=0)
dLab.grid(row=9,column=1)
dBox.grid(row=9,column=2,padx=5)

encrMsg.grid(row=10,column=0)
encrBox.grid(row=10,column=1,columnspan=2,pady=5)

decrMsg.grid(row=11,column=0)
decrBox.grid(row=11,column=1,columnspan=2)


'''main loop'''
main.mainloop()


