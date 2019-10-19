#include<stdio.h>

#define MSIZE 100

int mygetline(char s[], int max);

main()
{
	int len = 0;
	char line[MSIZE];
	
	while((len = mygetline(line,MSIZE)) > 0) 
		printf("%s\n",line);

	return 0;
}

int mygetline(char s[], int max) 
{
	int i,count = 0;
	char c;
	
	for (i = 0; count != 1; i ++) {
		if (i >= max - 1) {
			i --;
			count = 1;
		}
		else if ((c = getchar()) == EOF){
			i --;
			count = 1;
		}
		else if (c == '\n') {
			i --;
			count = 1;
		}
		else
			s[i] = c;
	}

	if (c == '\n') {
		s[i] = c;
		i ++;
	}
	
	s[i] = '\0';

	return i;
}  
