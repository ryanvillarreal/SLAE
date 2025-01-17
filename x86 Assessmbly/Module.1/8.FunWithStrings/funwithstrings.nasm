; Filename: logicaloperators.nasm
; author: moar Ryan
; 
; Purpose: Whooooo so much fun with Strings in Assembly


global _start

section .text
_start:

	; copy a string from src to dst
	mov ecx, sourcelen
	lea esi, [source]
	lea edi, [destination]

	cld ; clear direction flag
	rep movsb

	; Print Hello world using write syscall
	mov eax, 0x4
	mov ebx, 0x1
	mov ecx, destination
	mov edx, sourcelen
	int 0x80

	; string comparison with cmpsb
	; compare source and destination
	mov ecx, sourcelen
	lea esi, [source]
	lea edi, [comparison]
	repe cmpsb

	jz SetEqual
	mov ecx, result2
	mov edx, result2Len

SetEqual:
	mov ecx, result1
	mov edx, result1Len

Print: 
	mov eax, 0x4
	mov ebx, 0x1
	int 0x80

	; exit(0) gracefully
    mov eax, 1
    mov ebx, 0
    int 0x80


section .data
	; message is a label
	; db is nasm opcode that stands for define byte/bytes
	source: db "Hello, World!"
	sourcelen equ $-source

	comparison: db "Hello"

	result1: db "Strings are Equal", 0xA
	result1Len equ $-result1

	result2: db "Strings are Unequal", 0xA
	result2Len equ $-result2


section .bss
	destination: resb 100