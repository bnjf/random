#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h> 

uint64_t f(void) {
  static uint64_t hi = 0, lo = 1;

  asm("mulq    %%rbx\n\t"
      "movq    %%rdx, %%rsi\n\t"
      "xchgq   %%rax, %%rdi\n\t"
      "mulq    %%rbx\n\t"
      "addq    %%rsi, %%rax\n\t"
      "adcq    $0, %%rdx\n\t"
      "shlq    $1, %%rax\n\t"
      "rclq    $1, %%rdx\n\t"
      "shrq    $1, %%rax\n\t"
      "addq    %%rdi, %%rdx\n\t"
      "adcq    $0, %%rax\n\t"
      "xchgq   %%rdx, %%rax\n\t"
      "jns     .Lstore%=\n\t"
      "shlq    $1, %%rdx\n\t"
      "shrq    $1, %%rdx\n\t"
      "incq    %%rax\n"
      ".Lstore%=:"
      : "=a" (lo), "=d" (hi) 
      : "a" (lo), "D" (hi), "b" (13835058055282156213U)
      : "cc", "rsi");

  return lo;
}

int main(int argc,char *argv[]) {
  uint64_t buf[1024];

  for (int i = time(NULL); i > 0; i--) { (void)f(); }

  for (;;) {
    for (int i = 0; i < 1024; i++){
      buf[i] = f();
    }
    fwrite(buf, sizeof(uint64_t), 1024, stdout);
  }

  return 0;
}
