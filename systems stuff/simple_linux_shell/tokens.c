#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tokens.h"

int tokens(char str[], char** args)
{
	char* ptr;
	int count = 0;
	ptr = strtok(str, " \n");
	while (ptr != NULL) {
//		args[count] = (char*) malloc (sizeof(char) * 500);
		args[count] = ptr;
		ptr = strtok(NULL, " \n");
		count ++;
	}
	if (ptr == NULL)
		args[count] = NULL;

	return count;
}
