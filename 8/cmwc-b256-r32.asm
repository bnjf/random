
; vim:set sts=8 ts=8 sw=8 et ai fdm=marker nowrap:

%use smartalign

section .data
align 16
Q:
db 151, 66, 68,226,205,211, 52,  3, 90,121, 42,136,158,138, 21, 57
db  93, 81,159, 36,255, 32,245, 10,212,147,181, 32,186, 26,176,216
Q_end:

section .text
global _start
_start:
        xor ecx,ecx ; carry
        mov edi,Q
        mov esi,Q

align 32
next:
        lodsb

        ; 207*256**32+1
        ;
        ; period, at best, is roughly 2^259.  I haven't got the order of 3 and 23.
        mov ah,207
        mul ah
        add ax,cx
        not al
        mov cl,ah

        stosb

        cmp rdi,Q_end
        jb next

        ; write Q[16] out

        push rdx
        push rcx                ; unused, but clobbered by syscall
        mov rax,1               ; sys_write
        mov rdi,3               ; fd 3
        mov rsi,Q
        mov rdx,Q_end-Q
        syscall                 ; XXX not checking the amount written
        pop rcx
        pop rdx

        mov rdi,Q               ; reset
        mov rsi,Q
        jmp next

