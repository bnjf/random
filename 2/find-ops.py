#!/usr/bin/env python3

# vim:set ts=2 sts=2 sw=2 et ai fdm:marker

from quine_mccluskey.qm import QuineMcCluskey
import itertools as it
import sys

#qm = QuineMcCluskey()
qm = QuineMcCluskey(use_xor=True)

#for o in list( filter( lambda s: len(s) == 2, [qm.simplify(list(_), []) for _ in it.combinations(range(8), 3)])):
#for o in list( filter( lambda s: len(s) == 2, [qm.simplify(list(_), []) for _ in it.combinations(range(8), 3)])):
seen_expr = set()
for o in list(
    filter(lambda s: len(s) < 4, [
        qm.simplify(list(_), []) for _ in it.chain(
            it.combinations(range(8), 2),
            it.combinations(range(8), 3),
            it.combinations(range(8), 4))
    ])):
  s = ""
  seen_terms = set()
  for f in sorted(o):
    #c = it.cycle(('Q[i]', 'Q[j]', 'c'))
    c = it.cycle('xyc')
    #c = it.cycle('cyx')
    op_cnt = 0
    op = '&'
    xors = []
    ands = []
    for (t, v) in zip(reversed(f), c):
      if t == '-':
        continue
      elif t == '0':
        ands.append(f'~{v}')
      elif t == '1':
        ands.append(f'{v}')
      elif t == '^':
        xors.append(f'{v}')
      elif t == '~':
        xors.append(f'~{v}')
      else:
        print(f'unknown t: {t}')
        sys.exit(1)
      seen_terms.add(v)
    if xors:
      s += f"({' ^ '.join(xors)})"
      if ands:
        s += f' & {ands[0]}'
        if len(ands) > 1:
          print('more than one and!')
          sys.exit(1)
    else:
      s += ' & '.join(ands)
    s += " | "

  if s[-3::] == " | ":
    s = s[:-3]

  if len(seen_terms) > 0 and s not in seen_expr:
    print(f'({s}) & 1, # {sorted(o)}')
    seen_expr.add(s)

