from __future__ import division, print_function

# add
print('A B Ci | S Co')
for x in range(2):
  for y in range(2):
    for c_i in range(2):
      print('{} {} {}  | {} {}'.format(
          x,
          y,
          c_i,
          # add
          x ^ y ^ c_i,
          # carry
          #((x & c_i) | (x & y) | (y & c_i) & 1),
          (x & y) | (c_i & (x ^ y)),))

print('')

# full sub
print('X Y Bi | D Bo')
for x in range(2):
  for y in range(2):
    for b_i in range(2):
      print(
          '{} {} {}  | {} {}'.format(
              x,
              y,
              b_i,
              # sub
              x ^ y ^ b_i,
              # borrow
              #(~x & b_i | ~x & y | y & b_i) & 1),
              #(~x & b_i | ~x & y | y & b_i) & 1),
              ((x & y & b_i) | (~x & (y | b_i))) & 1),
          #(-x * b_i + -x * y + y * b_i) % 2,
      )
