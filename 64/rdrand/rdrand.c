#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

static uint64_t f(void) {
  uint64_t x;

  /*
   * must be volatile otherwise it can be optimized away:
   * https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html#Volatile
   */
  asm volatile(".Lretry%=:\n\t"
               "rdrand %0\n\t"
               "jnc .Lretry%="
               : "=r" (x)
               : /* no input */
               : "cc");

  return x;
}

int main(int argc, char *argv[]) {
  uint64_t buf[1024];

  for (;;) {
    for (int i = 0; i < 1024; i++) {
      buf[i] = f();
    }
    fwrite(buf, sizeof(uint64_t), 1024, stdout);
  }

  return 0;
}
