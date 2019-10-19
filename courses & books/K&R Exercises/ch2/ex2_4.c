#include<stdio.h>

void mysqueeze(char s[], char t[]);
main()
{
	char l1[] = "HELLO WORLD. IT IS GREAT TO BE HERE";
	char l2[] = "EL";

	mysqueeze(l1,l2);
	printf("%s\n",l1);
	return 0;
}

void mysqueeze(char s[], char t[])
{
	int i,j,k;
	for (i = 0; t[i] != '\0'; i ++) {
		for (j = k = 0; s[j] != '\0'; j ++)
			if (s[j] != t[i])
				s[k ++] = s[j];
		s[k] = '\0';
	}

	
}
