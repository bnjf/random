
via http://www.firstpr.com.au/dsp/rand31/

There's `RANDOM.ASM`, which translated almost directly into 64-bit.  The only
major change I made was to eliminate:

```
    test  dx, 8000h
    jz  Store
```

The author might've forgotten that we have a sign flag, and that it will be set
from the previous ADC instruction on the register in question.  So we can
simply write `jns Store` and skip the TEST.

Another catch was writing `AND reg,0x7fff`, because there's no imm64 encoding:
a SHL and accompanying SHR will give the same result.

