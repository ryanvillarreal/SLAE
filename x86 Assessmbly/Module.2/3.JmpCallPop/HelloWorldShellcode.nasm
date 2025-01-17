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

	jmp short call_shellcode


shellcode:
	; clear eax with XOR in order to not introduce bad chars
	xor eax,eax
	; print Hello, World on the screen
	mov al, 0x4

	; clear ebx with XOR in order to not introduce bad chars
	xor ebx, ebx
	mov bl, 0x1

	; you don't have to xor this one?
	pop ecx

	; clear edx with XOR in order to not introduce bad chars
	; counted manually for some reason
	xor edx, edx
	mov dl, 0x12 ; this was counted by hand
	
	int 0x80 ; issue the syscall that is in eax

	; fixing the bad characters
	xor eax, eax ; xor of the same variable is always zero.  Which will get rid of anything in eax
	mov al, 1
	xor ebx, ebx
	mov bl, 10
	int 0x80


call_shellcode:
	call shellcode
	message: db "Hello, World!", 0xA