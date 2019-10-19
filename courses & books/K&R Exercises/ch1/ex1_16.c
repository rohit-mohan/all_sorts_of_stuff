#include<stdio.h>

#define MSIZE 11

int mygetline(char s[], int max);

main()
{
	int len,max = 0;
	char line[MSIZE];
	
	while((len = mygetline(line,MSIZE)) > 0) {
		
		if((len == (MSIZE - 1)) && (line[len-1] != '\n'))
			while(getchar() != '\n')
				len ++;
		printf("STRING : \"%s\" \t",line);
		printf("LENGTH : %d\n",(len-1));
	}

	return 0;
} 


int mygetline(char s[], int max)
{
	int c,i;
	for(i = 0; (i < max - 1) && ( (c = getchar()) != EOF) && (c != '\n'); i++) 
		s[i] = c;

	if(c == '\n')
		i++;
	
	s[i] = '\0';

	return i;
}
