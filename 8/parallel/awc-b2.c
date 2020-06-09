#include <assert.h>
#include <limits.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void handler(int sig) { fputs(strsignal(sig), stderr); fputs("\n", stderr); exit(1); }

#define B_TYPE uint64_t

int main(int argc, char* argv[])
{
  B_TYPE buf[PIPE_BUF];
  int i, j;

  unsigned int r0 = atoi(argv[1]);
  unsigned int s0 = atoi(argv[2]);
  unsigned int r = r0 - r0, s = r0 - s0;
  B_TYPE Q[r0];
  B_TYPE c;

  fprintf(stderr, "%s: b=%u r=%u s=%u\n", "awc", 2, r0, s0);
  signal(SIGINT, handler); signal(SIGHUP, handler); signal(SIGPIPE, handler);

  //for (i = 0; i < r0; i++) { Q[i] = i; }
  read(0, Q, r0*sizeof(Q[0]));
  c = -1;

  i = j = 0;
  while (1) {
    B_TYPE x = Q[s] ^ Q[r] ^ c;   // AWC
    //B_TYPE x = ~(Q[s] ^ Q[r] ^ c);  // AWC-c

    //c = (Q[s] & Q[r]) ^ (c & (Q[s] ^ Q[r]));
    // by QMK optimisation:
    c = (c | Q[r]) & (c | Q[s]) & (Q[r] | Q[s]);
    Q[r] = x;

    buf[i++] = Q[r];

    if (++r >= r0)
      r = 0;
    if (++s >= r0)
      s = 0;

    /// XXX this is only really true when buf is bytes
    if (i == PIPE_BUF) {
      size_t rv = write(1, buf, PIPE_BUF*sizeof(buf[0]));
      if (rv != PIPE_BUF*sizeof(buf[0])) { fprintf(stderr, "write failed: %ld\n", rv); exit(1); }
      i = 0;
    }
  }
}
