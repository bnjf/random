#!/usr/bin/env python

import sys

w = 256
m = w + 1

def add_modm(x,y):
    a = x
    a = a - m
    a = a + y
    if a < 0:
       a = a + m
    return a/w,a%w

def sub_modm(x,y):
    a = x
    a = a - y
    if a < 0:
        a = a + m
    return a

def mul_modm(a, x):
    if x == 0:
        x = w
    rA = a * x
    (rX,rA) = divmod(rA, w)
    rA = rA - rX
    if rA < 0:
        rA = rA + 1
        rX = rX - 1
    return rX, rA % w

# recall: (A + B) mod C = (A mod C + B mod C) mod C
def mul_add_modm(a, x, c):
    rA = 0
    rX = 0

    if x == 0:
        x = w
    rA = a * x + c

    (rX,rA) = divmod(rA, w)

    rA = rA - rX
    if rA < 0:
        rA = rA + 1
        rX = rX - 1
    elif rA == 0:
        # XXX cheat.  assuming we'll get called with the same `a`, handle 0
        # properly and return the result of f(f()) instead
        #
        # this is not quite right though.  we need to fetch the next the next
        # element for the case of MWC r>1, and move all the elements
        # n_1,n_2,n_3 -> n_2,n_3,...
        #
        # ... which is quite expensive when using a circular buffer
        (rX,rA)=(rA,rX)

    return rX, rA % w

for a in xrange(1,w):
    for x in xrange(0,w):
        for c in xrange(0,w):
            print mul_add_modm(a, x, c), a, x, c, ' # mul_add_modm'
            print divmod(a*(x or w)+c,m), a, x, c, ' # real divmod'

