#!/usr/bin/env perl

use strict;
use warnings;
use v5.10;

use Math::GMP ":constant";

my ( $b, $r, $a );

$b = shift // 256;
my $step = shift;

for ($r = 1; $r <= 256; $r += $step ? 1 : $r) {
  for ($a = ($b - 2); $a > 0; $a--) {

    say "$a*$b**$r-1 ", $a * $b**$r - 1
    if Math::GMP->new( $a * $b**$r - 1 )->probab_prime(25);
    say "$a*$b**$r+1 ", $a * $b**$r + 1
    if Math::GMP->new( $a * $b**$r + 1 )->probab_prime(25);
  }
}

