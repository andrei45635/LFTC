%{
	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>
	#include <stdbool.h>
	#include <ctype.h>

	extern int yylex();
	extern int yyparse();
	extern FILE* yyin;
	extern int line;
	extern int yyerror()
	{
		printf("Error at line %d\n", line);
		exit(1);
	}
	
	void print_line_info() {
		printf("Line %d: ", line);
	}
	
	FILE* file;
	char* filename;
	
	char imports[100][100], decl[100][100], cod[100][100];
	int k1 = 0, k2 = 0, k3 = 0;
	
	char read_var[100][100];
	int n = 0, nr = 0;
	
	char expr[1000][1000];
	int m = 0;
	
	bool find(char col[][100], int n, char* var);
	void process_expr(char* ex);
%}

%union {
	char* char_val;
};

	%token DIGIT CONST ID NZD
	%token INCLUDE USING NAMESPACE STD IOSTREAM FSTREAM 
	%token INT MAIN VOID DOUBLE STRUCT
	%token LPR RPR LBR RBR SEMICOLON DOT
	%token CIN COUT 
	%token IF WHILE
	
	%left ELSE LS RS
	%left ASSIGN DIFF
	%left LT GT LTE GTE 
	%left PLUS MINUS MUL DIV
%%
	program 		: headers_block main_block
				    ;
				  
	headers_block   : headers_list USING NAMESPACE STD SEMICOLON
				    ;
					
	headers_list    : header headers_list
						| header
		
	header		    : INCLUDE library
					;
					
	library 		: IOSTREAM	
						| FSTREAM
					;
					
	main_block 		: type MAIN LBR instr_list RBR
					;
	
	type			: VOID 
						| INT
						| DOUBLE
						| triple
						| point
					;
	
	triple 			: NZD DOT DIGIT DIGIT DIGIT
					;
					
	point			: STRUCT LBR INT ID SEMICOLON INT ID SEMICOLON RBR ID SEMICOLON
					;
					
	instr_list		: instr instr_list
						| instr	
					;
					
	instr 			: atribuire { print_line_info(); printf("aici\n"); }
						| declarare { print_line_info(); printf("declarare\n"); }
						| read { print_line_info(); printf("read\n"); }
						| write { print_line_info(); printf("write\n"); }
						| if_instr { print_line_info(); printf("if\n"); }
						| while_instr { print_line_info(); printf("while\n"); }
					;
	
	atribuire 		: ID ASSIGN expr SEMICOLON 
						{ 
							char temp[100];
							strcpy(temp, $<char_val>3);
							char* token;
							token = strtok(temp, " ");
							while ( NULL != token ) {
								strcpy(expr[m++], token);
								token = strtok(NULL, " ");
							}
							process_expr($<char_val>1);
						}
					;
					
	declarare		: type ID SEMICOLON 
						{
							char temp[100];
							strcpy(temp, " ");
							strcat(temp, $<char_val>2);
							printf("$<char_val>2 %s\n", $<char_val>2);
							printf("temp %s\n", temp);
							if ( false == find(decl, k2, temp) ) {
								strcpy(decl[k2++], strcat(temp, " times 4 db 0"));
							}
						}
					;
	
	expr 			: ID 
						{
							char temp[100];
							strcpy(temp, " ");
							strcat(temp, $<char_val>1);
							printf("$<char_val>1 %s\n", $<char_val>1);
							printf("temp %s\n", temp);
							if ( false == find(decl, k2, temp) ) {
								strcpy(decl[k2++], strcat(temp, " times 4 db 0"));
							}
						}
						| DIGIT 
						| CONST
						| DIGIT operator expr 
							{ 
								char temp[100];
								strcpy(temp, $<char_val>1);
								strcat(temp, " ");
								strcat(temp, $<char_val>2);
								strcat(temp, " ");
								strcat(temp, $<char_val>3);
								$<char_val>$ = strdup(temp);
							}
						| CONST operator expr 
							{ 
								char temp[100];
								strcpy(temp, $<char_val>1);
								strcat(temp, " ");
								strcat(temp, $<char_val>2);
								strcat(temp, " ");
								strcat(temp, $<char_val>3);
								$<char_val>$ = strdup(temp); 
							}
						| ID operator expr 
							{ 
								char temp[100];
								strcpy(temp, $<char_val>1);
								strcat(temp, " ");
								strcat(temp, $<char_val>2);
								strcat(temp, " ");
								strcat(temp, $<char_val>3);
								$<char_val>$ = strdup(temp);
							}
					;
					
	operator 		: PLUS
						| MINUS
						| DIV
						| MUL
						| LT
						| GT
						| DIFF
						| LTE
						| GTE
						| ASSIGN
						| RS
						| LS
					;
					
	read  			: CIN RS ID SEMICOLON
						{
							printf("$<char_val>3 %s\n", $<char_val>3);
							if ( false == find(imports, k1, "scanf") ) {
								strcpy(imports[k1++], "scanf");
							}
							if ( false == find(decl, k2, "format") ) {
								strcpy(decl[k2++], " format db \"%d\", 0\n");
							}
							n = 0;
							
							strcpy(read_var[n], "push dword ");
							strcat(read_var[n], $<char_val>3);
							strcat(read_var[n], "\n\t\tpush dword format");
							strcat(read_var[n], "\n\t\tcall _scanf");
							strcat(read_var[n], "\n\t\tadd esp, 4 * 2\n");
							
							n++;
							
							for(int i = n - 1; i >= 0; i--) {
								strcpy(cod[k3++], read_var[i]);
							}
						}
					;
	
	write 			: COUT LS ID SEMICOLON 
						{
							if ( false == find(imports, k1, "printf") ) {
								strcpy(imports[k1++], "printf");
							}
							if ( false == find(decl, k2, "format") ) {
								strcpy(decl[k2++], " format db \"%d\", 0");
							}
							
							strcpy(cod[k3], "push dword [");
							strcat(cod[k3], $<char_val>3);
							strcat(cod[k3++], "]");
							strcpy(cod[k3++], "push dword format");
							strcpy(cod[k3++], "call _printf");
							strcpy(cod[k3++], "add esp, 4 * 2\n");
						}
					;
					
	if_instr 		: IF LPR expr RPR LBR atribuire RBR else_instr
						| IF LPR expr RPR LBR atribuire RBR
					;
					
	else_instr 		: ELSE LBR atribuire RBR
					;

	while_instr		: WHILE LPR expr RPR LBR instr RBR 
					;
					
