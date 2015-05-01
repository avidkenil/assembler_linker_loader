# assembler_linker_loader
Assembler-linker-loader for 8085 simulator

## Authored By
* Aishwarya Agarwal
* Kenil Tanna
* Mayank Gupta

## Pre-requisites
* Python 2.7
* XAMPP

## About
This is a web-based application which takes input assebly language program and outputs executable machine language program. It has three basic features – Mnemonic operation codes, Symbolic operands, and Data declarations. Our software aims at converting simple assembly language code defined on an instruction set into 8085 assembly code, linking different files and their variables and loading it in appropriate location in the memory as defined by the user. It involves three basic functions- Assembling, Linking and Loading.

> Some pre-processiong is done too. It converts mnemonic opcodes to machine language instruction set, ensures case-insensetivity of the assembly language, etc. 

**Assembler** converts assembly language program to machine language format, resolves symbolic names for memory locations and variables. This can also be extended to incorporate macros.

**Linker** links the files with each other. Its function is to store the EXTERN variables and mark them for loader.

**Loader** asks the user for memory location to load the program. The output file `fileName.asm` can be run on [GNUSim8085](http://gnusim8085.org/)
