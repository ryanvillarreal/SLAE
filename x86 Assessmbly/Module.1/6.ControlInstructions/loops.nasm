; Filename: logicaloperators.nasm
; author: moar Ryan
; 
; Purpose: Loopy Dee Scoop De Boop


global _start

section .text
_start:
	jmp Begin

NeverExecute: 
	mov eax, 0x10
	xor ebx, ebx

Begin:
	; this will be your counter.  set it to how many times you want to print
	mov ecx, 0x5 ; loop depends on ecx

PrintHW:
	push ecx ; push eax onto the stack so we can keep track of the counter
	; print Hello world using syscall
	mov eax, 0x4 ; need this for writing the syscall
	mov ebx, 1
	mov ecx, message
	mov edx, mlen
	int 0x80

	; pop ecx off the stack to get the counter
	pop ecx
	loop PrintHW ; loop will automatically check ecx to see if conditions are met

	; exit(0) gracefully
    mov eax, 1
    mov ebx, 0
    int 0x80


section .data
	; message is a label
	; db is nasm opcode that stands for define byte/bytes
	message: db "Hello, World!"
	mlen equ $-message