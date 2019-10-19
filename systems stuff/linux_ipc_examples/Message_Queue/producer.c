#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <sys/msg.h>

struct msgbuf {
	long type;
	char mtext[1024];
};
 
struct msgbuf m; 

int mqid;

void sigint_handler (int signum)
{
	msgctl (mqid, IPC_RMID, NULL);
	printf("Producer exiting gracefully\n");
	_exit(1);
}

#define MSGKEY 0x1234
#define PROD 0x2345

int main()
{
	if ((mqid = msgget (MSGKEY, IPC_CREAT | 0666)) < 0) {
		printf ("msgget() failed \n");
		_exit(2);
	}
	m.type = PROD;

	while (1) {
		printf ("Producer : ");
		fgets (m.mtext, sizeof(m.mtext), stdin);
		if (msgsnd (mqid, (void*) &m, sizeof(m.mtext), 0) < 0) {
			printf ("msgsnd() failed\n");
			_exit(3);
		}
	}
	return 0;
}
