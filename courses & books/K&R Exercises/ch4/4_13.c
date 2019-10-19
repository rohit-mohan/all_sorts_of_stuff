#include <stdio.h>
#include <string.h>

void recreverse(char *s)
{
	static int i = 0, j = strlen(s) - 1;

	if (i < j) {
		char temp;
		temp = s[i];
		s[i] = s[j];
		s[j] = temp;
		i++, j--;
		recreverse(s); 
	}

	return;
}

int main(void)
{
	char s[] = "Hello, World!";

	printf("%s\n", s);
	recreverse(s);
	printf("%s\n", s);

	return 0;
}
