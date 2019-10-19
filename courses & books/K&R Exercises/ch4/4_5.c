/* 
+ Title : Command-line Calculator (Exercise 4.5, 4.6, 4.9 of KnR) 
+ Author : Rohit Mohan
+ Date : 15/2/16

+ Usage : 
	- This program takes a postfix expression from the terminal console and performs computations.
	- floating point numbers are supported.
	- Operations supported are : 
		- +, -, *, /, %
		- sin, exp, pow
	- You have to enter '=' to view the result.
	- Variable support is present for 26 variables named 'a' to 'z'.	
	- '$' sign followed by the variable name (the alphabet to be precise), should be used to load the variable.
	- Note that '$a' followed by '=', loads the value of variable 'a' and '=' pops it out again. Use 'print' to view.

	- Examples : 
		# 1 2 + = 			=> 3 is displayed
		# 1	2 + a           => 3 is stored in variable a
		# $a 3 +=			=> value in variable a and 3 are added and the result is displayed
		# 1 sin= 			=> displays sin(1)
		# 2 3 pow=			=> displays 2^3
		# 10 exp=			=> displays exp(10)
		# print				=> prints the top-most value in the stack. This is the answer of prev computation if you didnt use '=' to display.
		# $a print			=> prints the value of variable 'a'

		(Read the source if there is any doubt ;) 
 
+ Comments : 
	- To compile :  
		gcc -o 4_5 4_5.c -lm

*/

#include <stdio.h>
#include <string.h> /*for strncmp()*/
#include <ctype.h>  /*for isdigit(), isalpha()*/
#include <stdlib.h> /*for atof()*/
#include <math.h> /*for math functions*/


/*
	Set DEBUG to 1 and then compile and use the code, to see detailed information on how it works.
*/

#define DEBUG 0

#define STACKSIZE 50
#define STRINGSIZE 20

// Return values from getop()
#define NUMBER '0'
#define SINE '1'
#define EXP '2'
#define POW '3'
#define PRINT '4'
#define SWAP '5'
#define CLEAR '6'
#define UNKNOWN '7'
#define CALLVAR '8'

// Stack for storing numbers
double stack[STACKSIZE];
int pos = 0;

// Memory for storing variable values
double variable[26];

// get next computation element from STDIN
int getop(char *s);

// Stack operations
void push(double operand);
double pop(void);
double peek(void);

int main(void)
{
	int ret, i;
	double op2, num1, num2;
	char s[STRINGSIZE];

/* 
Main loop that constantly checks for new computation from the STDIN until EOF occurs
Note that the EOF terminates the program only on the beginning of a new line. So if you are in between a command, you have to press the EOF (usually ctrl-D) twice to exit.
*/
	while((ret = getop(s)) != EOF) {

#if DEBUG
		printf("main : ret = %d\n", ret);
#endif

		switch(ret) {

		
		case NUMBER :
			push(atof(s));
			break;
	
		case SINE :
			push(sin(pop()));
			break;

		case EXP :
			push(exp(pop()));
			break;

		case POW :
			op2 = pop();
			push(pow(pop(), op2));
			break;

		case '+':
			push(pop() + pop());
			break;

		case '*':
			push(pop() * pop());
			break;

		case '-':
			op2 = pop();
			push(pop() - op2);
			break;

		case '/':
			op2 = pop();
			push(pop() / op2);
			break;

		case '%':
			op2 = pop();
			push((int) pop() % (int)op2);
			break;

		case '=':
			printf("Answer : %g\n", pop());
			break;

// Print top-most number on the stack

		case PRINT :
			printf("Top element : %g\n", peek());
			break;

// Swap out the top two numbers on the stack for new values
		case SWAP : 
			printf("What elements to swap top two elements with [in order of push]? (<num1> [space] <num2>]): ");
			scanf("%lf %lf", &num1, &num2);
			pop();
			pop();
			push(num1);
			push(num2);
			break;
			
// Clear the contents of the stack and start anew
		case CLEAR : 
			pos = 0;
			printf("Cleared Stack!!\n");
			break;

// Fetch the numerical value assossiated with the variable from the variable memory
		case CALLVAR : 
			push(variable[s[0] - 'a']);
			break;

		case '\n' : 
			break;


		default : 

// Check if the returned value is a reference to a variable
			if (ret >= 'a' && ret <= 'z') {
// Save the topmost value of the stack in the variable
				variable[ret - 'a'] = pop();
				printf("main : value => %g  saved to variable => %c\n", variable[ret - 'a'], ret);
			}

// If not a variable then print an unknown value error
			else							
				printf("Unknown command %s\n", s);

			break;
		}	
	}

	return 0;
}

