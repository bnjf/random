
%use smartalign

global _start

section .text

_start:
        xor r8,r8       ; period
        mov ecx,0x01010101 ; Q[4]
        mov ebx,1       ; c (bl, but clearing upper too)

        mov edi,buf
        mov edx,A       ; a
align 32
next:
        mov dx,A
        mov ax,cx
        ;stosw

        mul dx
        add ax,bx
        adc dx,0

        ; mod 65537 handling
        sub ax,dx
        ja no_wrap
        jnz adjust

        ;stosw          ; XXX probably need to remove this to avoid 0 bias
        inc r8          ; we'll skip a state, bump period
        xchg ax,dx
        mov dx,A
        sub ax,dx
adjust: inc ax
        dec dx

no_wrap:
        neg ax          ; cmwc

        mov cx,ax
        mov bx,dx

        ;rol cx,8       ; Q[i++]-ish
        ;rol ecx,8

        inc r8          ; period++

        cmp ecx,0x01010101
        jnz next

        ;call write_buf

        cmp bx,1
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
buf:    resw 1000000

