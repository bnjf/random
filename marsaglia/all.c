#include <assert.h>
#include <limits.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#ifndef B
#define B 256
#endif

#ifndef CLASS
#error generator class not defined
#endif

#define CLASS_AWC 1
#define CLASS_AWCC 2
#define CLASS_SBBI 3
#define CLASS_SBBII 4

static char const* const class_names[] = {
      [CLASS_AWC] = "awc", [CLASS_AWCC] = "awc-c",
  [CLASS_SBBI] = "sbb-i", [CLASS_SBBII] = "sbb-ii"
};

void handler(int sig)
{
  fputs(strsignal(sig), stderr);
  fputs("\n", stderr);
  exit(1);
}

int main(int argc, char* argv[])
{
  uint8_t buf[PIPE_BUF];
  int i;

  unsigned int c;
  unsigned int r0 = atoi(argv[1]);
  unsigned int s0 = atoi(argv[2]);
  unsigned int r = r0 - r0, s = r0 - s0;
  uint8_t Q[r0];

  fprintf(stderr, "%s: b=%u r=%u s=%u\n", class_names[CLASS], B, r0, s0);
  signal(SIGINT, handler);
  signal(SIGHUP, handler);
  signal(SIGPIPE, handler);

  for (i = 0; i < r0; i++) {
    //Q[i] = i + 1;
    Q[i] = 0;
  }

  i = 0;

#if CLASS == CLASS_AWCC
  c = 0;
#elif CLASS == CLASS_SBBII
  c = 0;
  Q[0] = 1;
#elif CLASS == CLASS_AWC || CLASS == CLASS_SBBI
  // AWC can't start with a zero state
  c = 1;
#else
#error generator not defined
#endif

  while (1) {
#if CLASS == CLASS_AWC
    int x = Q[s] + Q[r] + c; // AWC
    Q[r] = x % B;
    c = x >= B;
#elif CLASS == CLASS_AWCC
    int x = (2 * B) - 1 - Q[s] - Q[r] - c; // AWC-c
    Q[r] = x % B;
    c = Q[s] + Q[r] + c >= B;
#elif CLASS == CLASS_SBBI
    int x = B + Q[s] - Q[r] - c; // SBB-I
    // (010989)
    Q[r] = x % B;
    c = x < B;
#elif CLASS == CLASS_SBBII
    int x = B + Q[r] - Q[s] - c; // SBB-II
    // (01123595505617977528089887640449438202247191)
    Q[r] = x % B;
    c = x < B;
#else
#error unknown generator
#endif

    //fprintf(stderr, "%u c %u\n", Q[r], c);

    buf[i++] = Q[r];

    if (++r >= r0)
      r = 0;
    if (++s >= r0)
      s = 0;

    if (i == PIPE_BUF) {
      size_t rv = write(1, buf, PIPE_BUF);
      if (rv != PIPE_BUF) {
        fprintf(stderr, "write failed: %ld\n", rv);
        exit(1);
      }
      i = 0;
    }
  }
}
