#include <stdio.h>
#include <ctype.h>
#include <stdlib.h> /*for atof()*/

#define STACKSIZE 50
#define STRINGSIZE 20

double stack[STACKSIZE];
int pos = 0;

int getop(char *s);
void push(double operand);
double pop(void);

int main(void)
{
	int ret, i;
	double op2;
	char s[STRINGSIZE];

	while((ret = getop(s)) != EOF) {
		switch(ret) {
		
		case '0' :
			push(atof(s));
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

		case '\n':
			printf("Answer : %g\n", pop());
			break;

		case 'p':
			printf("Stack : ");
			for (i = 0; i < pos; i++)
				printf("%g ", stack[i]);
			printf("\n");

		default : 
			printf("Unknown command %s\n", s);
			break;
		}	
	}

	return 0;
}

void push(double num) 
{
	if (pos >= STACKSIZE)
		printf("push : Stack full\n");

	else {
		stack[pos++] = num;
//		printf("push : %g\n", num);
	}
}

double pop(void)
{
	if (pos > 0){
//		printf("pop : %g\n", stack[pos - 1]);	
		return stack[--pos];
	}

	else
		printf("pop : Stack empty\n");

	return 0.0;
}


int getch(void);
void ungetch(int c);


int getop(char *s)
{
	int i = 0, c, ctemp;

	while ((s[0] = c = getch()) == ' ' || c == '\t');
	s[1] = '\0';

/*
	if (isalpha(c)) 
		while(isalpha(s[++i] = c = getch()));



*/

    /* c is not a number */
	if (!isdigit(c) && c != '.') {

		if (c == '-'){

			if(isdigit(ctemp = getch())) {
				s[++i] = c = ctemp;
//				printf("getop : %c\n", ctemp);
			}

			else {
				ungetch(ctemp);
				return c;						
			}			
		}

		else		
			return c; 
	}

	/* collect the digits */
	if (isdigit(c))
		while (isdigit(s[++i] = c = getch()));

	/* collect the fraction digits */
	if(c == '.')
		while (isdigit(s[++i] = c = getch()));

	s[i] = '\0';

	if (c != EOF)
		ungetch(c);

	return '0';
}

#define BUFSIZE 50
char buf[BUFSIZE];
int bufp = 0;


int getch(void)
{
	return (bufp > 0) ? buf[--bufp] : getchar();
}

void ungetch(int c)
{
	(bufp < BUFSIZE) ? (buf[bufp++] = c) : printf("ungetch : too many characters\n");
}












