; Filename: logicaloperators.nasm
; author: back to Ryan
; 
; Purpose: Learn control instructions in Assembly


global _start

section .text
_start:
	jmp Begin

NeverExecute: 
	mov eax, 0x10
	xor ebx, ebx

Begin:
	; this will be your counter.  set it to how many times you want to print
	mov eax, 0x5

PrintHW:
	push eax ; push eax onto the stack so we can keep track of the counter
	; print Hello world using syscall
	mov eax, 0x4 ; need this for writing the syscall
	mov ebx, 1
	mov ecx, message
	mov edx, mlen
	int 0x80

	; so this is a for loop.  Pop eax which will print the hello world message
	; then will decrement eax by 1.  the JNZ checks to see if it is not zero. 
	; if true (not zero) go back to PrintHW again and loop another time.
	pop eax ; pop eax off the stack so we can update the counter
	dec eax ; update the counter
	jnz PrintHW ; check the conditional jump

	; exit(0) gracefully
    mov eax, 1
    mov ebx, 0
    int 0x80


section .data
	; message is a label
	; db is nasm opcode that stands for define byte/bytes
	message: db "Hello, World!"
	mlen equ $-message