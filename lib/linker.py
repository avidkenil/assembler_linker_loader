#!/usr/bin/python
__author__ = 'mayankgupta'
import assembler
from assembler import varTable
from assembler import varScope

############GLOBAL VARIABLE#####################
externVar={}        #LIST CONTAIN ALL EXTERN VARIABLE
machineCodeLen={}   #contain number of machine codes in that file
################################################


def initFunc(fileNames):

    for fileName in fileNames:
        newCode=[]
        fileName=fileName.replace('input', 'output').replace('asm', 's')
        filePt=open(fileName,'r')
        fileName = fileName.split('.')[0].split('/')[-1].lstrip().rstrip()

        externVar[fileName]=[]
        oldCode=filePt.read()
        lines=oldCode.split('\n')
        for line in lines:
            line=line.lstrip().rstrip()
            if 'EXTERN' in line:
                extVar=line.split(' ')[1]
                for fileName2 in fileNames:
                    fileName2=fileName2.replace('input', 'output').replace('asm', 's')
                    fileName2 = fileName2.split('.')[0].split('/')[-1].lstrip().rstrip()
                    if extVar in varTable[fileName2] and varScope[fileName2][extVar]== 'GLOBAL':
                        
                        externVar[fileName].append(extVar)
            else:
                newCode.append(line)
        linkFile = open('outputCode/'+fileName+'.l','w+')
        linkFile.write('\n'.join(newCode))
        linkFile.close()

    for fileName in fileNames:
        fileName=fileName.replace('input', 'output').replace('asm', 's')
        fileName=fileName.split('.')[0].split('/')[-1].lstrip().rstrip()
        filePt=open('outputCode/'+ fileName+'.l','r')
        oldCode=filePt.read()
        newCode=[]
        lines=oldCode.split('\n')
        for line in lines:
            line=line.lstrip().rstrip()
            operands = line.split(' ')[1:]
            for operand in operands:
                operand.lstrip().rstrip()
                operand=operand.split('+')[0]

                if operand in externVar[fileName]:
                    addr=externAddr(operand,fileNames)
                    line=line.replace(operand,str(addr)+"#"+operand)
            newCode.append(line)
        loadFile = open('outputCode/'+ fileName+'.l','w+')
        loadFile.write('\n'.join(newCode))
        loadFile.close()


def externAddr(var,fileNames):
    for fileName in fileNames:
        fileName=fileName.split('.')[0].split('/')[-1].lstrip().rstrip()
        if var in varTable[fileName] and varScope[fileName][var]=='GLOBAL':
            return varTable[fileName][var]











