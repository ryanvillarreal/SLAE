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
"\x31\xc0\xb0\x01\x31\xdb\xb3\x0a\xcd\x80";

int main()
{
    printf("Shellcode size: %d\n", strlen(shellcode));
    int (*ret)() = (int(*)())shellcode;
    ret();
}