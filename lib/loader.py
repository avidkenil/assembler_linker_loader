#merge the files and specifies memory locations for all variables

import assembler, re
from assembler import varTable,varScope,machineCodeLen

def initFunc(fileNames):
    offset=0
    newCode=[]
    for fileName in fileNames:

        fileName=fileName.replace('input', 'output').replace('asm', 'l')
        filePt=open(fileName,'r')
        fileName = fileName.split('.')[0].split('/')[-1].lstrip().rstrip()

        oldCode=filePt.read()
        lines=oldCode.split('\n')
        for line in lines:
            line.lstrip().rstrip()
            if not line=='':
                pars=line.split(' ',1)
                if len(pars) >=2:
                    parameters=pars[1]
                    pars=parameters.split(',')
                    for par in pars:
                        par=par.lstrip().rstrip()
                        if '$' in par:
                            val=par.split('$')[1]
                            val1=int(val)+int(offset)
                            pat=par[1:]
                            pattern=re.compile(pat)
                            print pattern, line
                            for m in pattern.finditer(line):
                                if m.start()==len(line)-1:
                                    if line[m.start()-1]=='$' and line[m.start()-1]=='$':
                                        line = line[:m.start()] + str(val1) + line[m.end():]
                                elif not line[m.start() + len(par)-1].isdigit():
                                    if line[m.start()-1]=='$' and line[m.start()-1]=='$':
                                        line = line[:m.start()] + str(val1) + line[m.end():]
                        elif '#' in par:
                            val=par.split('#')[0]
                            add=par.split('+')[1]
                            if add=='':
                                add=0
                            val1=int(val)+int(add)
                            var=par.split('#')[1].split('+')[0]
                            for fileName2 in fileNames:
                                fileName2=fileName2.split('.')[0].split('/')[-1].lstrip().rstrip()
                                if var in varTable[fileName2] and varScope[fileName2][var]=='GLOBAL':
                                    tempLength=0
                                    for fileName3 in fileNames:
                                        if fileName2==fileName3.split('.')[0].split('/')[-1].lstrip().rstrip():
                                            break
                                        tempLength += machineCodeLen(fileName3.split('.')[0].lstrip().rstrip())
                                    break
                            val1=val1+tempLength
                            line=line.replace(par,'$'+str(val1))
            if not 'HLT' in line:
                newCode.append(line)
        offset+=machineCodeLen[fileName]
    newCode.append('HLT')
    loadFile = open('outputCode/'+ fileNames[0].split('.')[0].split('/')[-1]+'.load','w+')
    loadFile.write('\n'.join(newCode))
    loadFile.close()


