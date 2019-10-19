#include<stdio.h>

int bitcounter(int x);

main()
{
	int x = 0XAE;
	int count = 0;

	count = bitcounter(x);

	printf("%d\n",count);
	return 0;
}

int bitcounter(int x)
{
	int count = !(!x);
	printf("%d\n",count);
	while ((x &= x - 1) != 0) 
		count ++; 
	return count;
}
