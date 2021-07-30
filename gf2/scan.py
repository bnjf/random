#!/usr/bin/env python3

import itertools as it
import functools as ft
import sympy as sp

# old python
import operator


def prod(factors):
  return ft.reduce(operator.mul, factors, 1)


def pp(x):
  d = 0
  p = []
  while x:
    if x & 1:
      if d > 1:
        p.append('x^' + str(d))
      elif d == 1:
        p.append('x')
      elif d == 0:
        p.append('1')
    x = x >> 1
    d += 1
  return ' + '.join(reversed(p))


def f(x, p):
  x = x << 1
  if x >= N:
    x = x ^ p
  return x


from math import log


@ft.lru_cache(maxsize=100000)
def gf2mul(x, y, p=11):
  a = 0
  msb = 1 << int(log(p) / log(2))
  while x and y:
    if y & 1:
      a = a ^ x
    x = x << 1
    if x >= msb:
      x = x ^ p
    y = y >> 1
  return a


@ft.lru_cache(maxsize=100000)
def gf2pow(a, power, r):
  a2 = a
  out = 1
  while power:
    if power & 1:
      out = gf2mul(out, a2, r)
    power = power >> 1
    a2 = gf2mul(a2, a2, r)
  return out


def gf2inv(b, r):
  n = int(log(r) / log(2))
  pn2 = (1 << n) - 2
  assert (b != 0)
  return gf2pow(b, pn2, r)


def gf2div(a, b, r):
  binv = gf2inv(b, r)
  return gf2mul(a, binv, r)


if __name__ == '__main__':
  import sys
  N = int(sys.argv[1])  #2**4

  if N < 4 or N & (N - 1) != 0:
    sys.exit(1)
  for p in range(N + 1, N + N, 2):
    N_all = set(range(2, N))
    t = dict()

    # found = False
    # #for x in N_all:
    while N_all:
      x = N_all.pop()

      #     ## brute force
      #     # y = 0
      #     # for y in (x,*N_all):
      #     #     if gf2mul(x,y,p) == 1:
      #     #         #print(f'{x}*{y}')
      #     #         t[x] = y
      #     #         t[y] = x
      #     #         #N_all.remove(x)
      #     #         if x != y:
      #     #             N_all.remove(y)
      #     #         break

      y = gf2inv(x, p)
      if gf2mul(x, y, p) != 1:
        break
      t[x] = y
      t[y] = x
      N_all.remove(y)

    def isprimitive():
      ok = True
      #pf = [3, 5, 17]  #,257]
      pf = sp.primefactors(N - 1)
      root = 2  # x root => primitive poly
      for e in it.chain(*(map(prod, it.combinations(pf, i))
                          for i in range(1, len(pf)))):
        if gf2pow(root, e, p) == 1:
          return False
      if ok and gf2pow(root, N - 1, p) == 1:
        return True
      return False

    if len(t) == N - 2:
      print(f'{hex(p)}{"*" if isprimitive() else ""} {t}')
