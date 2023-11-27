%{
	#include "lab4.tab.h"
	
	int line = 1;
%}

%option noyywrap

ID 	  [a-zA-Z][1-9]*
CHAR  [a-zA-Z]*
DIGIT [0-9]*
NZD   [1-9]*
CONST [-]?[0-9]+("."[0-9]+)?

%%	
"#include"   			{ return INCLUDE; }
"cin" 		 			{ return CIN; }
"cout" 		 			{ return COUT; }
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
	
{DIGIT} 	 			{ return DIGIT; }
{ID}{1,250}  			{ return ID; }
{CONST}  				{ return CONST; }
{CHAR} 					{ return CHAR; }
	
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
"+" 		 			{ return PLUS; }
"-" 		 			{ return MINUS; }
"*" 		 			{ return MUL; }
"/" 		 			{ return DIV; }
";" 		 			{ return SEMICOLON; }
"=" 		 			{ return ASSIGN; }
"!=" 		 			{ return DIFF; }
"." 		 			{ return DOT; }
	
[\n] 		 			{ line++; }
%%
