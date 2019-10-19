#include <stdio.h>

void expand(char *t, char *s)
{
	int i = 0, j = 0;
	char upper, lower, c;

	if (t[i] == '-'){
		s[j] = '-';
		i = j = 1;
	}

	for	( ; t[i] != '\0'; i++) {

		if (t[i] == '-' && t[i+1] != '\0'){
			upper = t[i + 1];
			lower = t[i - 1];
		
			for(c = lower + 1; c < upper; c++)
				s[j++] = c;

		}

		else
			s[j++] = t[i]; 
	}
	
	s[j] = '\0';
	return;	
}


int main(void)
{
	char t[] = "-a-z0-9a-d-";
	char s[100];

	printf("Pre-processed : %s\n", t);
	expand(t, s);
	printf("Post-processed : %s\n", s);

	return 0;
}
