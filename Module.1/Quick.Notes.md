###Video 001

###Video 002

###Video 003

###Video 004

###Video 005

###Video 006

###Video 007


###Video 008 - 
/usr/include/i386-linux-gnu/asm/ looking at the system calls that are available to use.  
We need to write to the screen, so lets use the write system call
int 0x04 - NR_write


###Video 009
gdb commands used:
stepi
next
set diassembly-flavor intel
disassemble
`break _start`
`break *address `


###Video 010
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


###Video 011
Moving Data
MOV - most common
LEA - Load Effective Address - load pointer values
XCHG - Exchanges (swaps) values

For some reason my MovingData.nasm is not compiling and linking correctly -jk had not seen the data section yet

print/x $eax - displays register
info registers - displays all registers