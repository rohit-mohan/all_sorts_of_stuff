#include<stdio.h>

main() {
	
	int countblank = 0;
	char c;
	while((c = getchar()) != EOF) {
		if(c == ' ') {
			while((c = getchar()) == ' ');
			putchar(' ');
			putchar(c);
		}
		else
			putchar(c);
	}
		
					
}
