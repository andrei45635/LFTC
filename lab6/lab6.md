## Mini translator MLP

## How to compile:
1. flex lab4.l
2. bison -d lab4.y
3. gcc -g lex.yy.c lab4.tab.c -o lab4
4. ./lab4 mlp_example.txt
5. nasm -f win32 asm_code.asm -o asm_code.obj
6. gcc -m32 asm_code.obj -o asm_code.exe
