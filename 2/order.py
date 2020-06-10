#!/usr/bin/env python3

# vim:set ts=2 sts=2 sw=2 et ai fdm=marker:

import itertools
import functools
from sympy import gcd, lcm, isprime, primefactors

# some examples:
'''
cycle 0 32 2 4294967290 1000101110100001100100100000001000001001
cycle 0 32 4 2147483639 1001110101001111101011000010011101010000
cycle 0 32 6 2147483615 0100100111001111000100011111101001011111
cycle 1 32 2 2147483645 1111100010110100111101111011100000000100
cycle 1 32 4 4294967278 0100100100001110110111100100111000000100
cycle 1 32 6 4294967230 0111110111110010001110001110101001111110
'''

import sys

#for n in [257, 263, 271, 383, 241, 193, 251, 239, 223, 191, 127]:
#for n in [ 61441, 63487, 64513, 65407, 65519, 65521, 65537, 65539, 65539, 65543, 65551, 65599, 66047, 73727, 81919 ]:
exit_code = 0
for n in sys.argv[1:]:
  n = int(n)
  #n = 73727 #4294967291
  phi_n = n - 1
  b = 2
  orders = []
  if not isprime(n):
    sys.exit(1)
  # f = factors of phi(n)
  ok = True
  for f in primefactors(phi_n):
    x = pow(b, phi_n // f, n)
    print('{}^({}/{}) mod {} == {}'.format(b, phi_n, f, n, x))
    if x == 1:
      ok = False
      exit_code = 1
      break
  print('{}: {}'.format(n, {True:"ok", False: "not ok"}[ok]))

  # loops = []
  # for x in range(1, n):
  #   if pow(b, x, n) == 1:
  #     print('{}^{} mod {} == {}'.format(b, x, n, 1))
  #     loops.append(x)
  # print('{}: {}'.format(n, loops))

sys.exit(exit_code)

