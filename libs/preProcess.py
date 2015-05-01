#store the opcodes used in the input code and replace with corresponding assembly instructions

#contains all opcodes and their parameters
opcodeTable={}
#instruction set corresponding to each output
opcodeIns={}

def initFunc(files):
	global fileNames=files
	
	createOpcodeTable()
	for fileName in fileNames
		replaceOpcodes(fileName)

#store all opcodes in a table
def createOpcodeTable():
	opcodeFile=open('opcodes/opcodes.config', 'r')
	lines=opcodeFile.readlines()
	#current opcode in the line
	currentOpcode=''
	#set of instructions in the currentOpcode
	currentOpcodeIns=''
	#true between opcode and opend
	ins=False
	for line in lines:
		line=line.lstrip().rstrip().replace('\n', '')
		if 'OPCODE' in line:
			ins=True
			currentOpcode = line.split(' ')[1]
			opcodeTable [currentOpcode] = line.split(currentOpcode)[1].split(',')
		elif 'OPEND' in line:
			ins = False
			opcodeIns[currentOpcode] = currentOpcodeIns
			currentOpcode=''
			currentOpcodeIns=''
		elif ins:
			currentOpcodeIns += line + '\n'

def replaceOpcodes():
	inpFile=open('fileName', 'r')
	lines=inpFile.readlines().upper()

	replace=True
	while replace:
		replace=False
		for line in lines:
			line=line.lstrip().rstrip().replace('\n', '')
			temp = line.split(' ')[0]
			if temp in opcodeTable:
				replace=True
				arguements = line.split(' ', 1)[1].split(',')
				##################### convert var[1] to var + 1 ##############################
				for a in arguements:
					a=a.lstrip().rstrip()
					a=a.replace('[', '+').replace(']', '')
				############################################################################
				currentOpcode=temp
				currentOpcodeIns=opcodeIns[currentOpcode]
				dummyvars=opcodeTable[currentOpcode]
				########################### replace dummy variables by the arguements ###################
				i=0
				for x in dummyvars:
					x=x.lstrip().rstrip()
					currentOpcodeIns=currentOpcodeIns.replace(x, arguements[i])
					i += 1
				##############################################################################
		