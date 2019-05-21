
%use smartalign

global _start

section .text

_start:
        xor r8,r8       ; period
        mov eax,1       ; Q[4]
        mov ecx,1       ; Q[4]
        mov ebx,1       ; c (bl, but clearing upper too)

        mov edi,buf
        mov edx,A       ; a
align 32
next:
        mov edx,A
        ;mov eax,ecx
        ;stosw

        or eax,eax
        jz skip
        mul edx
skip:   add eax,ebx
        adc edx,0

again:  sub eax,edx
        ja no_wrap
        jnz adjust

        ;stosw          ; XXX probably need to remove this to avoid 0 bias
        inc r8          ; we'll skip a state, bump period
        xchg eax,edx
        jmp no_wrap

adjust: inc eax
        dec edx

no_wrap:

        ;mov ecx,eax
        mov ebx,edx

        inc r8          ; period++

        cmp eax,1
        jnz next

        ;call write_buf

        cmp ebx,1
        jnz next

        mov edx,A       ; for gdb, TODO change this to another reg
done:
        ;call write_buf

        mov rdi,rax
        mov rax,60      ; sys_exit
        syscall

write_buf:
        ;write the buf out
        push rdx
        push rsi
        push rcx        ; unused, but clobbered by syscall

        mov rax,1       ; sys_write
        mov rdx,rdi
        mov rdi,3       ; fd 3
        mov rsi,buf
        sub rdx,rsi
        syscall         ; XXX not checking the amount written

        pop rcx
        pop rsi
        pop rdx
        mov rdi,buf     ; reset

        ret

section .bss
buf:    resw 100000000

