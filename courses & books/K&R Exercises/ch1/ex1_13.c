#include<stdio.h>

#define IN 0
#define OUT 1
#define MSIZE 10

main() {

	int c,max,height,state = OUT,length = 0;
	int array[MSIZE];

	for (c = 0; c < MSIZE; c ++)
		array[c] = 0;

	while((c = getchar()) != EOF)
 
		if (c == ' ' || c == '\n' || c == '\t') {
			if (state == IN) {
				array[length] ++;
				length = 0;
			}
			state = OUT;
		}

		else {
			if (state == OUT)  
				state = IN;
			length++;
		}
	
	max = array[0];

	for (c = 1; c < MSIZE; c ++)
		if (array[c]  > max)
			max = array[c];
	

	printf("\n");

	for (height = 0; height < max; height ++) {
		printf("  %d  ",max-height);
		for(c = 0; c < MSIZE; c++)
			if(array[c] >= (max - height))
				printf("  #  ");
			else
				printf("  .  ");
		printf(" %d \n",max-height);
	}
	
	printf("\n");
	

}	
				
			


	


	
