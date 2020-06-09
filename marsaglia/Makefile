
B?=256

.PHONY: all clean
	
all: awc awcc sbb1 sbb2

clean:
	rm -f awc awcc sbb1 sbb2

awc: all.c
	gcc -O9 -march=native -fprofile-generate -Wall all.c -o $@ -DCLASS=CLASS_AWC -DB=${B}

awcc: all.c
	gcc -O9 -march=native -Wall all.c -o awcc -fprofile-generate -DCLASS=CLASS_AWCC -DB=${B}

sbb1: all.c
	gcc -O9 -march=native -Wall all.c -o sbb1 -fprofile-generate -DCLASS=CLASS_SBBI -DB=${B}

sbb2: all.c
	gcc -O9 -march=native -Wall all.c -o sbb2 -fprofile-generate -DCLASS=CLASS_SBBII -DB=${B}
