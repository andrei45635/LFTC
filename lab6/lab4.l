%{
	#include <math.h>
	#include <string.h>
	#include "lab4.tab.h"
	#define YY_DECL int yylex()
	int line = 1;
%}

%option noyywrap

ID 	  [a-zA-Z][1-9]*
DIGIT [1-9]*
NZD   [1-9]*
CONST [-]?[0-9]+("."[0-9]+)?

%%	
"#include"   			{ return INCLUDE; }
"cin" 		 			{ yylval.char_val = strdup(yytext); return CIN; }
"cout" 		 			{ yylval.char_val = strdup(yytext); return COUT; }
"main()" 	 			{ return MAIN; }
"namespace"  			{ return NAMESPACE; }
"std" 		 			{ return STD; }
"int" 		 			{ return INT; }
"void" 		 			{ return VOID; }
"double" 	 			{ return DOUBLE; }
"<iostream>" 			{ return IOSTREAM; }
"<fstream>"  			{ return IOSTREAM; }
"using" 	 			{ return USING; }
"if" 		 			{ return IF; }
"else" 	 	 			{ return ELSE; }
"while" 	 			{ return WHILE; }
"struct" 	 			{ return STRUCT; }
	
{ID}{1,250}  			{ yylval.char_val = strdup(yytext); return ID; }
{DIGIT} 	 			{ yylval.char_val = strdup(yytext); return DIGIT; }
{CONST}  				{ yylval.char_val = strdup(yytext); return CONST; }
	
"{" 		 			{ return LBR; }
"}" 		 			{ return RBR; }
"(" 		 			{ return LPR; }
")" 		 			{ return RPR; }
">>" 		 			{ return RS; }
"<<" 		 			{ return LS; }
"<" 		 			{ return LT; }
">" 		 			{ return GT; }
">=" 		 			{ return GTE; }
"<=" 		 			{ return LTE; }
"+" 		 			{ yylval.char_val = strdup(yytext); return PLUS; }
"-" 		 			{ yylval.char_val = strdup(yytext); return MINUS; }
"*" 		 			{ yylval.char_val = strdup(yytext); return MUL; }
"/" 		 			{ return DIV; }
";" 		 			{ return SEMICOLON; }
"=" 		 			{ return ASSIGN; }
"!=" 		 			{ return DIFF; }
"." 		 			{ return DOT; }
	
[\n] 		 			{ line++; }
%%