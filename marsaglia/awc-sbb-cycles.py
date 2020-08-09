#!/usr/bin/env python3

# vim:set ts=2 sts=2 sw=2 et ai fdm=marker:

from __future__ import division, print_function

import sys
import functools as ft
import itertools as it
import multiprocessing


def _gwc(a, x=1, r=1, b=10, g=0, W=16):
  Q = [0 for _ in range(W)]
  Q0 = Q[:]
  i = 0
  c0 = c = 1

  t = tuple([((a, b, c, d)) for a in range(2) for b in range(2)
             for c in range(2) for d in range(2)])

  t_x = t[g % 16]
  t_c = t[g // 16]
  #while True:
  #for _ in range(9 * 2**(W * 2)):
  for _ in range(11 + 2 * 2**W):
    yield Q[i]

    # 16 s => 3:114674 7:126914 9:126914 13:114674
    #s = 3
    #j = (Q[i] << 1) | Q[(i-max(1,r-s)) % r]

    # # stuck?
    # if c == t_c[j] and Q[i] == t_x[j]:
    #     break

    # https://oeis.org/A046932
    #(c, Q[i]) = (t_c[j], t_x[j])

    # main operation
    t = t_x[Q[(i - r) % W] << 1 | c]
    #t = t_x[Q[i] << 1 | c]

    # some sort of carry operation, input needs to be the
    # current calculation and the previous carry
    c = t_c[Q[(i - r) % W] << 1 | Q[i]]
    #c = t_c[c << 1 | Q[i]]

    Q[i] = t
    i = (i + 1) % W

    #print (c,Q)
    # cycle
    if Q == Q0 and c == c0:
      break
  while True:
    yield None


def _mwc_bn(a, x=1, r=1, b=10):
  Q = [0 for _ in range(r)]
  Q0 = Q[:]
  i = 0
  c = 1

  while True:
    yield (c, Q[i])
    (c, Q[i]) = divmod(a * Q[i] + c, b)
    i = (i + 1) % r
    #print (c,Q)
    if Q == Q0 and c == 1:
      break


def _lfsr(a, r=4):
  x = 1
  while True:
    if x & 1 == 1:
      x = (x >> 1) ^ a
    else:
      x = (x >> 1)
    yield x


def _xorshift(a, r=4):
  Q = [_ for _ in range(r)]

  #(c, Q[i]) = divmod(a * Q[i] + c, b)
  (a, i) = divmod(a, 8)
  (a, j) = divmod(a, 8)
  (a, k) = divmod(a, 8)
  (a, l) = divmod(a, 8)
  cur = 0
  #print('init',a,i,j,k,l,Q)
  while True:
    yield Q[cur % r]
    Q[cur % r] = (
        # z
        (Q[(cur + 1) % r] ^ ((Q[(cur + 1) % r] << i) & 255)) ^
        # z
        (Q[(cur + 2) % r] ^ ((Q[(cur + 2) % r] >> j) & 255)) ^
        #
        (Q[(cur + 3) % r] ^ ((Q[(cur + 3) % r] << k) & 255)) ^
        #
        (Q[(cur + 4) % r] ^ ((Q[(cur + 4) % r] >> l & 255))))
    cur += 1


@ft.lru_cache()
def awc(x, y, c, b=2):

  t = divmod(x + y + c, b)
  return (b - 1 - t[0], t[1])

  # returns full period for 2^16+2^n-1!
  #return ((~x & ~c | (x ^ c) & ~y) & 1, x ^ y ^ c)

  #return divmod(x + y + c, b)
  l = [0, 0, 0, 0, 0, 0, 0, 0]

  # popcount, essentially
  l[0b000] = (0, 0)
  l[0b001] = l[0b010] = l[0b100] = (0, 1)
  l[0b011] = l[0b101] = l[0b110] = (1, 0)
  l[0b111] = (1, 1)
  return l[x << 2 | y << 1 | c]


@ft.lru_cache()
def awcc(x, y, c, b=2):
  #return divmod(2 * b - 1 - x - y - c, b)
  #return divmod(-x - y - c - 1, b)
  tx = (2 * b) - 1 - x - y - c
  tc = x + y + c
  return (tc // b, tx % b)


@ft.lru_cache()
def sbb1(x, y, c, b=2):
  #return divmod(x - y - c, b)
  tx = x - y - c
  return (0 if tx >= 0 else 1, tx % b)


@ft.lru_cache()
def sbb2(x, y, c, b=2):
  #return divmod(y - x - c, b)
  tx = y - x - c
  return (0 if tx >= 0 else 1, tx % b)


def _awc(a, b=2, r=8, g=-1):
  Q = [0 for _ in range(r)]
  Q0 = Q[:]

  if a >= r:
    return

  Q[0] = 0
  c = 1

  # if g == 1:
  #   c = 0
  # if g == 3:
  #   c = 0
  #   Q[0] = 1
  # else:
  #   c = 1

  R = 0
  S = r - a

  f = [awc, awcc, sbb1, sbb2][g]

  while True:
    yield Q[R]

    #print('{} {} {} {} {} {}'.format(g, Q[S], Q[R], c, *f(Q[S], Q[R], c)))
    (c, Q[R]) = f(Q[S], Q[R], c)

    R += 1
    S += 1
    if R >= r:
      R = 0
    if S >= r:
      S = 0


mwc = _awc

# {{{

# a = 3
# #g_bad = {106, 149, 154, 166, 169, 89}
# g_bad = {}
# g_good = dict()
# W = 13  # XXX r-1
# pairs = {
#     #5: range(1,5),
#     #17: range(17), #[1,3,5,6,8,11,14,15,16],
#     #8: range(1,(8+1)//2),
#     18: range(1,18),
# }

# for W in pairs.keys():
#   for r in pairs[W]:
#     #for g in [105]:
#     for g in range(16 * 16):
#       if g in g_bad:
#         continue
#       f = mwc(a=a, r=r, b=2, g=g, W=W)
#       period = 0
#       x = next(f, None)
#       s = ""
#       while x is not None:
#         if len(s) < 100:
#           s += "01" [x]
#         x = next(f, None)
#         period += 1
#       # if r < 13 and period > 2*2**r:
#       #   print('marking g={} bad r={}'.format(g, r))
#       #   g_bad[g] = g_bad.get(g, 0) + 1
#       # elif r >= 8 and period < r:
#       #   print('marking g={} bad'.format(g))
#       #   g_bad[g] = g_bad.get(g, 0) + 1
#       #else:
#       #if period > r:  # and period < 99999:
#       if period == 11 + (2**W) * 2:
#         g_bad[g] = True
#         period = -1
#       print('r={} g={} W={} period={} s={}'.format(r, g, W, period, s[:100]))
#   #print('good generators: {}'. format(set(range(256)) - g_bad))
# sys.exit(0)
# }}}


#def worker(r=2, a=1, gtype=0):
def worker(args):
  a = args['a']
  r = args['r']
  gtype = args['gtype']

  f = mwc(a=a, r=r, b=2, g=gtype)
  g = mwc(a=a, r=r, b=2, g=gtype)

  f_period = 0
  g_period = 0
  while True:
    try:
      x = next(f)
      y = next(g)
      y = next(g)
      f_period += 1
      g_period += 2

      if x != y:
        continue

      # till f reaches g
      delta = g_period - f_period - r - r
      buf = ""
      while x == y and delta < g_period:
        x = next(f)
        y = next(g)
        delta += 1

      if delta == g_period:
        return (gtype, r, a, f_period)
    except StopIteration:
      return None


if __name__ == '__main__':
  '''
AWC     b^r+b^s-1  20  10  1049599
AWC-c   b^r+b^s+1  20   5  1048609
SBB-I   b^r-b^s+1  20  18   786433
SBB-II  b^r-b^s-1  20   4  1048559

g  0  r  20  s  10  period  524799
g  1  r  20  s  5   period  524304
g  2  r  20  s  18  period  393216
g  3  r  20  s  4   period  524279
'''

  if len(sys.argv) < 2:
    if worker({'r': 20, 'a': 10, 'gtype': 0})[-1] != 524799:
      print('g=0 failed')
      sys.exit(1)
    if worker({'r': 20, 'a': 5, 'gtype': 1})[-1] != 524304:
      print('g=1 failed')
      sys.exit(1)
    if worker({'r': 20, 'a': 18, 'gtype': 2})[-1] != 393216:
      print('g=2 failed')
      sys.exit(1)
    if worker({'r': 20, 'a': 4, 'gtype': 3})[-1] != 524279:
      print('g=3 failed')
      sys.exit(1)
    print('test ok')
    sys.exit(0)

  p = multiprocessing.Pool(processes=3)
  r = int(sys.argv[1])
  for result in p.imap_unordered(
      worker,
      tuple({
          'r': r,
          'a': a,
          'gtype': g
      } for a in range(3, r) for g in range(4))):
    print(result)
