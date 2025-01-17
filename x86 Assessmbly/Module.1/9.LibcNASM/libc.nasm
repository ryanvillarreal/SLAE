; Filename: libc.nasm
; Author: yo boi!

; Purpose: to learn how to load external libraries. 


; need to use gcc for linking
extern printf ; how to call external libraries. 
extern exit

; changing from _start to main.  
; I believe it's neccessary for the external libraries.
global main

section .text
main: 
	push message 
	call printf ; call the imported printf function
	add esp, 0x4 ; adjust the stack

	mov eax, 0xa
	call exit

section .data
	message: db "Hello, World! \n", 0xA
	mlen equ $-message