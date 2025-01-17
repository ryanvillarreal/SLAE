; HelloWorld.asm
; Author: Ryan Villarreal
; Build Instructions:
; nasm -f elf32 -o HelloWorld.o HelloWorld.asm
; ld -m elf_i386 -o HelloWorld HelloWorld.o

; define the global start where the label _start is
global _start


; text section is where you want to keep the actual functionality
section .text

; define the program entry point
_start:

	; clear eax
	xor eax,eax
	; print Hello, World on the screen
	mov eax, 0x4
	mov ebx, 0x1
	mov ecx, message
	;mov edx, 0x12 ; this was counted by hand
	mov edx, mlen ; nasm understands mlen and gets the length
	int 0x80 ; issue the syscall that is in eax

	; exit the program gracefully
	mov eax, 0x1
	mov ebx, 0x5
	int 0x80 ; issue the syscall that is in eax

; data section can be used for saving variables, data, etc
section .data
	; message is a label
	; db is nasm opcode that stands for define byte/bytes
	message: db "Hello, World!"
	mlen equ $-message