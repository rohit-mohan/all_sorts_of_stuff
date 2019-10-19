#include <stdio.h>
#include <string.h>

void reverse(char *s)
{
	int i, j;	

	for (i = 0, j = strlen(s) - 1; i < j; i++, j--) 
		s[i] ^= s[j] ^= s[i] ^= s[j];

	return;
}


void int2char(int n, char *s)
{
	int i = 0, sign = 1;

	if (n < 0)
		sign = -1;	
	
	do {
		s[i++] = sign * ((n) % 10) + '0';
	} while((n /= 10) != 0);		

	if (sign < 0)
		s[i++] = '-';

	s[i] = '\0';

	reverse(s);

	return;
}




int main(void)
{
	int n = -2147483648;
	char s[50];		

	printf("Number : %d\n", n);
	int2char(n, s);
	printf("String number : %s\n", s);

	return 0;
}
