#!/usr/bin/env python3

from sympy import isprime
import sys

B = int(sys.argv[1])
R = int(sys.argv[2])
S = R
if len(sys.argv) > 3:
  S = int(sys.argv[3])

for result in filter(lambda n: n[3], [(
    r,
    s,
    b**r + b**s - 1,
    isprime(b**r + b**s - 1),
    isprime((b**r + b**s - 1) // 2 - 1),)
                                      for b in [B] for r in [R]
                                      for s in range(1, S)]):
  print('AWC    b^r+b^s-1 {} {} {} {}'.format(
      result[0],
      result[1],
      B**result[0] + B**result[1] - 1,
      {True: "(safe!)",
       False: ""}[result[4]],))

for result in filter(lambda n: n[3], [(
    r,
    s,
    b**r + b**s + 1,
    isprime(b**r + b**s + 1),
    isprime((b**r + b**s + 1) // 2 - 1),)
                                      for b in [B] for r in [R]
                                      for s in range(1, S)]):
  print('AWC-c  b^r+b^s+1 {} {} {} {}'.format(
      result[0],
      result[1],
      B**result[0] + B**result[1] + 1,
      {True: "(safe!)",
       False: ""}[result[4]],))

for result in filter(lambda n: n[3], [(
    r,
    s,
    b**r - b**s + 1,
    isprime(b**r - b**s + 1),
    isprime((b**r - b**s + 1) // 2 - 1),)
                                      for b in [B] for r in [R]
                                      for s in range(1, S)]):
  print('SBB-I  b^r-b^s+1 {} {} {} {}'.format(
      result[0],
      result[1],
      B**result[0] - B**result[1] + 1,
      {True: "(safe!)",
       False: ""}[result[4]],))

for result in filter(lambda n: n[3], [(
    r,
    s,
    b**r - b**s - 1,
    isprime(b**r - b**s - 1),
    isprime((b**r - b**s - 1) // 2 - 1),)
                                      for b in [B] for r in [R]
                                      for s in range(1, S)]):
  print('SBB-II b^r-b^s-1 {} {} {} {}'.format(
      result[0],
      result[1],
      B**result[0] - B**result[1] - 1,
      {True: "(safe!)",
       False: ""}[result[4]],))

#print(list(filter(lambda n: n[3], [(r,s,b**r+b**s-1,isprime(b**r+b**s-1)) for b in [B] for r in [R] for s in range(1,r)])))
#print(list(filter(lambda n: n[3], [(r,s,b**r+b**s+1,isprime(b**r+b**s+1)) for b in [B] for r in [R] for s in range(1,r)])))
#print(list(filter(lambda n: n[3], [(r,s,b**r-b**s-1,isprime(b**r-b**s-1)) for b in [B] for r in [R] for s in range(1,r)])))
#print(list(filter(lambda n: n[3], [(r,s,b**r-b**s+1,isprime(b**r-b**s+1)) for b in [B] for r in [R] for s in range(1,r)])))
