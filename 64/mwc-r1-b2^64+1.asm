
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

        mov rbp,18446744073709543164    ; a
        lea rdi,[rel buf]
        mov rsi,rdi
align 32
next:
        ; 18446744073709543164*18446744073709551617**1-1 340282366920938307569940440512347496187
        ; 340282366920938307569940440512347496186: 2 170141183460469153784970220256173748093

        mov rdx,rbp
        test rax,rax
        jz skip
        mul rbp
skip:   add rax,rbx
        adc rdx,0

        sub rax,rdx
        ja ok
        jnz adjust

        xchg rax,rdx
        jmp ok

adjust: inc rax
        dec rdx

ok:     mov rbx,rdx

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
