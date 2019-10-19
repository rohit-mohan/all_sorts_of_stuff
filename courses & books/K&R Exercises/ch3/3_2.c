#include <stdio.h>

void escape(char *t, char *s)
{
	int i = 0, j=0;
	while(t[i] != '\0') {
		switch(t[i]){
			case '\n':
				s[j] = '\\';
				s[++j] = 'n';
				j++;
				break; 
			case '\t':
				s[j] = '\\';
				s[++j] = 't';
				j++;
				break;

			default:
				s[j] = t[i];
				j++;
				break;			
		}
		
		i++;
	}

	s[j] = '\0';
}

void descape(char *t, char *s)
{
	int i = 0, j = 0, flag = -1;

	while(t[i] != '\0') {

		switch(t[i]) {
			case '\\' : 
				flag = 1;
				break;
			case 'n' :
				if (flag) 
					s[j++] = '\n';
				else
					s[j++] = t[i];

				flag = 0;	
				break;
	
			case 't' :
				 if (flag) 
					s[j++] = '\t';
				else
					s[j++] = t[i];

				flag = 0;
				break;

			default : 
				s[j++] = t[i];
				flag = 0;
				break;
		}
		
		i++;
	}
}


int main(void)
{
	char t[100] = "hello world\nthe world is a\tbetter place than you think\n";
	char s[120], r[120];

	printf("before processing : %s || \n", t);
	escape(t,s);
	printf("after processing : %s || \n", s);
	descape(s,r);
	printf("after unprocessing : %s || \n",r);
	
	return 1;
}
