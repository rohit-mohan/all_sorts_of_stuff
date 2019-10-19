/*
- Title : Recursive integer2char
- Author : Rohit Mohan
*/
#include <stdio.h>


void reci2a(char *s, int num)
{
	static int i = -1;
	static int count = 0;

	if (num < 0) {
		s[++i] = '-';
		num = -num;	
		count++;
	}


	if (num == 0){
		if (i == -1) 
			s[++i] = '0', count++;
		
//		printf("count : %d\n", count);
		s[count] = '\0';
	}


	else {
		count++;
		reci2a(s, num/10);
//		printf("%c\n", s[++i] = (num % 10) + '0');
	} 

	return;
}




int main(void)
{
	int num = 0;
	char s[10];

	printf("Number : %d\n", num);
	reci2a(s, num);
	printf("String : %s\n", s);

	return 0;
}
