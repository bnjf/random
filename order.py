#!/usr/bin/env python

import itertools
from gmpy2 import gcd, lcm

# some examples:

# 1. prime 31 in base 10 (10 isn't a primitive root)
n = 31
phi_n = n - 1
b = 10
orders = []
# f = factors of phi(n)
for f in [2,3,5]:
    #print '# factor',f
    for x in xrange(1,phi_n+1/f):
        if pow(b,f*x,n) == 1:
            #print(f,x)
            orders.append(x)
            break
print '# order of {} in base {}'.format(n, b)
print reduce(lcm,orders)

# 2. prime 61 in base 10 (10 is a primitive root)
n = 61
phi_n = n - 1
b = 10
orders = []
# f = factors of phi(n)
for f in [2,3,5]:
    #print '# factor',f
    for x in xrange(1,phi_n+1/f):
        if pow(b,f*x,n) == 1:
            #print(f,x)
            orders.append(x)
            break
print '# order of {} in base {}'.format(n, b)
print reduce(lcm,orders)

# 3. composite 81 in base 10
n = 81
# when n isn't prime, phi(n) is the product of the factors of n's factors.
# with 81 we have 3^4 as the factorization, and the factors of each minus one:
# 2^4.
phi_n = 16
b = 10
orders = []
# f = factors of phi(n)
for f in [2]:
    #print '# factor',f
    for x in xrange(1,phi_n+1/f):
        if pow(b,f*x,n) == 1:
            #print(f,x)
            orders.append(x)
            break
print '# order of {} in base {}'.format(n, b)
print reduce(lcm,orders)

