#include <stdio.h>
#include <string.h>

void reverse(char *s)
{
	int i, j;

	for (i = 0, j = strlen(s) - 1; i < j; i++, j--)
		s[i] ^= s[j] ^= s[i] ^= s[j];

	return;
}

void int2str(int n, int min, char *s)
{
	int i = 0,sign = 1, remaining, d;

	if (n < 0)
		sign  = -1;

	do {
		s[i++] = sign* (d = (n % 10)) + '0';
		printf("D : %d\n", d);
	}while ((n /= 10) != 0);

	if (sign < 0)
		s[i++] = '-';

	if ((remaining = min - i) > 0) 
		while (remaining--)
			s[i++] = ' ';
	
	s[i] = '\0';

	reverse(s);
	return;
}


int main(void)
{
	int n, min;
	char s[30];
	
	printf("Enter number [space] min_chars : ");
	scanf("%d %d", &n, &min);
	
	int2str(n, min, s);	
	
	printf("Number in string : %s\n", s);
	printf("number of characters : %d\n", strlen(s));
	
	return 0;
}
