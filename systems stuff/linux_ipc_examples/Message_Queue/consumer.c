#include <stdio.h>
#include <unistd.h>
#include <sys/msg.h>
#include <signal.h>

struct msgbuf {
	long mtype;
	char mtext [1024];
};

struct msgbuf m;

int mqid;

void sigint_handler (int signum)
{
	msgctl (mqid, IPC_RMID, NULL);
	_exit(1);
}

#define MSGKEY 0x1234
#define CONS 0x3456
#define PROD 0x2345

int main()
{
	if ((mqid = msgget (MSGKEY, 0)) < 0) {
		printf ("msgget() failed\n");
		_exit(2);
	}

	while (1) {
		if (msgrcv(mqid, (void*) &m, sizeof(m.mtext), PROD, 0) < 0) {
			printf ("msgrcv() failed\n");
			_exit(3);
		}
		printf ("Consumer : %s\n", m.mtext);		
	}
	return 0;
}
