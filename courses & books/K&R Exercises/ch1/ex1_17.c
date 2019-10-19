#include<stdio.h>

#define MSIZE 1000
#define THRESHOLD 10

int getlinelen(char s[]);
main() 
{
	char line[MSIZE];
	int len = 0;
	
	while((len = getlinelen(line)) > 0) 
		if(len > THRESHOLD)
			printf("Line : \"%s\"\n",line);
		else
			printf("\n");
	
	return 0;
}


int getlinelen(char s[]) 
{
	int i,c;
	for(i = 0; ((c = getchar()) != EOF) && (c != '\n'); i++)
		s[i] = c;

	s[i] = '\0';	
	
	if (c == '\n')
		i ++;
	
	return i - 1;
}	 
		
