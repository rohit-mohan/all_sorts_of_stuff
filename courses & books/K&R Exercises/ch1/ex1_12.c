#include <stdio.h>

#define OUT 0
#define IN 1
main() {
	
	int c, state = 0;
	while((c = getchar()) != EOF) {
		if ( c == ' ') 
			state = OUT;
		else {
			if(state == OUT) {

				state = IN;
				putchar('\n');
			}

			putchar(c);
		}
	}
}
			
