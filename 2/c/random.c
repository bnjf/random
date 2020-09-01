#include <immintrin.h>
#include <stdio.h>
#include <unistd.h>

/*#define R 23*/
/*#define S 20*/

#define R 128
#define S 54

/*
 * 23 104 19 6 524351 1
 * 23 120 19 6 524351 1
 * 23 104 19 12 528383 1
 * 23 120 19 12 528383 1
 * 23 104 19 18 786431 1
 * 23 120 19 18 786431 1
 */
//#define R 23
//#define S 4
#if S >= R
#error "short lag should be less than R"
#endif

__m256i Q[R];
__m256i c = { 0, 0, 0, 0 };
void f()
{
  for (int i = 0, j = R - S; i < R; i++, (j = (j + 1) % R)) {
    __m256i t = Q[i] ^ Q[j] ^ c;

    //c = (Q[i] & Q[j]) | (Q[i] & c) | (Q[j] & c); // awc

    //c = (~Q[i] & c) | (~Q[i] & Q[j]) | (Q[j] & c); // sbb-i
    // aka ~(~y & ~c | (y ^ c) & x)
    // aka ~((~y & ~c | (~y ^ ~c) & x))
    c = _mm256_or_si256(
          _mm256_or_si256(
            _mm256_andnot_si256(Q[i], c),
            _mm256_andnot_si256(Q[i], Q[j])),
          _mm256_and_si256(Q[j], c));

    Q[i] = t;
  }
}

void f256()
{
  for (int i = 0, j = R - S; i < R; i++, (j = (j + 1) % R)) {
    __m256i x = _mm256_sub_epi8(_mm256_add_epi8(Q[i], Q[j]), c);
    c = _mm256_cmpgt_epi8(Q[i], x);
    Q[i] = x;
  }
}

#define VSIZE (256 / 8) // avx2

int main(int argc, char* argv[])
{
  fprintf(stderr, "vsize=%u buflen=%u r=%u s=%u\n", VSIZE, R * VSIZE, R, S);
  read(0, &Q, R * VSIZE);
  while (1) {
    ssize_t len = write(1, &Q, (R * VSIZE));
    if (len < R * VSIZE) {
      fprintf(stderr, "write returned %d!\n", len);
      exit(10);
    }
    f();
    //for (int i=0;i<257;i++) { f(); }
  }
}
