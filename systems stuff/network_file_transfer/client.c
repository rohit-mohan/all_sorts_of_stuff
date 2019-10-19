#include "filetransfer.h"

// ID for IPC
int semid, shmid, msqid;
// Data structure for shared memory
Data* ptr;
char pipe_name[30];

void sig_handler (int signum)
{
	printf ("......................................\n");
	printf ("disconnecting pipe...");
	unlink(pipe_name);
	printf("DONE\n");
	// disconnect semaphore 
	// disconnect shared memory
	printf ("disconnecting shared memory...");
	shmdt((void*) ptr);
	printf("DONE\n");
	// disconnect message queue
	printf (".....................................\n");
	_exit(10);

}

int main(int argc, char* argv [])
{
	// signals declarations
	struct sigaction sa;
	sigset_t set;
	//  semaphore declarations
	struct sembuf sb[2];
	// message queue declarations
	msgbuf_t msg;
	// process creation declarations
	int pid, status;
	// error check variable
	int ret;
	// pipe declarations
	int pipe_num;
	// file declarations
	char des [512], buffer[512];
	int len, fdrd, fdwr, count, tot_size;

	// register signal with O.S
	sa.sa_handler = sig_handler;
	sigaction(SIGINT, &sa, NULL);

	// connect with server semaphore
	semid = semget(SEMKEY, 3, 0);
	
	// connect with server shared memory
	shmid = shmget (SEMKEY, sizeof (Data*), 0);

	// attach to shared memory
	ptr = (Data*) shmat (shmid, NULL, 0);

	// attach with server message queue  
	msqid = msgget (MSGKEY, 0);

	//get pid
	pid = getpid();

	//compile message to send to server
	msg.type = (long) SERVER;
	strcpy(msg.filepath, argv[1]);
	
	// lock write semapore and mx semaphore
	sb[1].sem_num = 2;
	sb[1].sem_op = -1;
	sb[1].sem_flg = 0;
		
	sb[0].sem_num = 1;
	sb[0].sem_op = -1;
	sb[0].sem_flg = 0;
	ret = semop (semid, sb, 2);
			
	
	sprintf (pipe_name, "%d_%d.pipe",pid, ptr->spid);
	strcpy(ptr->pipe_name, pipe_name);
	mkfifo (pipe_name, 0666);
	msgsnd (msqid, &msg, sizeof(msg.filepath), 0);
		
	// unlock read semaphore and mx semaphore
	sb[1].sem_num = 2;
	sb[1].sem_op = +1;
	sb[1].sem_flg = 0;
		
	sb[0].sem_num = 0;
	sb[0].sem_op = +1;
	sb[0].sem_flg = 0;
	ret = semop (semid, sb, 2);

	printf ("file : %s 				in pipe : %s\n", argv[1], pipe_name);
	
	strcpy(des, argv[1]);
	len = strlen(des);
	len --;
	while (len) {
		if (des[len] == '/') {
			strcpy(des, des + len + 1);					
			break;		
		}
		len --;
	}
	

	//open pipe to read from
	fdrd = open (pipe_name, O_RDONLY);
	if (fdrd < 0) {
		perror("open() for pipe failed");
		kill (pid, SIGINT);
	} 

	// open file to write to
	fdwr = open (des, O_CREAT | O_WRONLY | O_TRUNC, 0666);		
	if (fdwr < 0) {
		perror ("open() for file failed");
		kill (pid, SIGINT);
	}

	// copy from pipe to file
	while ((count = read(fdrd, buffer, sizeof(buffer))) != 0) {
		write (fdwr, buffer, count);
		tot_size += count;
	}

	close(fdrd);
	close(fdwr);	

	printf ("\n**Download Completed [%d MB] . %s copied to %s **\n", tot_size/1000000, argv[1], des);  

	kill (pid, SIGINT);
	return 0;
}





