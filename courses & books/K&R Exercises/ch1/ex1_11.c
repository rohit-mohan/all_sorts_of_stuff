#include<stdio.h>

#define IN 1
#define OUT 0
main() {
	
	int nl,nw,nc;
	int c;
	int state = OUT;

	nl = nw = nc = 0;
	
	while((c = getchar()) != EOF) {
		
		nc ++;

		if (c == '\n') {
			nl ++;
			state = OUT;
		}
		else if (c == ' ' || c == '\t') 
			state = OUT;
		else {
			if (state == OUT) {
				state = IN;
				nw ++;
			}
		}
	}
	printf("characters : %d words : %d lines : %d",nc,nw,nl);
}
	
