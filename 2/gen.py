#!/usr/bin/env python3

# vim:set ts=2 sts=2 sw=2 et ai fdm=marker:

from __future__ import division, print_function
import sys


def _gwc(a, x=1, r=1, b=10, g=0, W=16):
  Q = [0 for _ in range(W)]
  Q0 = Q[:]
  i = 0
  c0 = c = 1

  t = tuple([((a, b, c, d))
             for a in range(2) for b in range(2) for c in range(2)
             for d in range(2)])

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


def _awc(a, b=2, r=8, g=-1):
  Q = [0 for _ in range(r)]
  Q0 = Q[:]

  if a >= r:
    return

  if g == 1:
    c = 0
  if g == 3:
    c = 0
    Q[0] = 1
  else:
    c = 1

  R = 0
  S = r - a
  while True:
    yield Q[R]
    #(c, Q[R]) = divmod(Q[R] + Q[S] + c, b)
    #c = b - 1 - c

    if g == 0:
      (c, Q[R]) = divmod(Q[S] + Q[R] + c, b)
    elif g == 1:
      (c, Q[R]) = divmod(b - 1 - Q[S] - Q[R] - c, b)
    elif g == 2:
      (c, Q[R]) = divmod(Q[S] - Q[R] - c, b)
    elif g == 3:
      (c, Q[R]) = divmod(Q[R] - Q[S] - c, b)
    else:
      sys.exit(1)

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

r = int(sys.argv[1])
for a in range(1, r):
  for gtype in range(4):
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
          if len(buf) < 40:
            buf += "01" [x]

        if delta == g_period:
          #print('cycle', r, a, f_period, buf[:-100])
          print('cycle', gtype, r, a, f_period, buf[:40])
          break
      except StopIteration:
        print('exception', r, a, f_period, g_period)
        break
    #print(r,a,f_period,g_period)
