
fPtr=open('sampLab.txt','r')
dict={'a':0}
for file in fPtr:
	for let in file:
		if not let.isalpha(): continue
		let=let.lower()
		if let in dict:
			dict[let]+=1
		else: dict[let]=1	

fPtr.close()
fPtr=open('outLetters.txt','w')
for key in sorted(dict):
	fPtr.write(key)
	fPtr.write(':')
	fPtr.write((str)(dict[key]))
	fPtr.write('\n')
	

fPtr.close()
