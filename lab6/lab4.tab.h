
/* A Bison parser, made by GNU Bison 2.4.1.  */

/* Skeleton interface for Bison's Yacc-like parsers in C
   
      Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.
   
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.
   
   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */


/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     DIGIT = 258,
     CONST = 259,
     ID = 260,
     NZD = 261,
     INCLUDE = 262,
     USING = 263,
     NAMESPACE = 264,
     STD = 265,
     IOSTREAM = 266,
     FSTREAM = 267,
     INT = 268,
     MAIN = 269,
     VOID = 270,
     DOUBLE = 271,
     STRUCT = 272,
     LPR = 273,
     RPR = 274,
     LBR = 275,
     RBR = 276,
     SEMICOLON = 277,
     DOT = 278,
     CIN = 279,
     COUT = 280,
     IF = 281,
     WHILE = 282,
     RS = 283,
     LS = 284,
     ELSE = 285,
     DIFF = 286,
     ASSIGN = 287,
     GTE = 288,
     LTE = 289,
     GT = 290,
     LT = 291,
     DIV = 292,
     MUL = 293,
     MINUS = 294,
     PLUS = 295
   };
#endif



#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
{

/* Line 1676 of yacc.c  */
#line 38 "lab4.y"

	char* char_val;



/* Line 1676 of yacc.c  */
#line 98 "lab4.tab.h"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif

extern YYSTYPE yylval;


