
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
        mov dx,A
        mov ax,cx
        ;stosw

        or ax,ax
        jz skip
        mul dx
skip:   add ax,bx
        adc dx,0

        sub ax,dx
        ja no_wrap
        jnz adjust

        ;stosw          ; XXX probably need to remove this to avoid 0 bias
        inc r8          ; we'll skip a state, bump period
        xchg ax,dx
        jmp no_wrap

adjust: inc ax
        dec dx

no_wrap:
        mov cx,ax
        mov bx,dx

        ;rol cx,8       ; Q[i++]-ish
        ;rol ecx,8

        inc r8          ; period++

        cmp ax,1
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
buf:    resw 100000000

