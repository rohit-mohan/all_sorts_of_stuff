#include <stdio.h>
#include <unistd.h>
int main()
{
	int i = 0;
	while(i < 11) {
		printf("count number : %d\n",i);
		i ++;
		sleep(1);
	}	
	return 0;
}
