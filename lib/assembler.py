#!/usr/bin/python
__author__ = 'mayankgupta'

import sys

###########GLOBAL VARIABLES ###############
opLen={}        #LEN OF STANDARD ASSM LANGUAGE OPCODES
labelTable={}   #DICT FOR LABELS AND THEIR ADDRESS IN PERTICULAR FILE labelTable[filename][label]=address_of_label
varTable={}     #key var of type DS and DB value of key is address of starting memory or value of var
varScope={}     #var and scope dictionary varScope[filename][var]=LoOCAL/GLOBAL
machineCodeLen={}   #contain number of machine codes in that file
###########################################


#FILELIST AFTER PREPROCESS ALL IN UPPER CASE




# CREATE SYMBOL TABLE
def firstPass(fileList):
    createAsmOpcode()

    for fileName in fileList:
        fileName=fileName.replace('input', 'output').replace('asm', 'pre')
        currentAddress=0                                             #ASSUME START ADDRESS OF EACH FILE IS 0 IN MEMORY
        filePt=open(fileName,'r')
        fileName = fileName.split('.')[0].split('/')[-1]               #ext of file is not needed further

        labelTable[fileName]= {}
        varTable[fileName]  = {}
        varScope[fileName]  = {}

        code=filePt.read()
        lines=code.split('\n')
        for line in lines:
            line=line.lstrip().rstrip()
            if not line=='':
                label=''
                if len(line.split(':')) > 1:
                    label=line.split(':')[0].lstrip().rstrip()
                    if line.split(':')[1].lstrip().rstrip()=='' or line.split(':')[1].lstrip().rstrip()=='NOP':
                        labelTable[fileName][label]=currentAddress

                if 'DS' in line:
                    var = line.split(':')[0].split(' ')[-1].lstrip().rstrip()
                    varTable[fileName][var]=currentAddress
                    varScope[fileName][var] = scopeVar(line)
                    currentAddress=currentAddress+int(line.strip('DS')[1].lstrip().rstrip())
                if 'DB' in line:
                    var = line.split(':')[0].split(' ')[-1].lstrip().rstrip()
                    varTable[fileName][var] = currentAddress
                    varScope[fileName][var] = scopeVar(line)
                    currentAddress = currentAddress + len(line.split(','))
                if 'EQU' in line:                                           #EQU not require currentAddress=currentAddress+1 as it does not allocate memory give EQU only decimal constants
                    
                    var = line.split(':')[0].split(' ')[-1].lstrip().rstrip()
                    varTable[fileName][var] = line.split('EQU')[1].rstrip().lstrip()
                    varScope[fileName][var] = scopeVar(line)
                    
                elif not 'EXTERN' in line:
                    opcode = line.split(' ')[0].lstrip().rstrip()
                    if opcode in opLen:
                        currentAddress = currentAddress + int(opLen[opcode])
        machineCodeLen[fileName]=currentAddress
        tableFile = open('outputCode/'+fileName+'.table', 'w+')
        codeLabel = ''
        variables = ''
        codeLabel = '***********************LABELS***********************\n'
        if fileName in labelTable:
            for label in labelTable[fileName]:
                codeLabel = codeLabel + label + "\t" + str(labelTable[fileName][label]) + '\n'
        codeLabel = codeLabel + '***********************LABELS***********************\n'
        variables = '***********************VARIABLES***********************\n'
        if fileName in varScope:
            for var in varScope[fileName] :
                variables = variables + var + "\t" + str(varTable[fileName][var]) + "\t" + varScope[fileName][var] + '\n'
        variables = variables + '***********************VARIABLES***********************\n'
        tableFile.write(codeLabel + variables)
        filePt.close()
        tableFile.close()
    raw_input("1st pass done...\n--------Press Enter to continue--------")



def secondPass(fileList):

    for fileName in fileList:
        #file must be input from preProcess
        fileName=fileName.replace('input', 'output').replace('asm', 'pre')
        filePt = open(fileName, 'r')
        fileName = fileName.split('.')[0].split('/')[-1]
        code =  filePt.read()
        code=code.upper()
        lines = code.split('\n')
        tempCode = []
        for line in lines:
            line=line.lstrip().rstrip()
            if not line=='':
                
                if ':' in line:
                    label=line.split(':')[0]
                    label=label.lstrip().rstrip()
                    
                    if not label=='':
                        if label in labelTable[fileName]:
                            line=line.split(':')[1].lstrip().rstrip()
                    else:
                        print "incorrect syntex"
                        sys.exit()
                elif 'DB' in line:
                    line = 'DB ' + line.split('DB',1)[1]
                    line=line.lstrip().rstrip()
                    pars = line.split('DB',1)[1].split(',')                                  #contains parameters after DB
                    for par in pars:
                        par=par.lstrip().rstrip()
                        if par in varTable[fileName]:                       # DB var+9,code  // code: EQU 12h
                            line = line.replace(par,'$'+str(varTable[fileName][par]))
                        elif par.split('+')[0].strip() in varTable[fileName]:
                            offset = par.split('+')[-1]
                            if offset.isdigit() :
                                offset = int(offset)
                            else :
                                offset = 0
                            line = line.replace(par,'$'+str(varTable[fileName][par.split('+')[0].strip()]+offset))
                elif 'DS' in line:
                    line='DS '+line.split('DS')[1]
                    line=line.lstrip().rstrip()
                    par=line.split('DS')[1].lstrip().rstrip()
                    if par in varTable[fileName]:                       # DS code  // code: EQU 2h
                        line = line.replace(par,'$'+str(varTable[fileName][par]))
                    elif par.split('+')[0].strip() in varTable[fileName]:
                        offset = par.split('+')[-1]
                        if offset.isdigit() :
                            offset = int(offset)
                        else :
                            offset = 0
                        line = line.replace(par,'$'+str(varTable[fileName][par.split('+')[0].strip()]+offset))
                else:
                    tags = line.split(' ')
                    for tag in tags:
                        if tag in labelTable[fileName]:
                            line = line.replace(tag,'$'+str(labelTable[fileName][tag]))
                        elif tag.split('+')[0].strip() in varTable[fileName]:
                            add = tag.split('+')[-1]
                            if add.isdigit() :
                                add = int(add)
                            else :
                                add = 0
                            line = line.replace(tag,'$'+str(varTable[fileName][tag.split('+')[0].strip()]+add))

                tempCode.append(line.lstrip().rstrip())
        filePt.close()
        code = '\n'.join(tempCode)
        outputFile = open('outputCode/'+fileName+ '.s', 'w+')
        outputFile.write(code)
        outputFile.close()

    raw_input("2nd pass done...\n--------Press Enter to continue--------")
#GENERATE DICTIONARY OF ASSEMBLY LANGUAGE OPCODES AND LENGTHS

def createAsmOpcode():
    opcodeLength = open('opcodes/opcodeslength.config', 'r')
    opCodes=opcodeLength.read()
    lines=opCodes.split('\n')
    for opCode in lines:
        opCode=opCode.lstrip().rstrip()
        if not opCode=='':
            length=opCode.split(' ')[1]
            op=opCode.split(' ')[0]
            opLen[op]=length
    opcodeLength.close()

def scopeVar( line ):
    if 'GLOBAL' in line :
        return 'GLOBAL'
    else :
        return 'LOCAL'



def initFunc(fileList):
    firstPass(fileList)
    secondPass(fileList)
