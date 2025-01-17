; Filename: logicaloperators.nasm
; author: whoops, Ryan here
; 
; Purpose: procedures in Assembly


global _start

section .text

HelloWorldProc:
	; Print Hello World using write syscall
	mov eax, 0x4
	mov ebx, 1
	mov ecx, message
	mov edx, mlen
	int 0x80
	leave ; allows for restore
	ret ; signifies end of procedure - returns to PrintHelloWorld

_start:

	mov ecx, 0x10

PrintHelloWorld:
	; preserve registers and stack
	pushad
	pushfd

	call HelloWorldProc ; call the procedure HelloWorldProc - setups the syscall

	; restore registers and stack
	popfd
	popad
	
	loop PrintHelloWorld ; loop through PrintHelloWorld 10 times

	; exit(0) gracefully
    mov eax, 1
    mov ebx, 0
    int 0x80

section .data
	; message is a label
	; db is nasm opcode that stands for define byte/bytes
	message: db "Hello, World!"
	mlen equ $-message