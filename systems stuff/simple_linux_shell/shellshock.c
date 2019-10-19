#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "sigchld_handler.h"		// void sigchld_handler(int snum, siginfo_t* si, void* parameters)
#include "tokens.h" 			// int tokens(char str[], char** args)
#include "redirections.h"		// int redirections(char* str, char** argm)

#define NO_P 30
#define WSIZE 500
	
int main()
{
	pid_t pid;
	int status, i, count, async;
	char* argm[4];
	char* args[NO_P];
	char string[WSIZE];
	struct sigaction snew;
	struct sigaction sold;
	sigset_t set;

	// parameters for sigsuspend() function
	sigfillset(&set);
	sigdelset(&set, SIGCHLD);
	sigdelset(&set, SIGINT);


	// parameters for the sigaction() system call
	snew.sa_sigaction = sigchld_handler;
	snew.sa_flags = SA_SIGINFO;
	
	// registering the sigchld_handler() with the O.S (17 : SIGCHLD signal). 
	sigaction(17, &snew, &sold);
	
	while(1) {

		async = 0;
		string[0] = '\0';
		// prompt and user input
		printf("Enter Command : ");		
		fgets(string, sizeof(string), stdin);
		

		// spliting input string into command, input file and output file
		redirections(string, argm);

/*		
		// print the split tokens 
		for (i = 0; i < 3; i++)
			if (argm[i] != NULL)
				printf("%d : %s\n",i+1,argm[i]);
*/		
	
		// convert the command string into command-line argument format
		count = tokens(string, args);

/*
		// print command and arguments
		for (i = 0; args[i] != NULL; i++)
			printf("%s\n",args[i]);	
*/		
		// internal commands
		if (args[0] == NULL)
			continue;		
		
		if (!(strcmp(args[0], "exit")))
			break;

		if (!(strcmp(args[0], "cd"))) {
			if(chdir(args[1]) < 0)
				printf("Directory called %s does not exist\n"); 
			continue;	
		}	

		if (!(strcmp(args[count - 1], "&"))) {
			args[count - 1] = NULL;						
			async = 1;
		}
		
		// create child process and error check
		pid = fork();
		// in the child process load the command taken from the user
		if (pid == 0) {
			if(execvp(args[0], args)){
				// exit if execvp() fails
				printf("Command not found ...\n");
				_exit(100);
			}	
		}

		else {
			if (async == 0){
				sigsuspend(&set);
				printf ("synch kill of child : %d\n",pid);
				
			}	

		}
		
	
	} /* end of while loop */
	
	return 0;
}
