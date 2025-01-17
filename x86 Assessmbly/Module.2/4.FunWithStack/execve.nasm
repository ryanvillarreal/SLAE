; execve.asm
; Author: Ryan 
; Looking up answers for this why it throws a segfault on execution. 
; Abatchy: NOTE: This code will segfault if ocmpiled directly because it attempts
; to modify "message", which is inside the .text segment and is marked read-only
; in order to get this shellcode to work get the hex encoded version and dump into
; our shellcode skeleton c program

; define the global start where the label _start is
global _start


; text section is where you want to keep the actual functionality
section .text

_start:
	; jmp-pop-call 
	jmp short jmp_message


jmp_back:
	; esi contains the address of string in memory
	pop esi
	; clear ebx
	xor ebx, ebx
	; the +9 is from counting the string
	mov byte [esi +9], bl 

	; moving the address of esi into the bbbb section
	mov dword [esi +10], esi

	; now cccc needs to get overwritten by all Cs
	mov dword [esi +14], ebx

	; load the effective addresses
	lea ebx, [esi]
	lea ecx, [esi + 10]
	lea edx, [esi + 14]


	; fixing the bad characters and exiting
	xor eax, eax
	mov al, 0xb ; syscall for execve
	int 0x80


jmp_message:
	call jmp_back
	; so basically the way this string is setup is calling /bin/bash
	; the A represents the null terminator after /bin/bash
	; the B's are going to be the address of the message /bin/bash?  I think?
	; the C's are going to be null terminated instructions
	message db "/bin/bashABBBBCCCC"