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
"\xeb\x1b\x31\xc0\xb0\x04\x31\xdb\xb3\x01\x31\xc9\x59\x31\xd2\xb2\x12\xcd\x80\x31\xc0\xb0\x01\x31\xdb\xb3\x0a\xcd\x80\xe8\xe0\xff\xff\xff\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64\x21\x0a";

int main()
{
    printf("Shellcode size: %d\n", strlen(shellcode));
    int (*ret)() = (int(*)())shellcode;
    ret();
}