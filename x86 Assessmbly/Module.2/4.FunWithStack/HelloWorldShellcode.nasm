; HelloWorld.asm
; Author: Ryan Villarreal
; Build Instructions:
; nasm -f elf32 -o HelloWorld.o HelloWorld.asm
; ld -m elf_i386 -o HelloWorld HelloWorld.o

; define the global start where the label _start is
global _start


; text section is where you want to keep the actual functionality
section .text

_start:
	; clear eax with XOR in order to not introduce bad chars
	xor eax,eax
	mov al, 0x4

	; clear ebx with XOR in order to not introduce bad chars
	xor ebx, ebx
	mov bl, 0x1

	; clear edx with XOR in order to not introduce bad chars
	xor edx, edx
	push edx ; this is done to use less instructions?


	; so here you can push hex encoded string in reverse order to the stack
	; 0a21646c726f57202c6f6c6c6548
	push 0x0a21
	push 0x646c726f
	push 0x57202c6f
	push 0x6c6c6548

	; moving the xor'd ecx onto the stack pointer?
	mov ecx, esp
	mov dl, 0xd
	int 0x80

	; fixing the bad characters
	xor eax, eax ; xor of the same variable is always zero.  Which will get rid of anything in eax
	mov al, 1
	xor ebx, ebx
	mov bl, 10
	int 0x80