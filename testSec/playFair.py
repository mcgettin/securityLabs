'''
Function prints out the cipherBox in easy readable 5x5 format
'''
def printBox(cipherBox):
    for i in range(len(cipherBox)):
        print (cipherBox[i],end='\t')
        if i%5==4:  print('\n')


'''
Function alters key to remove repeating letters
'''
def normKey(key):
    tmp=""
    for let in key:
        if let not in tmp: tmp+=let
    return tmp

'''
Fuction fills in the reaminder of the cipherBox with the letters of the alphabet
'''
def fillBox(box,key):
    letters=["a","b","c","d","e","f","g","h","(i/j)","k","l","m","n",
                 "o","p","q","r","s","t","u","v","w","x","y","z"]

    #inserting key into box
    for i in range(len(key)):
        box[i]=key[i]
        
    #filling remaining spaces in box
    for let in letters:
        for i in range(len(key),len(box)):
            #print(let)
            if let is "(i/j)" and "i" in key or "j" in key: pass
            elif let not in box and box[i] is ".":
                box[i]=let        
                break
    return box


'''
Function takes a message and strips out punctionation, fills in double letters and adds filler
'''
def normMsg(msg):
    exclude = ",. /?!$£*()-;:"
    msg= ''.join(ch for ch in msg if ch not in exclude).lower()

    if len(msg)%2 is not 0: msg+="x"

    for i in range (len(msg)-1):
        if i%2 is 1: continue
        elif msg[i] is msg[i+1] and i%2==0:
            tmp1=msg[:i]
            tmp2=msg[i:]
            msg=tmp1+"x"+tmp2
    return msg

'''
--- Main Program ---
'''
cipherBox=["." for x in range(25)]
msg="There is a box hidden under thine tree with all my money, Love Joo-boo."
key="xylophone"

print("Message: "+msg)
print("Secret Key: "+key+"\n")

key=normKey(key)
cipherBox=fillBox(cipherBox,key)
printBox(cipherBox)

msg=normMsg(msg)
pairs=""
for i in range(len(msg)-1):
    if not i%2:
        pairs+=msg[i:i+2]+" "

pairs=pairs.strip().split(" ")
#print(pairs)

crypto=""
for elm in pairs:
    if elm[0] is "i" or elm[0] is "j":
        try:
            pos1=cipherBox.index("(i/j)")
        except:
            try:
                pos1=cipherBox.index("i")
            except:
                pos1=cipherBox.index("j")
    else: pos1=cipherBox.index(elm[0])
    if elm[1] is "i" or elm[1] is "j":
        try:
            pos2=cipherBox.index("(i/j)")
        except:
            try:
                pos2=cipherBox.index("i")
            except:
                pos2=cipherBox.index("j")
    else: pos2=cipherBox.index(elm[1])

    if int(pos1/5) is int(pos2/5):
        tmp1=pos1+1
        tmp2=pos2+1
        if tmp1%5 is 0: tmp1-=5
        if tmp2%5 is 0: tmp2-=5
        elm=cipherBox[tmp1]+cipherBox[tmp2]
        #print(elm + " - row",end="\t")
    elif pos1%5 is pos2%5:
        tmp1=int(pos1)+5
        tmp2=int(pos2)+5
        if tmp1 < 25: tmp1=cipherBox[tmp1]
        else: tmp1=cipherBox[tmp1-25]
        if tmp2 < 25: tmp2=cipherBox[tmp2]
        else: tmp2=cipherBox[tmp2-25]
        elm=tmp1+tmp2
        #print(elm + " - col",end="\t")
    else:
        tmp1=cipherBox[int(pos1/5)*5+(pos2%5)]
        tmp2=cipherBox[int(pos2/5)*5+(pos1%5)]
        elm=tmp1+tmp2
        #print(elm + " - box",end="\t")
    crypto+=elm

print("Encrypted: "+crypto)

