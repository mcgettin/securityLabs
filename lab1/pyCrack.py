

fPtr=open('sampLab.txt','r')
fOut=open('decrypted.txt','w')
offset=9

for file in fPtr:
	for let in file:
		if not let.isalpha():
			fOut.write(let)
		else:
			let=let.lower()
			let=ord(let)+offset
			if(let>122): let-=26
			fOut.write(chr(let))

fPtr.close()
fOut.close
