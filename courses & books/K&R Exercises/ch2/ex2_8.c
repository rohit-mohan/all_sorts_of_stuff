#include<stdio.h>

int rightrot(int x, int n);

main()
{
	int x = 0XFF;
	int n = 3;
	x = rightrot(x,n);

	printf("%d\n",x);

	return 0;
}


int rightrot(int x, int n)
{
	return x >> n;
}
