#include<stdio.h>

int setbits(int x, int p, int n, int y); 

main()
{
	int y = 0X2F;
	int x = 0XFE;
	int p = 6;
	int n = 3;

	printf("%X %X %X\n",y,x,setbits(x,p,n,y));

	return 0;
}

int setbits(int x, int p, int n, int y)
{

	return ~(~0 << n) << p - n + 1 & y | ~(~(~0 << 3) << p - n + 1) & x;

}
