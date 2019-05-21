
; vim:set sts=8 ts=8 sw=8 et ai fdm=marker nowrap:

%use smartalign

section .bss
buf:    resq 8192
.len equ $ - buf

section .text
global _start
_start:
        mov eax,1       ; x
        mov ebx,0       ; c

        mov rbp,18446744073709550874            ; a
        lea rdi,[rel buf]
        mov rsi,rdi
align 32
next:
        ; 18446744073709550874*18446744073709551616**1-1 340282366920938449775890504739280912383
        ; 340282366920938449775890504739280912382: 2 170141183460469224887945252369640456191

        mul rbp
        add rax,rbx
        adc rdx,0
        mov rbx,rdx

        stosq
        cmp rdi,buf+buf.len
        jb next

        push rax
        mov rax,1               ; sys_write
        mov rdi,3               ; fd 3
        ; rsi already loaded
        ;lea rsi,[rel buf]
        mov rdx,buf.len
        syscall
        pop rax

        mov rdi,rsi
        jmp next
