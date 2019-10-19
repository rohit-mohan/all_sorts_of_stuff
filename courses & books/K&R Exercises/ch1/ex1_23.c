#include<stdio.h>

#define IN 1
#define OUT 0

main()
{
	char c;
	int sstate = OUT;   // string state
	int cmstate = OUT;  // comment multi line

	while((c = getchar()) != EOF) {
		if (c == '"') {
			putchar('"');
			if (sstate == IN)
				sstate = OUT;
			else
				sstate = IN;
		}
		else if (sstate != IN && c == '/') { 
			if ((c = getchar()) == '/') {
				while ((c = getchar()) != '\n');
				putchar(c);
			}

			else if (c == '*') 
				cmstate = IN; 
			else
				printf("/%c",c);
		}

		else if (sstate != IN && c == '*' && cmstate == IN) {
			if ((c = getchar()) == '/') 
				cmstate = OUT;
			else 
				printf("*%c",c);
		}

		else if (cmstate != IN) 
			putchar(c);
	}

	return 0;
}

		
	
		

		


	
	
		
