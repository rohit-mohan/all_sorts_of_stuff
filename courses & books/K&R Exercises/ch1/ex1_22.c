#include <stdio.h>

#define N 10
#define MSIZE 100
main()
{
	int i,len = 0,pos = 0;
	char word[MSIZE];

	while ((len = getword(word,MSIZE)) > 0) {
			if ((len + pos) > N) { 
				if(len <= N) {
					if (word[0] != '\n') {
						printf("\n&%s",word);
						pos = len ;
						
					}
					else {
						putchar('\n');
						pos = 0;
					}
				}
				else if (len > N) {
					if (pos != 0){
						printf("\n");
						pos = 0;
					}
					for (i = 0; i < len; i++) 
						if (((i % N) == 0) && (i != 0)) {
							printf("...\n%c",word[i]);
							pos = 0;
						}
						else {
							printf("%c",word[i]);
							if (word[i] == '\n')
								pos = 0;
							else
								pos ++;
						} 
				}				
			
			}
			else 
				if (word[0] != '\n'){
					pos += len;				
					printf("%s",word);
				}
				else {
					putchar('\n');
					pos = 0;
				}
			
	}	
	return 0;
}


int getword(char s[], int max) 
{
	int c,i;
	for(i = 0; (i < max - 1) && ((c = getchar()) != EOF) && (c != ' ') && (c != '\n'); i++) 
			s[i] = c;

	if (c == ' ' || c == '\n'){
		s[i] = c;
		i ++;
	}

	s[i] = '\0';

	return i;
}
		
	










