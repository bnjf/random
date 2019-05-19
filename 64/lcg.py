#!/usr/bin/env pypy

import sys
import struct

def lcg_parkmiller(x):
    N = 2**127-1
    G = 13835058055282156213
    x = G * x % N
    return x

count = 0
x = lcg_parkmiller(1)
while x != 1:
    sys.stdout.write(struct.pack('I', x & 0xffffffff))
    x = lcg_parkmiller(x)
    count += 1
print count
