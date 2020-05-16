
	processor 6502
	org $1000

vid	equ $0400

start:	
	cli

	; set hires bitmap mode, and video to page 1
	lda #$3b
	sta $d011
	;lda #$18	; multicolour mode
	lda #$8 	; hi res, 1 bit
	sta $d016
	lda #$18
	sta $d018

	lda #$0		; black
	;sta $d021	; set background colour
	sta $d020	; set border colour

	; clear colours
	lda #$04 ; $2000 bit map, $0400 screen
	sta $fc
	lda #$0
	sta $fb

	; colour data.  screen bitmap is 1-bit, and picks the
	; colour from the upper/lower nibble.
	lda #$10	; white / black
	ldx #$4		; 4*256 for palette
	ldy #$0
loopc:	sta ($fb),y
	iny
	bne loopc
	inc $fc
	dex
	bne loopc

clear:	lda #$20 	; $2000 bit map, $0400 screen
	sta $fc
	ldx #$20 	; $2000 - $3fff	
	ldy #0
	;lda #0
loopb:	txa
	adc #1
	and #~3
	sta ($fb),y
	iny
	bne loopb
	inc $fc
	dex
	bne loopb

;;
	; lags, x_{i-256} + x_{i-3} + c
	lda #0		; 256 % 256
	sta $fb
	lda #3		; 3   % 256
	sta $fd
forever:
	lda #$20 	; $2000 bit map, $0400 screen
	sta $fc
	sta $fe	

	ldx #$1e	; count of blocks.  lcm(320,256)=0x500
	ldy #$0
	sec
loop:	lda ($fb),y
	adc ($fd),y
	sta ($fb),y
	iny
	bne loop
	; next block.  XXX we're discarding carry block to block
	inc $fc
	inc $fe
	dex
	bne loop
	beq forever

