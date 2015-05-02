#store the opcodes used in the input code and replace with corresponding assembly instructions
#handles the functions in the input assembly code

#contains all opcodes and their parameters
opcodeTable={}
#instruction set corresponding to each output
opcodeIns={}
#store function and corresponding arguements
functionTable={}
#store instructions in functions
functionIns={}


def initFunc(files):
	createFunctionTable(files)
	for fileName in files:
		replaceFunction(fileName)
	createOpcodeTable()
	for fileName in files:
		replaceOpcodes(fileName)
	
	

def createFunctionTable(files):
	
	for fileName in files:

		inpFile=open(fileName, 'r')
		fileName=fileName.split('.')[0]
		
		insPresent=False
		currentFunctionIns=''
		currentFunction=''
		lines=inpFile.readlines()
		for line in lines:
			line=line.lstrip().rstrip().replace('\n', '').upper()
			temp = line.split(' ', 2)

			
			if temp[0] == 'MACRO':
				insPresent=True
				currentFunction = line.split(' ')[1]
				functionTable [currentFunction] = line.split(currentFunction)[1].split(',')

			elif temp[0] == 'MEND':
				insPresent=False
				functionIns[currentFunction] = currentFunctionIns
				currentFunction=''
				currentFunctionIns=''
			elif insPresent==True:
				currentFunctionIns += line + '\n'
		inpFile.close()


def replaceFunction(fileName):
	inpFile=open(fileName, 'r')
	lines=inpFile.readlines()
	code=''
	macroPresent=False
	for line in lines:
		line=line.lstrip().rstrip().replace('\n', '').upper()
		temp = line.split(' ')[0]
		
		if 'MACRO' in line:
			macroPresent=True
			line=''
		elif 'MEND' in line:
			macroPresent=False
			line=''
		elif macroPresent==True:
			line=''
			
		if temp in functionTable:
			
			arguements = line.split(' ', 1)[1].split(',')
			
			i=0
			##################### convert var[1] to var+1 ##############################
			for a in arguements:
				a=a.lstrip().rstrip()
				a=a.replace('[', '+').replace(']', '')
				arguements[i]=a
				i += 1
			############################################################################
			

			currentFunction=temp
			currentFunctionIns=functionIns[currentFunction]
			dummyvars=functionTable[currentFunction]
			
			########################### replace dummy variables by the arguements ###################
			i=0
			for x in dummyvars:
				x=x.lstrip().rstrip()
				currentFunctionIns=currentFunctionIns.replace(x, arguements[i])
				i += 1
			code += currentFunctionIns+'\n'
			##############################################
		else:
			code += line + '\n'
	outFile=open('outputCode/'+fileName.split('.')[0].split('/')[-1]+'.pre', 'w')
	outFile.write(code)
	
	outFile.close()
	f=open('outputCode/'+fileName.split('.')[0].split('/')[-1]+'.pre', 'r')
	print f.read()
	f.close()
	inpFile.close()





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
	opcodeFile.close()

def replaceOpcodes(fileName):
	
	inpFile=open('outputCode/' +fileName.split('.')[0].split('/')[-1]+'.pre' , 'r')
	lines=inpFile.readlines()
	code=''
	
	for line in lines:
		line=line.lstrip().rstrip().replace('\n', '').upper()
		temp = line.split(' ')[0]
		if len(line.split(' ', 1))>=2:
			arguements = line.split(' ', 1)[1].split(',')
			i=0
			##################### convert var[1] to var + 1 ##############################
			for a in arguements:
				a=a.lstrip().rstrip()
				a=a.replace('[', '+').replace(']', '')
				arguements[i]=a
				i += 1
			############################################################################
		if temp in opcodeTable:
			
			currentOpcode=temp
			currentOpcodeIns=opcodeIns[currentOpcode]
			dummyvars=opcodeTable[currentOpcode]
			########################### replace dummy variables by the arguements ###################
			i=0
			for x in dummyvars:
				x=x.lstrip().rstrip()
				currentOpcodeIns=currentOpcodeIns.replace(x, arguements[i])
				i += 1
			code += currentOpcodeIns+'\n'
			##############################################
		else:
			code += line + '\n'
	outFile=open('outputCode/'+fileName.split('.')[0].split('/')[-1]+'.pre', 'w')
	code=code.replace(' DS', ': DS')
	code=code.replace(' DB', ': DB')
	code=code.replace('EXTERN', 'EXTERN:')
	outFile.write(code)
	outFile.close()
	inpFile.close()
