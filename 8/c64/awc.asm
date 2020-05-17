
	processor 6502
	org $1000

start:	
	; set hires bitmap mode, and video to page 1
	lda #$3b
	sta $d011
	;lda #$18	; multicolour mode
	lda #$8 	; hi res, 1 bit
	sta $d016
	lda #$18
	sta $d018

	lda #$0		; black
	sta $d020	; set border colour

	; clear colours
	lda #$04 	; $0400 palette
	sta $fc
	lda #$00
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
	lda #0
clear_loop:
	sta ($fb),y
	iny
	bne clear_loop
	inc $fc
	dex
	bne clear_loop

;; seed

	ldy #0
	lda #$20 	; $2000 bit map, $0400 screen
	sta $fc
	ldx #20
	cli
	txa
seed_loop:
	adc $a2
	adc #7
	sta ($fb),y
	inc $fb
	bne seed_loop

; spin for screen
w1: bit $d011
    bpl w1
w2: bit $d011
    bmi w2

	pha
	tya
	clc
	adc #64
	tay
	pla
	bcc seed_next
	inc $fc
seed_next:
	inc $fc		; hi byte
	dex
	txa
	bne seed_loop
	sei

;; main

	; lags, x_{i-256} + x_{i-3} + c
	lda #0		; 256 - 256 % 256
	sta $fb
	lda #-3		; 256 - 3   % 256
	sta $fd

	ldy #0
forever:lda #$20 	; $2000 bit map, $0400 screen
	sta $fc
	sta $fe	

	ldx #20		; how many blocks to show
loop:	; grab the saved carry
	inc $fc
	lda ($fb),y
	lsr		; bit 0 -> carry
	dec $fc
l:	lda ($fb),y
	adc ($fd),y
	sta ($fb),y
	inc $fd		; s++
	inc $fb		; r++
	bne l

	; save carry for this block
	inc $fc
	inc $fe
	lda #0
	rol		; carry -> bit 0
	sta ($fb),y

	tya
	clc
	adc #64
	tay
	bcc next

	; catch up the y delta
	inc $fc
	inc $fe
next:	dex
	bne loop
	beq forever

