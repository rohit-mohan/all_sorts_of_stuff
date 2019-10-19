#include "sigchld_handler.h"

void sigchld_handler(int snum, siginfo_t* si, void* parameters) 
{
	int status;
	pid_t pid = waitpid(-1, &status, 0);
	printf ("Child (%d) dead with exit value %d\n", pid, status);
}
