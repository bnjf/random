#!/usr/bin/env python3

#
# 1/109 can be made with:
#
#   x[i] = x[i-2] + x[i-1] + c[i-1] div b
#   c[i] = x[i-2] + x[i-1] + c[i-1] mod b
#
# with b=10 and c=1 to kick things off.  its period is 108, 2*2*3*3*3.  to
# perform this in parallel, split the period by the column count... XXX this is
# not ideal unless the column count is congruent to the period because the
# other columns will overlap with previous values.
#
# let's split into 3 as a demo


def f(n):
  n = n % 109
  return ((10**(108 - n)) // 109) % 10


def c(n, b=10):
  return 0 if n < b else 1


V = [
        (f(0 * 36), f(1 * 36), f(2 * 36)),
        (f(0 * 36 + 1), f(1 * 36 + 1), f(2 * 36 + 1)),
     ]
C = [
    c(f(0 * 36) + f(0 * 36 - 1)),
    c(f(1 * 36) + f(1 * 36 - 1)),
    c(f(2 * 36) + f(2 * 36 - 1)),
]
i = 1

import pprint
pprint.pprint(V)
pprint.pprint(C)

for _ in range(34):
  i += 1
  V.append((
      (V[i - 2][0] + V[i - 1][0] + C[0]) % 10,
      (V[i - 2][1] + V[i - 1][1] + C[1]) % 10,
      (V[i - 2][2] + V[i - 1][2] + C[2]) % 10,))
  C = [
      c(V[i - 2][0] + V[i - 1][0] + C[0]),
      c(V[i - 2][1] + V[i - 1][1] + C[1]),
      c(V[i - 2][2] + V[i - 1][2] + C[2]),
  ]

pprint.pprint(V)
pprint.pprint(C)

