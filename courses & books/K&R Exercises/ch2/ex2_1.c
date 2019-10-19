#include<stdio.h>

main()
{
	int i;
	int countb = 0;
	long countr = 1;
	short s;
	long l;
	char c;
	unsigned int ui;
	unsigned short us;
	unsigned long ul;
	unsigned char uc;
	
	for (c = 1 ; c > 0;  c = c * 2)
			countb ++;
	for (; countb > 0; countb --)
		countr = countr * 2;
		
	printf("%ld\n",countr);

	return 0;
}
	
