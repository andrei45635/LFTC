%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int MAX_CAP = 999;
int currentLine = 0;
int codAtom = 0;

char** constTS;
char** idTS;
char** FIP;

void createTS(char* type){
	if(0 == strcmp(type, "ID")){
		idTS = (char**)malloc(MAX_CAP * sizeof(char*));
		for(int i = 0; i < MAX_CAP; i++){
			idTS[i] = (char*)malloc(100 * sizeof(char));
			idTS[i][0] = '\0';
		}
	} else if (0 == strcmp(type, "CONST")) {
		constTS = (char**)malloc(MAX_CAP * sizeof(char*));
		for(int i = 0; i < MAX_CAP; i++){
			constTS[i] = (char*)malloc(100 * sizeof(char));
			constTS[i][0] = '\0';
		}
	} else {
		printf("Unknown type\n");
	}
}

void printTS(char* type){
	if(0 == strcmp(type, "ID")){
		for(int i = 0; i < MAX_CAP; i++){
			if(strlen(idTS[i])){
				printf("%d\t|\t%s\n", i, idTS[i]);
			}
		}
	} else if(0 == strcmp(type, "CONST")) {
		for(int i = 0; i < MAX_CAP; i++){
			if(strlen(constTS[i])){
				printf("%d\t|\t%s\n", i, constTS[i]);
			}
		}
	} else {
		printf("Unknown type\n");
	}
}

int hash(int letter, int i){
	int hashed = letter % MAX_CAP + i * (1 + letter % MAX_CAP);
	return hashed % MAX_CAP;
}

int atoi(const char* atom){
	int result = 0;
	for(int i = 0; i < strlen(atom); i++){
		result += atom[i];
	}
	return result;
}

void addToFIP(char* atom, int cod, int codTabel){
	if(-1 == codTabel){
		printf("%d\t|\t-\t|\t%s\n", codTabel, atom);
	} else {
		printf("%d\t|\t%d\t|\t%s\n", codTabel, cod, atom);
	}
}

void addToTS(char* atom, char* type){
	if(0 == strcmp(type, "ID")) {
		int codAtomTS = atoi(atom);
		int currentChar = 0;
		int hashVal = hash(codAtomTS, currentChar);
		while(strlen(idTS[hashVal]) && strcmp(idTS[hashVal], atom)){
			currentChar++;
		}
		strcpy(idTS[hashVal], atom);
		addToFIP(atom, codAtomTS, hash(hashVal, currentChar));
	} else if(0 == strcmp(type, "CONST")) {
		int codAtomTS = atoi(atom);
		int currentChar = 0;
		int hashVal = hash(codAtomTS, currentChar);
		while(strlen(constTS[hashVal]) && strcmp(constTS[hashVal], atom)){
			currentChar++;
		}
		strcpy(constTS[hashVal], atom);
		addToFIP(atom, codAtomTS, hash(hashVal, currentChar));
	} else {
		printf("Unknown type\n");
	}
}

%}

%option noyywrap

DIGIT 		[0-9]
ID          [a-zA-Z][a-zA-Z0-9]*   
CONST   	0|[1-9][0-9]*
KEYWORD 	#include|<iostream>|using|namespace|std|int|main|cin|cout|double|if|while
OPERATOR	"+"|"-"|"*"|"="|">"|"<"|"!="
SEPARATOR 	","|"."|":"|";"|"{"|"}"|"("|")"

%%

{KEYWORD} {
	int codAtom = -1;
	if (strcmp("#include", yytext) == 0) codAtom = 2;
	if (strcmp("<iostream>", yytext) == 0) codAtom = 3;
	if (strcmp("using", yytext) == 0) codAtom = 4;
	if (strcmp("namespace", yytext) == 0) codAtom = 5;
	if (strcmp("std", yytext) == 0) codAtom = 6;
	if (strcmp("int", yytext) == 0) codAtom = 7;
	if (strcmp("main", yytext) == 0) codAtom = 8;
	if (strcmp("cin", yytext) == 0) codAtom = 9;
	if (strcmp("main", yytext) == 0) codAtom = 10;
	if (strcmp("cout", yytext) == 0) codAtom = 11;
	if (strcmp("double", yytext) == 0) codAtom = 12;
	if (strcmp("if", yytext) == 0) codAtom = 13;
	if (strcmp("while", yytext) == 0) codAtom = 14;
	addToFIP(yytext, codAtom, -1);
}

{ID} {
	if(yyleng > 250){
		printf("Error on line %d: String %s exceeds limit\n", currentLine, yytext);
		break;
	}
	addToTS(yytext, "ID");
}

{CONST}|{DIGIT}+"."{DIGIT}* {
	addToTS(yytext, "CONST");
}

{OPERATOR} {
	int codAtom = -1;
	if (strcmp("+", yytext) == 0) codAtom = 15;
	if (strcmp("-", yytext) == 0) codAtom = 16;
	if (strcmp("*", yytext) == 0) codAtom = 17;
	if (strcmp("=", yytext) == 0) codAtom = 18;
	if (strcmp(">", yytext) == 0) codAtom = 19;
	if (strcmp("<", yytext) == 0) codAtom = 20;
	if (strcmp("!=", yytext) == 0) codAtom = 21;
	addToFIP(yytext, codAtom, -1);
}

{SEPARATOR} {
	int codAtom = -1;
	if (strcmp(",", yytext) == 0) codAtom = 22;
	if (strcmp(".", yytext) == 0) codAtom = 23;
	if (strcmp(":", yytext) == 0) codAtom = 24;
	if (strcmp(";", yytext) == 0) codAtom = 25;
	if (strcmp("{", yytext) == 0) codAtom = 26;
	if (strcmp("}", yytext) == 0) codAtom = 27;
	if (strcmp("(", yytext) == 0) codAtom = 28;
	if (strcmp(")", yytext) == 0) codAtom = 29;
	addToFIP(yytext, codAtom, -1);
}

[\n] {
	currentLine++;
}

[ \t\n]+ ;

. {
	printf("Error on line %d. Unrecognized character: %s\n", currentLine, yytext);
}

%% 
int main(argc, argv) 
int argc; 
char **argv; 
{ 
	++argv, --argc;
	if (argc > 0) {
		yyin = fopen(argv[0], "r"); 
	} else {
		yyin = stdin;
	}

	createTS("ID");
	createTS("CONST");
	
	printf("FIP:\n");
	yylex();
	
	printf("\n");
	
	printf("ID symbol table: \n");
	printTS("ID");
	
	printf("\n");
	
	printf("CONST symbol table: \n");
	printTS("CONST");
}
