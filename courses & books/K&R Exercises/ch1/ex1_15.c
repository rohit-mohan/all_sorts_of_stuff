#include<stdio.h>

#define UPPER 200
#define LOWER 0
#define STEP 20


float fahr2cel(int f);

main() 
{
	int fahr;
	printf("Fahr\t:\t    Cel\n");
	printf("----\t \t    ---\n");
	for (fahr = LOWER; fahr <= UPPER; fahr = fahr + STEP) 
		printf /*celsius = 5/9*(fahr-32)*/("%4d\t:\t%7.2f\n",fahr,fahr2cel(fahr));
	
	return 0;
}

float fahr2cel(int f)
{
	return ((5.0/9.0)*(f-32));
}
