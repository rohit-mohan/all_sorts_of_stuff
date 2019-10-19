#include <stdio.h>
#include <string.h>

void reverse(char *s)
{
	int i, j;

	for (i = 0, j = strlen(s) - 1; i < j; i++, j--)
		s[i] ^= s[j] ^= s[i] ^= s[j];		

	return;
}

int int2b(int n, int b, char *s)
{
	int i = 0, sign = 1;
	char lut[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";	
	
	if (b > 36)
		return 1;

	do 	
		s[i++] = lut[(n % b)];
	while ((n /= b) > 0);
	
	s[i] = '\0';

	reverse(s);

	return 0;
}


int main(void)
{
	int n = 15;
	int b = 2;
	char s[50];
	int ret;

	printf("Enter number [space] base: ");
	scanf("%d %d", &n, &b);	

	printf("Number : %d, Base : %d\n", n, b);		

	ret = int2b(n, b, s);	
	if (ret == 0)
		printf("Number string : %s\n", s);
	
	else
		printf("Error\n");	

	return 0;
}
