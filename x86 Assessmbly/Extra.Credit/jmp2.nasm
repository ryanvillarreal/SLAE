
[BITS 32]
global _start
_start:
fldz
fnstenv [esp-12]
popecx
add cl, 10
nop
dec ch
dec ch
jmp ecx
