; <filename>.asm
; Author: Ryan 

global _start

section .text
_start:


	; fixing the bad characters
	xor eax, eax ; xor of the same variable is always zero.  Which will get rid of anything in eax
	mov al, 1
	xor ebx, ebx
	mov bl, 10
	int 0x80