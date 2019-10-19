;..................................................................
;Name : adterm.asm
;Author : Rohit Mohan
;Date Updated : 26th June, 2015
;Version : 1.0
;Description : A full-screen console display of text
;..................................................................

section .data

SCREENWIDTH equ 80
PosTerm : db 27,"[01;01H"
POSLEN equ $-PosTerm
ClearTerm : db 27,"[2J"
CLEARLEN equ $-ClearTerm
AdMsg : db "Welcome Rohit!!"
ADLEN equ $-AdMsg
Prompt : db "Press Enter : "
PROMPTLEN equ $-Prompt
GreenBack : db 27,"[30;47m"
GREENLEN equ $-GreenBack

;A table to convert binary numbers upto 80 to their ascii equals.
;Save them in a 16 bit register (since they are two digits).

Digit : 
	db "0001020304050607080910111213141516171819"
	db "2021222324252627282930313233343536373839"
	db "4041424344454647484950515253545556575859"
	db "606162636465666768697071727374757677787980"

section .bss

section .text

;..................................................................
;Name of proc : ClearScr
;Date Last Updated : 26/6/2015 
;IN : none
;OUT : none
;MODIFIES : none
;CALLS : WriteStr
;DESCRIPTION : Clear console by sending pre-defined control string
;..................................................................

ClearScr :
	push ecx
	push edx
	mov ecx, ClearTerm
	mov edx, CLEARLEN
	call WriteStr
	pop edx
	pop ecx
	ret

;...................................................................
;Name : GotoXY
;Date Last Updated : 26/6/2015
;IN : X in AH, Y in AL
;OUT : none
;MODIFIES : PosTerm (memory)
;CALLS : WriteStr
;DESCRIPTION : Puts curosor on any position on the screen
;...................................................................

GotoXY :
	push ebx
	push ecx
	push edx

	xor ebx, ebx
	
;modifying the Y cordinate
	mov bl, al
	mov cx, word [Digit + ebx * 2]
	mov word [PosTerm + 2], cx
;modifing the X cordinate
	mov bl, ah
	mov cx, word [Digit + ebx * 2]
	mov word [PosTerm  + 5], cx
;send the esc sequence to stdout
	mov ecx, PosTerm
	mov edx, POSLEN
	call WriteStr
	
	pop edx	
	pop ecx
	pop ebx
	ret

;.......................................................................
;Name of Proc : WriteCtr
;Date Last Updated : 26/6/15
;IN : Y in AL, String in ECX, Length in EDX
;OUT : None
;MODIFIES : AH (with value for X)
;CALLS : GotoXY, WriteStr
;DESCRIPTION : Displays string in the center of the screen
;.......................................................................
WriteCtr :
	push ebx
	xor ebx, ebx 
	mov bl, SCREENWIDTH
	sub bl, dl
	shr bl, 1
	mov ah, bl
	call GotoXY
	call WriteStr
	pop ebx
	ret

;.........................................................................
;Name of Proc : WriteStr
;Date Last Updated : 26/6/15
;IN : string in ECX, string length in EDX
;OUT : None
;MODIFIES : Nothing
;CALLS : sys_write
;DESCRIPTION : Writes string on terminal using sys_write system call
;.........................................................................
WriteStr : 
	push eax
	push ebx
	mov eax, 4
	mov ebx, 1
	int 80h
	pop ebx
	pop  eax
	ret

;........................................................................
; Main 
;.......................................................................

global _start

_start :
	nop

;Turn background green
	mov ecx, GreenBack
	mov edx, GREENLEN
	call WriteStr

;Clear screen
	call ClearScr

;print ad message
	mov al, 12
	mov ecx, AdMsg
	mov edx, ADLEN
	call WriteCtr

;position and display prompt message
	mov ax, 0117h
	call GotoXY
	mov ecx, Prompt
	mov edx, PROMPTLEN
	call WriteStr

;wait for user to press enter
	mov eax, 3
	mov ebx, 0
	int 80h

;quit program
Exit :
	mov eax, 1
	mov ebx, 0
	int 80h

	






































































	
	
	
	
