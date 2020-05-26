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

b = 10
a = 11
d = a * b - 1
r = 2
s = 1

columns = 4  # width of vectors


def f(n):
  if n < 0:
    n = n % d
    n = n - 1
  else:
    n = n % d
  return ((b**(d - 1 - n)) // d) % b


def c(n):
  return 0 if n < b else 1


x = 0
y = 0
V = [
    tuple([f(x * (d // columns) + y) for x in range(columns)])
    for y in range(-r * 2, 0)
]
i = len(V) - 1
C = [{
    True: 1,
    False: 0
}[V[i][x] < V[i - r][x] + V[i - s][x]] for x in range(columns)]

import pprint
# pprint.pprint(V)
# pprint.pprint(C)

#for _ in range(d-r*2):
for _ in range(d // columns - r * 2):
  i += 1
  V.append(
      tuple([(V[i - r][x] + V[i - s][x] + C[x]) % b for x in range(columns)]))
  C = [{
      True: 1,
      False: 0
  }[V[i][x] < V[i - r][x] + V[i - s][x]] for x in range(columns)]

pprint.pprint(V)
pprint.pprint(C)