%%

int main(int argc, char* argv[]){
	printf("Compile with:\nnasm -f win32 asm_code.asm -o asm_code.obj\ngcc -m32 asm_code.obj -o asm_code.exe\n");
	FILE* f = NULL;
	printf("here\n");
	if ( 1 < argc ) {
		f = fopen(argv[1], "r");
		filename = argv[1];
		int i = strlen(filename) - 1;
		while( "." != filename && 0 < i ) {
			i--;
		}
		filename[i] = '\0';
		strcat(filename, "asm_code.asm");
	} else {
		strcpy(filename, "output.asm");
	}
	
	if ( NULL == f) {
        perror("Couldn't open file\n");
        return 1;
    }
	
	yyin = f;
	
	strcpy(imports[k1++], "exit");
	
	while ( !feof(yyin) ) {
		yyparse();
	}
	
	printf("Result: OK\n");
	
	file = fopen(filename, "w+");
	
	//printing imports
	fprintf(file, "bits 32\n\n");
	for ( int i = 0; i < k1; i++ ) {
		//fprintf(file, "extern %s\nimport %s msvcrt.dll\n\n", imports[i], imports[i]);
		fprintf(file, "extern _%s\n", imports[i], imports[i]);
	}
	
	//printing declarations
	//fprintf(file, "segment data use32 class=data\n");
	fprintf(file, "section .data\n");
	for ( int i = 0; i < k2; i++ ) {
		fprintf(file, "\t%s\n", decl[i]);
	}
	
	//printing code
	//fprintf(file, "segment code use32 class=code\n\tstart:\n");
	fprintf(file, "section .text\nglobal _main:\n\t_main:\n");
	strcpy(cod[k3++], "push dword 0");
	strcpy(cod[k3++], "call _exit");
	for ( int i = 0; i < k3; i++ ) {
		fprintf(file, "\t\t%s\n", cod[i]);
	}
	
	printf("All OK\n"); 
	return 0;
}

bool find(char col[][100], int n, char* var) {
	char temp[100];
	strcpy(temp, var);
	strcat(temp, " ");
	for ( int i = 0; i < n; i++ ) {
		if ( NULL != strstr(col[i], temp) ) {
			return true;
		}
	}
	return false;
}

void process_expr(char* ex) {
	printf("expr[0] %s\n", expr[0]); 
	strcpy(cod[k3], "mov AL, [");
	strcat(cod[k3], expr[0]);
	strcat(cod[k3++], "]");
	
	for ( int i = 1; i < m - 1; i += 2 ) {
		if ( 0 == strcmp(expr[i], "*") ) {
		printf("expr[i] %s\n", expr[i]);
			if ( isdigit(expr[i + 1][0]) ) {
				strcpy(cod[k3], "mov DL, ");
				strcat(cod[k3++], expr[i + 1]);
				strcat(cod[k3++], "mul DL");
			} else {
				strcpy(cod[k3], "mul byte [ ");
				strcat(cod[k3], expr[i + 1]);
				strcat(cod[k3++], "]");
			}
		} else if ( 0 == strcmp(expr[i], "+") ) {
			if ( isdigit(expr[i + 1][0]) ) {
				strcpy(cod[k3], "add AL, ");
				strcat(cod[k3++], expr[i + 1]);
			} else {
				strcpy(cod[k3], "add AL, byte [ ");
				strcat(cod[k3], expr[i + 1]);
				strcat(cod[k3++], "]");
			}
		} else if ( 0 == strcmp(expr[i], "-") ) {
			if ( isdigit(expr[i + 1][0]) ) {
				strcpy(cod[k3], "sub AL, ");
				strcat(cod[k3++], expr[i + 1]);
			} else {
				strcpy(cod[k3++], "sub AL, byte [ ");
				strcat(cod[k3++], expr[i + 1]);
				strcat(cod[k3++], "]");
			}
		}
	}
	
	strcpy(cod[k3], "mov [");
	strcat(cod[k3], ex);
	strcat(cod[k3++], "], AL\n");
	m = 0;
}