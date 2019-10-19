SECTION .data

DumpLine: db " 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
DumpLen EQU $-DumpLine
TextLine: db "| ................ |", 10
TextLen EQU $-TextLine
FullLen EQU $-DumpLine

HexDigit: db "0123456789ABCDEF"

TransTable:
	db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
	db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
	db 20h,21h,22h,23h,24h,25h,26h,27h,28h,29h,2Ah,2Bh,2Ch,2Dh,2Eh,2Fh
	db 30h,31h,32h,33h,34h,35h,36h,37h,38h,39h,3Ah,3Bh,3Ch,3Dh,3Eh,3Fh
	db 40h,41h,42h,43h,44h,45h,46h,47h,48h,49h,4Ah,4Bh,4Ch,4Dh,4Eh,4Fh
	db 50h,51h,52h,53h,54h,55h,56h,57h,58h,59h,5Ah,5Bh,5Ch,5Dh,5Eh,5Fh
	db 60h,61h,62h,63h,64h,65h,66h,67h,68h,69h,6Ah,6Bh,6Ch,6Dh,6Eh,6Fh
	db 70h,71h,72h,73h,74h,75h,76h,77h,78h,79h,7Ah,7Bh,7Ch,7Dh,7Eh,2Eh
	db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
	db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
	db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
	db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
	db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
	db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
	db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
	db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh

SECTION .bss
BufLen EQU 16
Buffer resb BufLen

SECTION .text

;..........................................................................
;Procedure Name : ClearLine 
;IN : none
;OUT : none
;CALL : WriteChar
;REG USE : all of caller's registers are backed up 
;DESCRIPTION : Reset the string DumpLine and TextLine to its initial state
;..........................................................................
ClearLine :
	pushad 
	mov edx, 15
repeat:
	mov eax, 0
	call WriteChar
	sub edx, 1
	jae repeat
	popad
	ret

;..........................................................................
;Procedure Name : WriteChar
;IN : character to write in EAX, position to write in EDX
;OUT : none
;CALL: none
;REG USE : ebx, ecx (both saved and restored)
;DESCRIPTION : the value passed in EAX will be put in both the hex dump and
;		text.
;..........................................................................

WriteChar:
	push ebx
	push ecx
; change vlaue in text partition	
	mov bl, byte [TransTable + eax] ; searches the translated value of [EAX] 
	mov byte [TextLine + edx + 2], bl ; write the translated value to memory
; change value in the hex partition
	mov ebx, eax
	lea ecx, [edx*2 + edx] ; multiply by 3 to get position of hex byte in DumpLine
; Extract the high nybble from the byte
	shr bl, 4
	mov bl, byte [HexDigit + ebx]
	mov byte [DumpLine + ecx + 1], bl
; Extract the low nybble from the byte
	and eax, 0Fh
	mov al, byte [HexDigit + eax]
	mov byte [DumpLine + ecx + 2], al
; Done
	pop ecx
	pop ebx
	ret

;....................................................................................
;Procedure Name : Display
;IN : none
;OUT : none
;REG USE : all used registers are saved and restored
;DESCRIPTION : the hex and text lines are displayed using the write system call 
;		(int 80h)
;....................................................................................

Display :
	push eax
	push ebx
	push ecx
	push edx

	mov eax, 4
	mov ebx, 1
	mov ecx, DumpLine
	mov edx, FullLen
	int 80h
	
	pop edx
	pop ecx
	pop ebx
	pop eax
	
	ret


;.....................................................................................
;Procedure Name : FillBuf
;IN : None
;OUT : Number of bytes read in EAX
;REG USE : eax is used to return value. Everything else is saved and restored
;DESCRIPTION : the buffer is filled with data using the read system call
;.....................................................................................

FillBuf :
	push ebx
	push ecx
	push edx

	mov eax, 3
	mov ebx, 0
	mov ecx, Buffer
	mov edx, BufLen
	int 80h

	pop edx
	pop ecx
	pop ebx

	ret

;Main

global _start

_start :
	nop

Read :	
	call FillBuf
	mov esi, eax ; save count for later use
	cmp esi, 0
	je Exit
	
	xor edx, edx ; initialize counter to zero

;Traverse the buffer and fill the Hex and Text columns accordingly
Scan :
	xor eax, eax
	mov al, byte [Buffer + edx] ; get a byte from the buffer		
	call WriteChar
	inc edx

;check if we have run out of characters in the buffer
	cmp edx, esi
	jb Scan ; if not then scan the next character in the buffer

;if we have run through the entire buffer, print it and fetch again
	call Display
	call ClearLine
	jmp Read

;clean up and exit
Exit :
	mov eax, 1
	mov ebx, 0
	int 80h

	
	








	
		
	







	
	









































