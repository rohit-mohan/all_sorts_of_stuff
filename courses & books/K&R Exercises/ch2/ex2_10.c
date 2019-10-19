#include<stdio.h>

main()
{
	int c;
	
	while((c = getchar ()) != EOF) 
		putchar( (c >= 'A' && c <= 'Z') ? c + 'a' - 'A' : c);
	return 0;
}
