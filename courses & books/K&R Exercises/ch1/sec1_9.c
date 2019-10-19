#include<stdio.h>

#define MAXLEN 1000  

int mygetline(char s[], int max);
void copy(char to[], char from[]);

main()
{
	int len,max = 0;
	char line[MAXLEN];
	char longest[MAXLEN];

	while ((len = mygetline(line,MAXLEN)) > 0) 
		if (len > max) {
			max = len;
			copy(longest,line);
		}

	if (max > 0)
		printf("\nlongest line : \"%s\" \t length : %d\n",longest,max);
	return 0;
}

int mygetline(char s[], int max)
{
	int c,i;
	
	for (i = 0; (i < max-1) && ((c = getchar()) != EOF) && (c != '\n'); i++)
		s[i] = c;

	if (c == '\n') {
		s[i] = c;
		i ++;
	} 
		
	s[i] = '\0';
	
	return i;
}

void copy(char to[], char from[])
{
	int i = 0;
	while((to[i] = from[i]) != '\0')
		i++;
}
	
	
