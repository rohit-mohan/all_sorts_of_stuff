#include<stdio.h>

#define MSIZE 100

int any(char s[],char t[]);

main()
{
	char l1[MSIZE] = "HELLO WORLD IS A GREAT PROGRAM";
	char l2[MSIZE] = "GA";
	int pos;

	pos = any(l1,l2);

	printf("%d\n",pos);

	return 0;
}

int any(char s[], char t[])
{
	int i,j,pos = -1;
	
	for (i = 0; t[i] != '\0'; i ++)
		for (j = 0; s[j] != '\0'; j++)
			if ((pos == -1 || j < pos) && s[j] == t[i])
				pos = j;

	return pos;
}
