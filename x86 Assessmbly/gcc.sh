#!/bin/bash

# Bash script that will take our assembly nasm file and assemble and link with GCC
# GCC is being used to use external libraries now.
if [[ $# -eq 0 ]] ; then
    echo 'Need to pass the file to assemble and link.'
    exit 0
fi

echo '[+] Assembling with NASM ...'
nasm -f elf32 -o $1.o $1.nasm
echo '[+] Linking ... using gcc'
gcc -m32 -o $1 $1.o
echo '[+] Done!'

# Launch gdb?
read -p "Want to launch in GDB? [y/n]" -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi
gdb ./$1

