#include<stdio.h>

#define MSIZE 100

int mygetline(char s[], int max);
long myhtoi(char s[]);

main()
{
	char line[MSIZE];
	int c,len;
		
	while((len = mygetline(line,MSIZE)) > 0)
		printf("%ld\n",myhtoi(line));

	return 0;
}

int mygetline(char s[], int max)
{
	int c,i;

	for (i = 0; i < max -1 && (c = getchar()) != EOF && c != '\n'; i++)
		s[i] = c;

	if (c == '\n'){
		s[i] = c;
		i ++;
	}

	s[i] = '\0';
	
	return i;
}

long myhtoi(char s[])
{
	long num = 0;
	int i;

	for (i = 0; (s[i] >= '0' && s[i] <= '9') || (s[i] >= 'A' && s[i] <= 'F') || (s[i] >= 'a' && s[i] <= 'f'); i++){
		if (s[i] >= '0' && s[i] <= '9')
			num = num * 16 + s[i] - '0'; 
		else if (s[i] >= 'A' && s[i] <= 'F')
			num = num * 16 + s[i] - 'A' + 10;
		else
			num = num * 16 + s[i] - 'a' + 10;
		//printf("%ld\n",num);
	}
//	printf("i : %d\n",i);
	return num;
}

