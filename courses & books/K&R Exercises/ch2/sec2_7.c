#include<stdio.h>

#define MSIZE 10

long myatoi(char s[]);

main()
{
	int i = 0;
	long num = 0;
	char c,line[MSIZE];
	while((c = getchar()) != '\n') {
		line[i] = c;
		i ++;
	}
	line[i] = '\0';

	num = myatoi(line);

	printf("%ld\n",num);
	
	return 0;
}

long myatoi(char s[])
{
	int i;
	long num = 0;
	
	for(i = 0; s[i] >= '0' && s[i] <= '9'; i ++)
		num = num * 10 + s[i] - '0' ;

	return num;
}

