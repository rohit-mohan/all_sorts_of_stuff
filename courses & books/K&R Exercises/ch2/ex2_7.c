#include<stdio.h>

int invert(int x, int p, int n);

main()
{
	int x = 0XF;
	int p;
	int n = 4;

	p = 3;
	x = invert(x,p,n);

	p = 7;
	x = invert(x,p,n);

	printf("%X\n",x);
	
	return 0;
}

int invert(int x, int p, int n)
{
	return ~(~0 << n) << p - n + 1 ^ x;
}
