; File: DataTypes.nasm
; Author: Ryan Villarreal
; 

global _start

section .text

; main functionality hasn't changed from helloWorld.asm
_start:
	; print hello world to the screen
	mov eax, 0x4
	mov ebx, 0x1
	mov ecx, message
	mov edx, mlen
	int 0x80

	; exit the program gracefully
	mov eax, 0x1
	mov ebx, 0x1
	int 0x80


; Data section has changed to show different ways to Take data
section .data

	var1: db 0xAA
	var2: db 0xBB, 0xCC, 0xDD
	var3: dw 0xEE
	var4: dd 0xAABBCCDD
	var5: dd 0x112233
	var6: TIMES 6 db 0xFF

	message: db "Hello, World!"
	mlen equ $-message

; BSS section for - this is for unitialized data 
section .bss

	var7: resb 100
	var8: resw 20