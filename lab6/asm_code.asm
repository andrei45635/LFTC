bits 32

extern _exit
extern _scanf
extern _printf
section .data
	 a times 4 db 0
	 format db "%d", 0

section .text
global _main:
	_main:
		push dword a
		push dword format
		call _scanf
		add esp, 4 * 2

		mov AL, [a]
		sub AL, 2
		mov [a], AL

		push dword [a]
		push dword format
		call _printf
		add esp, 4 * 2

		push dword 0
		call _exit
