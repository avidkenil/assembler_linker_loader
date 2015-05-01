#takes input the codes and calls assembler, linker and loader to process it and generates the output codes

from lib import preProcess, assembler

files=[]

fileName = raw_input('Enter the filename: ')

while (fileName!=''):
	files.append(fileName)
	fileName = raw_input('Enter the filename: ')

preProcess.initFunc(files)
raw_input("Pre-pass done...\n--------Press Enter to continue--------")
assembler.initFunc(files)
