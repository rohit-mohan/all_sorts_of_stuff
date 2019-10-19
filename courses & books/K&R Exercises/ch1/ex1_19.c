#include<stdio.h>

#define MSIZE 100
int mygetline(char s[], int max);

main()
{
	char c,line[MSIZE];
	int i,len = 0;
	

	while((len = mygetline(line,MSIZE)) > 0) {
			
		printf("LINE : \"%s\" %d\n",line,len);
		for(i = 0; i <= (len-1)/2; i ++){
			c = line[i];
			line[i] = line[len - i - 2];
			line[len - i - 2] = c; 
		}
		
		printf("REVERSED LINE : \"%s\" \n",line);
	}
	return 0;
}



int mygetline(char s[], int max)
{
	int i,c;
	for (i = 0; (i < max-1) && ((c = getchar()) != EOF) && (c != '\n'); i++)
		s[i] = c;

	if(c == '\n') {
		s[i] = '.';
		i ++;
	}

	s[i] = '\0';

	return i;
}
