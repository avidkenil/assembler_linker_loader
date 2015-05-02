; program to swap data between two memory locations


jmp start
global var db 7,4
start: 

macro swap x1, x2
swp x1, x2
mend

swap var[0], var[1]

hlt