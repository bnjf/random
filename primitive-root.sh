#!/bin/bash

# vim:set ts=2 sw=2 et ai fdm=marker:

set -eu

gcd() {
  #until (( 0 == $2 )); do set -- "$2" "$(( $1 % $2 ))"; done
  #echo "$(( 0 >= $1 ? 0 - $1 : $1 ))"
  { echo "${1?:}"
    echo "${2?:}"
  } | dc -e '??[dSarLa%d0<a]dsax+p' 
}

m=${1:?}
n=${2:?}

# gcd must be 1
g=$(gcd $m $n)
[[ $g == 1 ]] || {
  echo "gcd($m,$n) = $g != 1" >&2
  [[ $g == $m ]] || exit 1
}

phi_n=0
factors=$(python -m primefac $n)
if [[ "$factors" != "$n: $n" ]]; then
  # get the order for each factor
  set -- $(for f in ${factors#*:}; do factor $((f-1)) | awk '{$1="";print}'; done)
  phi_n=$1; shift
  while [[ $# -gt 0 ]]; do
    let phi_n="phi_n * $1"
    shift
  done
else
  # dc helpfully formats long integers, with backslash as a continuation.  join
  # it together.
  phi_n=$(dc <<< "$n 1 - p" | sed -e ':x /\\$/ { N; s/\\\n//g ; bx }')
fi

# unique factors of phi(n), use awk to squeeze
factors=$(python -m primefac $phi_n \
  | awk '{
    print $2
    for (i=2;i<NF;i++) {
      if ($i != $(i+1)) { print $(i+1); }}}')

rv=0
for p in $factors; do
  r=$(dc <<< "$m $phi_n $p / $n | p" | sed -e ':x /\\$/ { N; s/\\\n//g ; bx }' )
  echo "$m^{$phi_n/$p} mod $n == $r" >&2
  x=1
  while [[ $r == 1 ]]; do
    rv=1
    let x=x+1
    r=$(dc <<< "$m $phi_n $p $x ^ / $n | p" | sed -e ':x /\\$/ { N; s/\\\n//g ; bx }' )
    echo "$m^{$phi_n/$p^$x} mod $n == $r" >&2
  done
  if [[ $r == $phi_n ]]; then
    true
  fi
done

exit $rv

