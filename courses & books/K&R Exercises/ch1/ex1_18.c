#include<stdio.h>

#define MSIZE 100

int mygetline(char s[],int max);
 
main()
{
	char line[MSIZE]; 
	int len = 0,i;

	while ((len = mygetline(line,MSIZE)) != 0) 
		
		if (line[0] == '\t' || line[0] == '\n')
			line[0] = '\0';
		else {
			for (i = len-1; (line[i] == '\n') || (line[i] == '\t'); i --);
			line[i + 1] = '\0';
			printf("LINE : \"%s\"\n",line); 	
		}
				
	

		
	return 0;
}			

int mygetline(char s[], int max)
{
	int i,c;
	
	for (i = 0; (i < max - 1) && ((c = getchar()) != EOF) && (c != '\n'); i++)
		s[i] = c;
		
	if (c == '\n') {
		s[i] = '\n';
		i ++;
	}
	s[i] = '\0';

	return i;
} 










	














