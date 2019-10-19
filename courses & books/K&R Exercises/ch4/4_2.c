#include <stdio.h>
#include <ctype.h>

double atof(char *s)
{
	double val, power;
	int i, sign = 1, expsign = 1, exp = 0;

	for (i = 0; isspace(s[i]); i++);
	
	if(s[i] == '-')
		sign = -1, i++;

	for (val = 0.0; isdigit(s[i]); i++)
		val = 10.0 * val + s[i] - '0';

	if (s[i] == '.')
		i++;

	for (power = 1.0; isdigit(s[i]); i++, power *= 10.0)
		val = 10.0 * val + s[i] - '0';

	val = sign * val / power;
	sign = 1;

	if (s[i] == 'e' || s[i] == 'E')
		i++;

	if (s[i] == '-')
		sign = -1, i++;		

	for (exp = 0; isdigit(s[i]); i++)
		exp = 10 * exp + s[i] - '0';

	for (power = 1.0; exp > 0; exp--, power *= 10);

	if (sign > 0)
		val *= power;
	else
		val /= power;

	return val;
	
}

int main(void)
{
	char s[] = "123.45e-6";
	double num;

	printf("Number in string: %s\n", s);
	num = atof(s);
	printf("Number : %f\n", num);

	return 0;
}
