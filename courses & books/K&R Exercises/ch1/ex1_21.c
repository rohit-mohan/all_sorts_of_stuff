#include <stdio.h>

#define N 5
main()
{
	int c, i = 0, j = 0;

	for(i = 0; (c = getchar()) != EOF; i ++){
		if(c == ' ') {
			j = i;
			
			while ((c = getchar()) == ' ') {
				i++;
				if((i + 1) % N == 0) {
					j = i + 1;
					printf("\\t");
				}
			}
			
			for(; (j <= i); j++)
				putchar('*');
			i ++;
		}
	
		if (c == '\n'){
			putchar(c);
			i =  -1;
		}
		
		else
			putchar(c); 
	}
	return 0;			
}			
