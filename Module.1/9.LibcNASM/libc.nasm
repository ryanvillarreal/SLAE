; Filename: libc.nasm
; Author: yo boi!

; Purpose: to learn how to load external libraries. 


extern printf
extern exit

global main

section .text
main: 
	push message 
	call printf
	add esp, 0x4 ; adjust the stack

	mov eax, 0xa
	call exit

section .data
	message: db "Hello, World! \n", 0xA
	mlen equ $-message