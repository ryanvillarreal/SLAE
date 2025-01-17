## Module 2
### Video 022
Introduction to Shellcoding - Basics
Shellcode - machine code with a specific purpose
	- spawn a local shell
	- bind to port and spawn shell
	- create a new account

Can be executed by the CPU directly - no further assembling/linking or separate compilinig required
Shellcode is delivered: 
	- Part of an exploit - size of shellcode is important (smaller size=better)
	- Bad characters a concern

Added into an executable
	- Patch exisiting executable for with a code cave and chunk in shellcode
	- Typically size not a concern


Resources: 
	- shell-storm.org/
	- exploit-db.com/
	- projectshellcode.com/

Wrote a basic ShellcodeSkeleton that will allow us to paste in shellcode and see it execute from a c code


### Video 023
Exit Shellcode - calling syscall
So far I have wrote our basic assembly exit call inside the main function
I assembled and linked that exit program
used `objdump -M intel exit` to get the assembly instructions in hex code to paste into our shellcode skeleton
I pasted it in and compiled it.  It worked, but now he is talking about how the null characters are a bad idea. 
Yup.  he right.  once the strlen hits the null byte then it stops counting at 2 bytes. 
Remember bad characters will break the exploit

so let's get rid of the bad chars
Using XOR to fill the characters instead of null is easier
then instead of using the full eax/ebx register just use al/bl

We need a shortcut to dump the assembly into shellcode
https://www.commandlinefu.com/commands/view/6051/get-all-shellcode-on-binary-file-from-objdump
`objdump -d ./shell|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-6 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^/"/'|sed 's/$/"/g'`

compiling shellcode.c
`gcc shellcode.c -m32 -fno-stack-protector -z execstack -o shell`

### Video 024
Longer video
HelloWorld Shellcode using JMP-CALL-POP
Modifying Hello World - Replace all 0x00 opcode instructions
no hardcoded Addresses - dynamically figure out address of "Hello, World" string

ALright so what we have done so far is to copy the HelloWorld.nasm file over to HelloWorldShellcode.nasm
Cleared all the registers with XOR in order to not introduce bad chars
re-wrote all of the registers to only use al/bl/cl/dl
We did leave one register as a full which was ecx - holding the message
However using our getShellcode bash script it looks like ecx still has a bad character in it.  Ahh shit.  it's the address of where the message is being stored that has a null character in it.  
0x804a000 = b9 00 a0 04 08

I think we are going to fix that with a different address anyways.  Because we can't use hardcoded addresses
We should be able to figure out the address of message at runtime
move message to core segment.
JMP-CALL-POP technique: 
CALL instruction is calling a label the next instruction the address of the next instruction is being pushed onto the stack.  it's used when the procedure's ret is finished.  
So the first step is the JMP short Call_shellcode:
jumps to the call shellcode label which calls the function call shellcode: 
The next instruction gets pushed onto the stack.  which will be the address of the hello string onto the stack

so we need to add some labels in order for this to work.  
See the HelloWorldShellcode.nasm



### Video 025
This is slighlty different in that we are go ing to push the message 'Hello, World' onto the stack
Because the stack grows down we will have to push in backwards. 
You can use the python interpreter to quickly reverse a string and convert to hex
```
>>> code = "Hello, World\n"
>>> code[::-1].encode('hex')
```
You can cut down the number of instructions used by push edx which has already been xor'd previously
Not sure why this is working like this

### Video 025a
Looking at the execve call 
`man execve`
/bin/bash,0x0 into ebx
address of /bin/bash, 0x00000000 into ecx
These two specifc things will launch bin bash

No NULLS in shellcode

(this is all determined based off his slide which is the man page discussing the execve command)
so basically the way this string is setup is calling /bin/bash
the A represents the null terminator after /bin/bash
the B's are going to be the address of the message /bin/bash?  I think?
the C's are going to be null terminated instructions
message db "/bin/bashABBBBCCCC"


Looking up answers for this why it throws a segfault on execution. 
Abatchy: NOTE: This code will segfault if ocmpiled directly because it attempts
to modify "message", which is inside the .text segment and is marked read-only
in order to get this shellcode to work get the hex encoded version and dump into
our shellcode skeleton c program

### Video 026
Execve Shellcode Stack method
copying the execve.nasm to execve-stack.nasm


### Video 027

### Video 028

### Video 029

### Video 030

### Video 031

### Video 032

### Video 033

### Video 034

### Video 035

### Video 036