/******************* Stack oeration definitions ***************************/
void push(double num) 
{
	if (pos >= STACKSIZE)
		printf("push : Stack full\n");

	else {
		stack[pos++] = num;

#if DEBUG
		printf("push : %g\n", num);
#endif
	}
}

double pop(void)
{
	if (pos > 0){

#if DEBUG
		printf("pop : %g\n", stack[pos - 1]);	
#endif

		return stack[--pos];
	}

	else
		printf("pop : Stack empty\n");

	return 0.0;
}

double peek(void)
{
	if (pos <= 0){
		printf("peek : Stack empty\n");
		return -1;
	}	
	return stack[pos - 1];
}



int getch(void);
void ungetch(int c);

/* 
The function that parses the input for computational elements. There are broadly two categories : 

1) Numbers : both integers and floating point numbers
	- This is saved into a string (which is passed to the function as argument) and NUMBER flag is returned.
 
2) Characters
	- Operators
		- '+', '-', '*', '/', '=' : these are returned as such.
		- 'sin', 'exp', 'pow' : these are parsed from the input. When found, SINE, EXP, POW flags are returned resply.
		- '$' : this is used to access the values in the variable memory. So the next character is read, and put into a string (which is passed to the function as argument) and CALLVAR flag is returned.

	- Variables
		- They are alphabets ranging from 'a' - 'z' (No capital letters). If detected, they are returned as such.

	- Commands
		- A corresponding flag is returned.
*/

int getop(char *s)
{
	int i = 0, c, ctemp, command_count;
	char command[20];

// take care of all the whitespaces
	while ((s[0] = c = getch()) == ' ' || c == '\t');
	s[1] = '\0';

// if EOF, then return as such
	if (c == EOF)
		return c;

// if c is not a number
	if (!isdigit(c) && c != '.') {

// check if it is a variable call
		if (c == '$'){
			ctemp = getch();
			if (ctemp >= 'a' && ctemp <= 'z'){
				s[0] = ctemp;
				s[1] = '\0';
				return CALLVAR;
			}
			else
				return UNKNOWN;
		}
		
// check if it is either a variable assignment, command or an multi-character operator
		else if (isalpha(c)) {
			command_count = 0;
			command[command_count] = c;

// read all characters until the next non-character, into a command string
			while(isalpha(ctemp = getch())) {
				command[++command_count] = ctemp;
			}
			ungetch(ctemp);
			command[++command_count] = '\0';

#if DEBUG
			printf("getop : command = %s size = %d\n", command, strlen(command));
#endif

// Compare the command string with the available commands and operations 
			if (!strncmp(command, "sin", command_count))
				return SINE;
			
			else if (!strncmp(command, "exp", command_count))
				return EXP;

			else if (!strncmp(command, "pow", command_count))
				return POW;
			
			else if (!strncmp(command, "print", command_count))
				return PRINT;

			else if (!strncmp(command, "clear", command_count))
				return CLEAR;

			else if (!strncmp(command, "swap", command_count))
				return SWAP;

// if it is a one-character string consisting of an alphabet between 'a' and 'z' then it is taken to be a variable
			else if (strlen(command) == 1 && command[0] >= 'a' && command[0] <= 'z'){
		
				return command[0];
			}

// if it is none of the above return UNKNOWN
			else 
				return UNKNOWN;	
		}


// check if the '-' is for subtraction or for indicating a negative number 
		else if (c == '-'){

			if(isdigit(ctemp = getch())) {
				s[++i] = c = ctemp;
			}

			else {
				ungetch(ctemp);
				return c;						
			}			
		}

		else		
			return c; 
	}

// collect the digits
	if (isdigit(c))
		while (isdigit(s[++i] = c = getch()));

// collect the fraction digits
	if(c == '.')
		while (isdigit(s[++i] = c = getch()));

	s[i] = '\0';

	ungetch(c);

	return NUMBER;
}

// The intermediate buffer and functions which allow us to "push back" already read values, if we are not using them. 

#define BUFSIZE 50
char buf[BUFSIZE];
int bufp = 0;


int getch(void)
{
	int c = (bufp > 0) ? buf[--bufp] : getchar();;

#if DEBUG
	printf("getch : ascii value of c => %d\n", c);
#endif
	return c;
}

void ungetch(int c)
{
#if DEBUG
	printf("ungetch : %d\n", c);
#endif
	(bufp < BUFSIZE) ? (buf[bufp++] = c) : printf("ungetch : too many characters\n");
}












