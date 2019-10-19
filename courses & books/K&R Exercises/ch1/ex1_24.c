#include<stdio.h>

#define OUT 0
#define IN 1
#define INTER -1

main()
{
	char c;
	int i;

	int sstate = OUT;
	int cmstate = OUT;
	
	int cbstate = 0;
	int cbline;
	int bstate = 0;
	int bline;
	int pstate = 0;
	int pline;	
	
	for (i = 0; (c = getchar()) != EOF; i++) {
		if (c == '"') {
			if (sstate == OUT)
				sstate = IN;
			else
				sstate = OUT;
		}

		else if (sstate != IN && c == '/') {
			i ++;
			if ((c = getchar()) == '/'){
				for (; (c = getchar()) != '\n'; i ++);
				putchar(c);
			}
			else if(c == '*')
				cmstate = IN;
		}

		else if (sstate != IN && cmstate != IN && pstate != INTER && c == '(') {
			pstate ++;
			pline = i;
		}
		
		else if (sstate != IN && cmstate != IN && pstate != INTER && c == ')') {
			if (pstate)
				pstate --;
			else 
				pstate = INTER;
				
			pline = i;
		}

		else if (sstate != IN && cmstate != IN && cbstate != INTER && c == '{') {
			cbstate ++;
			cbline = i;
		}

		else if (sstate != IN && cmstate != IN && cbstate != INTER && c == '}') {
			if (cbstate)
				cbstate --;
			else
				cbstate = INTER;
			cbline = i;
		}

		else if (sstate != IN && cmstate != IN && bstate != INTER && c == '[') {
			bstate ++;
			bline = i;
		}

		else if (sstate != IN && cmstate != IN && bstate != INTER && c == ']') {
			if (bstate)
				bstate --;
			else
				bstate = INTER;
			bline = i;
		}

	}

	if (pstate != 0)
		printf("\nparanthesis ( mismatch at %d",pline);
	else 
		printf("\nNO paranthesis ( mismatch");

	if (cbstate != 0)
		printf("\nbraces { mismatch at %d",cbline);
	else
		printf("\nNO braces { mismatch");
	
	if (bstate != 0)
		printf("\nbrackets  [ mismatch at %d\n",bline);
	else
		printf("\nNO brackets [ mismatch\n");

	return 0;
}		
			
						
















