; program to swap data between two memory locations


jmp start
extern var
start: 
swp var[0],var[1]
mvi c, var[0]
mov b, c
hlt