#!/bin/sh

for max in "$@"; do
  sh -c '
    ./find-primes.py 2 "${0:?}" 3 |
    while read type form r s p safe; do
      echo "$type $form $r $s $(cpulimit -l 50 -f -- ./order.py $p | grep ok) $safe"
    done' "$max" |
  tee "$max.out"
done
