
; vim:set sts=8 ts=8 sw=8 et ai fdm=marker:

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

        ; 130*256**32+1
        ;mov ah,130              ; ax+=(al<<7)+al
        ; 207*256**32+1
        mov ah,207
        mul ah

        add ax,cx

;        add al,ah
;        jnc ok
;        inc al
;        inc ah
;ok:
        not al
;        dec al


        stosb
        mov cl,ah

        cmp rdi,Q_end
        jb next

        ; write Q[16] out

        push rdx
        push rcx        ; unused, but clobbered by syscall
        mov rax,1       ; sys_write
        mov rdi,3       ; fd 3
        mov rsi,Q
        mov rdx,Q_end-Q
        syscall         ; XXX not checking the amount written
        pop rcx
        pop rdx

        ;extern stdout, fwrite
        ;push rcx
        ;mov rcx,stdout
        ;mov edx,1
        ;mov esi,Q_end-Q
        ;mov rdi,Q
        ;push r10
        ;push r11
        ;call fwrite
        ;pop r11
        ;pop r10
        ;pop rcx

        mov rdi,Q     ; reset
        mov rsi,Q
        jmp next

