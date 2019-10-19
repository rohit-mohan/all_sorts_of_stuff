#include<stdio.h>

#define MSIZE 100
#define N 10
main()
{
	int c;
	int i = 0,j = 0;

	for(i = 0; (c = getchar()) != EOF; i++){
		//printf("%d",i);
		if(c == '\t') {
			for(j = 0; j < (N - (i % N)); j++)
				putchar(' ');
			i = i + j;
		}
		else if (c == '\n') {
			putchar(c);
			i = -1;
		}
		else
			putchar(c);

		
 	} 
	return 0;
}	
