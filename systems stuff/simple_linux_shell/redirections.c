/***************************************************************************************
Name : redirections.c
Version : 1.0
Date : 25/11/14
Parameters : string (STR), pointer to strings (ARGM)
Return value : 0 if redirection was not used in command, 1 if redirection was used.
Description : Given the input command as STR and the pointer to strings to store the 
tokens, the function stores the command as the first token, the file to read inputs 
from as the second token and file to write the outputs in as the third token.
**************************************************************************************/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int redirections(char* str, char** argm)
{
	int i;
	int flag = 0;
	argm[0] = str;
	argm[1] = NULL;
	argm[2] = NULL;
	argm[3] = NULL;

	for (i = 0; str[i]!= '\0'; i++) {
		
		if (str[i] == '<') {
			str[i] = '\0';
			argm[1] = str+i+1;
			flag = 1;
		}

		else if (str[i] == '>'){
			str[i] = '\0';
			argm[2] = str+i+1;
			flag = 1;
		}

		else if (str[i] == '\n') {
			str[i] = '\0';
		}
	}



	return flag;
}
