#include<stdio.h>

main() {
	int array [26];
	int c;
	int max,height;
	for (c = 0; c < 26; c++) 
		array[c] = 0;

	while ((c = getchar()) != EOF) 
		if(c >= 'a' && c <= 'z') 
			array[c-'a'] ++;

// Horizontal Histogram
	printf("\n\nHorizontal Histogram\n\n");

 	for (c = 0; c < 26; c ++) {
		printf("%c  %d\t",'a'+c,array[c]);
		for (height = 0; height < array[c]; height ++)
			printf(" * ");
		printf("\n");
	}	

// Vertical Histogram
	max = array [0];
	printf("\n\nVertical Histogram\n\n");
	for (c = 1; c < 26; c ++) 
		if ( array[c] > max)
			max = array[c];
	printf(" # ");
	for (c = 0; c < 26; c ++)
		printf(" %c ",'a'+c);
	printf(" # ");
 
	printf("\n");
	for (height = 0; height < max; height++) {

		printf(" %d ",max - height);
		for (c = 0; c < 26; c ++)
			if (array[c] >= (max - height))
				printf(" @ ");
			else
				printf(" . ");
		
		printf(" %d ",max - height);
		putchar('\n');
	}
	
	printf(" # ");
	for (c = 0; c < 26; c ++)
		printf(" %c ",'a'+c); 
	printf(" # ");
	printf("\n");	
 
}
	
