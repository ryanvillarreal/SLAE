; Filename: exit.nasm
; Author: whoa, it's yo boi!
; Purpose - Learning to use syscall with shellcode


global main

section .text
main:
	; fixing the bad characters
	xor eax, eax ; xor of the same variable is always zero.  Which will get rid of anything in eax
	mov al, 1
	xor ebx, ebx
	mov bl, 10
	int 0x80