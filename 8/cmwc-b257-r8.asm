
; vim:set sts=8 ts=8 sw=8 et ai fdm=marker nowrap:

%use smartalign

section .data
align 16
Q:
db 1,2,3,4,5,6,7,8
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

        ; 198*257**8+1
        mov ah,198
        mul ah
        add ax,cx

        ; adjust for mod b+1.  not sure if the branching is ideal.  we take in
        ; order "ok", "adjust", and finally no branch for the zero leap
check:  sub al,ah
        ja ok
        jnz adjust

        ;stosb                  ; don't sto 0, otherwise we'll bias

        ; straightforward, or ...
        ;xchg al,ah
        ;mov ah,198
        ;sub al,ah

        ; ... since we know al is 0, so we can overload sub here to do an
        ; implied load.  this optimization is of probably of limited use
        ; elsewhere.
        sub ax,(198-1 << 8) | (-198 & 255)
        xchg al,ah

adjust: inc al
        dec ah
ok:     neg al                  ; using neg here.  257-1-al = 256-al = 0-al = neg al
        mov cl,ah

        stosb

        cmp rdi,Q_end
        jb next

        ; write Q[8] out

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

