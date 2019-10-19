#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main()
{
	int fdarr [2];
	pid_t pid;
	char buf [1024];
	int count, status;
	
	pipe (fdarr);
	
	printf ("Parent begins \n");
	
	if ((pid = fork()) < 0){
		printf ("fork() failed\n");
		_exit(0);
	}

	if (pid == 0) {
		close (fdarr[1]);
		while ((count = read (fdarr[0], buf, sizeof(buf))) > 0)
			printf ("%s", buf);
	
		printf ("\nbye\n");
		close(fdarr[0]);
	}

	else {
		close (fdarr[0]);
		printf ("Producer : ");
		fgets(buf, sizeof(buf), stdin);
		write (fdarr[1], buf, sizeof(buf));
		close (fdarr[1]);
		waitpid (-1, &status, 0);
		printf ("Parent ends\n");
	}
	
	return 0;
}
