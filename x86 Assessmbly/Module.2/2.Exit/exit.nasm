; Filename: exit.nasm
; Author: whoa, it's yo boi!
; Purpose - Learning to use syscall with shellcode


global main

section .text
main:

	mov eax, 1
	mov ebx, 10
	int 0x80