#include <stdio.h>
#include <string.h>

void reverse(char *s)
{
	int i, j;

	for(i = 0, j = strlen(s) - 1; i < j; i++, j--)
		s[i] ^= s[j] ^= s[i] ^= s[j];

	return;
}

int strindex(char *s, char *t)
{
	int len, i, j, k;	

	len = strlen(s);

	reverse(s);
	reverse(t);
	
	for (i = 0; s[i] != '\0'; i++) {
		for (j = 0, k = i; t[j] != '\0' && t[j] == s[k]; j++, k++);
	
		if (j > 0 && t[j] == '\0')
			return 	len - i - 1;
	}

	return -1;
}

int main(void)
{
	int pos;
	char s[] = "Hello World. This is a new beginning.";
	char t[] = "is";

	printf("siz of t : %d\n", strlen(t));
	if ((pos = strindex(s, t)) != -1)
		printf("(Right) Index found : %d\n", pos);
	else
		printf("Patttern not found\n");

	return 0;
}
