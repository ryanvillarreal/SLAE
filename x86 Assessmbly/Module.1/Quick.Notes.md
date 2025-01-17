## Module 1
### Video 001

Code needed for pretty much every assembly program
    ; exit(0) gracefully
    mov eax, 1
    mov ebx, 0
    int 0x80

### Video 002

### Video 003

### Video 004

### Video 005

### Video 006

### Video 007


### Video 008 - 
/usr/include/i386-linux-gnu/asm/ looking at the system calls that are available to use.  
We need to write to the screen, so lets use the write system call
int 0x04 - NR_write


### Video 009
gdb commands used:
```
stepi
next
set diassembly-flavor intel
disassemble
break _start
break *address 
```


### Video 010
Fundamental Data Types
Byte, Word, Double Word, Quad, Double Quad
signed and unsigned
Accessing memory reference with []
mov eax, message <-- moves address into eax, like a pointer
mov eax, [message] <-- moves the value into eax

Defining Initialized Data in NASM
db, dw, dd, dq, dt

Special Tokens 
$ - evaluates the current line
$$ - evaluates to the beginning of current section
times - times 64 db 0 - run db 0 64 times

Little Endian Format slide

you can type `shell` in gdb to pass command line commands.  
`shell readelf -h DataTypes`
This will help you find out where the entry point is if you can't find it. 
You can use the examine byte of the address or variable to see the value inside
x/xb 0x0804a000
x/xb &var1
`print` inside of gdb will print the information of the variable or address specified


### Video 011
Moving Data
MOV - most common l
LEA - Load Effective Address - load pointer values
XCHG - Exchanges (swaps) values

For some reason my MovingData.nasm is not compiling and linking correctly -jk had not seen the data section yet

print/x $eax - displays register
info registers - displays all registers

### Video 012
In GDB you can define a hook-stop which I believe allows you to define functions within GDB so you don't have to type a ton of commands over and over. 
Syntax: 
(gdb) define hook-stop
Type commands for definition of "hook-stop".
End with a line saying "end" .
	> x/8xb $esp
	> x/4xh $esp
	> X/3xw $esp
	> Disassemble $eip,+10
	> end

Reiterating that bytes are 0x00 two bytes would be 0x0011 four bytes would be 0x00112233
STACK GOES DOWN!!!  When pushing to stack you subtract!! When popping from stack you add!


### Video 013
Arithmetic Instructions
ADD dst, src
ADC dst, src (plus carry flag)
SUB and SBB
INC and DEC
Carry flag is when extending forward i.e. 0x90 + 0x10

You can set, clear, complement the carry flag
clc - clear
stc - set
cmc - complement (basically an inverse of what is ever set currently.  If set, unset.  If unset, set)

Whenever an operation arrives at a zero sum it will set the ZF eflag

On your own look at Multiply and Divide


### Video 014
Mul - multiplication
Div - division 

When overflowing with multiplication it will use both registers to store the value.  
You can disassemble anywhere in the code by referencing disassemble `_start`
you can use display to display a register on every instruction

the result of the division of 16bit will be split into two registers.  the first for the times divided, and the second register for the remainder

Signed Arithmetic 
imul - signed multiplication
idiv -  signed division


### Video 015
Logical Operators
AND r/m, r/m/imm (8,16,32 bits)
OR
XOR
NOT

Might need to reivew logical operations.  
It's helpful to write out all of the logical operators to figure out what is happening. 

SAR - Shift Arithmetic Right
SHR - Shift Logical Right
ROR - 
ROL - 



### Video 016
Control instructions will control the flow of the program
Based on events e.g. calculation led to 0
uses flags to determine decision
Branching
	- unconditional JMP
	- conditional Jxx

Uncoditional - compare it with the GOTO statement in C
Types:  These types will be important for jumping to our code caves for shellcoding
	- Near Jump: Current Code Segment - Short -128 to +127 from current position
	- Far jump: in another segment

Jxx - Conditional - These cannot be used for far jumps
	- Just a few examples: JZ, JNZ, JA, JAE, JC, JNC
	- uses flags

Alright so you can define "Functions" inside assemblly using camel case and a colon afterwards i.e.
`Begin:`

There is no way to ignore a jmp instruction.  

I believe the JNZ was replaced with JNE because of optimization 


### Video 017
Looking at the looping functions of ia32. 
Seems that the loop instruction will check to see if conditions are met

short video

### Video 018
Set of operations grouped together
Called often from different places in the code
`CALL <procedure_name>`
in NASM procedures are defined by labels

Once you are done with the procedure you need to the RET instruction
tells the CPU to return to the previous procedure that was called

Organization isn't super important, but nice to have procedures above the `_start` function

The assembly instruction call will push the address onto the stack to keep track of where it needs to return. 
In order to test this we open gdb and use x/xw $esp (2 bytes of the stack at the time of call).  The address of 
the procedure being left is pushed to the stack

Arguments to a procedure
	- Passed via registers
	- passed on the stack
	- passed as data structures in memory referenced by registers / or on stack

Saving and Restoring State
	- Saving/restoring registers
		- pushad/popad
	- saving restoring flags
		- pushfd/popfd
	- saving/restoring
		- enter / leave + ret
 

### Video 019
Another short video
Using pushad/pushfd - popad/popfd
When you leave a procedure mov esp, ebp and pop ebp is the same as the leave instruction
Check out the Enter instructions


### Video 020
Looking at strings in Asm
MOVS (MOVS/MOVSW/MOVSD) - 
CMPS - Compares
SCAS - Subtracts
LODS - Loads
LEA - Load Effective Address (additional one remembered by me)

ESI and EDI registers are typically used with DF

MOVSB - mov byte by byte
MOVSW - mov word by word
MOVSD - move something

rep - similar to mov - instruction will continue to run until the ecx becomes not zero
other variations of rep

direction of which the copying is happening.  
x/15cb &destination - shows the bytes being copied byte by byte

### Video 021
Libc and NASM
Syscalls are good but sometimes too low level at times
Standard C library libc has tons of useful functions
calling libc functions from Assembly

Things to Remember: 
Define all libc functions you want to use with extern
all arguments in reverse order on stack
	- CALL function (a,b,c,d)
	- push d, push c, push b, push a

adjust the stack after calllinb libc function
link with GCC rather than LD -use main instead of `_start`

`man 3 printf` gets the man page for printf. 
Tried compiling with just the code given in the course, but it seems to fail to do the lookup
