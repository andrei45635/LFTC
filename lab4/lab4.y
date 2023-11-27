%{
	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>

	extern int yylex();
	extern int yyparse();
	extern FILE* yyin;
	extern int line;
	extern int yyerror(const char* msg)
	{
		printf("Error at line %d: %s\n", line, msg);
		exit(1);
	}
	
	void print_line_info() {
		printf("Line %d: ", line);
	}
%}
	%token DIGIT CONST ID CHAR NZD
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
	
	atribuire 		: ID ASSIGN expr SEMICOLON { print_line_info(); printf("aici2\n"); }
					;
					
	declarare		: type ID SEMICOLON
					;
	
	expr 			: ID 
						| DIGIT
						| CONST
						| DIGIT operator expr { print_line_info(); printf("aici3\n"); }
						| CONST operator expr { print_line_info(); printf("aici4\n"); }
						| ID operator expr { print_line_info(); printf("aici5\n"); }
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
					;
	
	write 			: COUT LS ID SEMICOLON
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
	++argv, --argc;
	
	if(argc > 0){
		yyin = fopen(argv[0], "r");
	} else {
		yyin = stdin;
	}

	while(!feof(yyin)){
		yyparse();
	}
	
	printf("Result: OK\n");
	return 0;
}
