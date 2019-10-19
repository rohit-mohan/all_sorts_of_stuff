#include "filetransfer.h"

// IDs for IPC
int semid, shmid, msqid, status;
// Data structure for shared memory
Data* ptr;

void sig_handler (int signum) 
{
	printf ("\n.......................................................................\n");
	// close semaphore
	printf ("closing semaphore...");
	semctl (semid, 0, IPC_RMID);
	printf("DONE\n");
	// close shared memory
	printf ("closing shared memory...");
	shmdt ((void*) ptr);
	shmctl (shmid, IPC_RMID, NULL);
	printf("DONE\n");

	// close message queue
	printf ("closing message queue...");
	msgctl (msqid, IPC_RMID, NULL);
	printf("DONE\n");

	// deallocate all child processes
	printf ("closing any child processes...");	
	while (waitpid (-1, &status, WNOHANG) > 0);
	printf("DONE\n");
	printf (".......................................................................\n"); 
	_exit(0);
}


int main ()
{
	// signals declarations
	struct sigaction sa;
	sigset_t set;
	//  semaphore declarations
	unsigned short arr[3] = {0, 1, 1};
	union semun su;
	struct sembuf sb[2];
	// message queue declarations
	msgbuf_t msg;
	// process creation declarations
	int pid;
	// error check variable
	int ret;
	// pipe declarations
	int pipe_num;
	char pipe_name[30];
	char filepath [512];
	// file declarations
	char buffer[512];
	int fdwr, fdrd, count, tot_size;


	// register signal with O.S
	sa.sa_handler = sig_handler;
	sigaction(SIGINT, &sa, NULL);

	// create semaphore
	semid = semget (SEMKEY, 3, IPC_CREAT | 0666);
	if (semid < 0) {
		perror ("semget() failed");
		_exit(0);
	}

	// initialize semaphore
	su.array = arr;
	ret = semctl (semid, 0, SETALL, su);	
	if (ret < 0) {
		perror("semctl() failed");
		printf("%d\n",errno);
		_exit(0);
	}

	// create shared memory
	shmid = shmget (SEMKEY, sizeof (Data*), IPC_CREAT | 0666);

	// attach to shared memory
	ptr = (Data*) shmat (shmid, NULL, 0);
	
	// create message queue  
	msqid = msgget (MSGKEY, IPC_CREAT | 0666);		
	
	// initialize counter in shared memory
	ptr->spid = getpid();

	printf ("**Server Ready**\n"); 


	// infinite loop 
	while (1) {
		printf ("\nWaiting for new client...	");
		// wait for client request in message queue
		msgrcv (msqid, &msg, sizeof(msg.filepath), SERVER, 0);
		strcpy(filepath, msg.filepath);
		
		// lock read semapore and mx semaphore
		sb[1].sem_num = 2;
		sb[1].sem_op = -1;
		sb[1].sem_flg = 0;
		
		sb[0].sem_num = 0;
		sb[0].sem_op = -1;
		sb[0].sem_flg = 0;
		semop (semid, sb, 2);
		
		// copy pipe value to local variable
		strcpy(pipe_name, ptr->pipe_name);
		
		// unlock write semaphore and mx semaphore
		sb[1].sem_num = 2;
		sb[1].sem_op = +1;
		sb[1].sem_flg = 0;
		
		sb[0].sem_num = 1;
		sb[0].sem_op = +1;
		sb[0].sem_flg = 0;
		semop (semid, sb, 2);
		
		
				
		// fork into new process
		pid = fork();
		if (pid < 0){
			perror("fork() failed");
			continue;
		}
		// in child server process		
		if (pid == 0) {

			printf ("\nfile : %s			pipe name : %s \n", filepath, pipe_name);
			// open file to read from
			fdrd = open (filepath, O_RDONLY);
			if (fdrd < 0) {
				perror("open() for file failed");
				kill (pid, SIGINT);
			} 
			// open pipe to write to
			fdwr = open (pipe_name, O_WRONLY);
			if (fdrd < 0) {
				perror("open() for pipe failed");
				kill (pid, SIGINT);
			} 
			// file copy
			while ((count = read(fdrd, buffer, sizeof(buffer))) != 0) {
				write (fdwr, buffer, count);
				tot_size += count;
			}
			// close files
			close(fdrd);
			close(fdwr);

			printf ("\n## Download Completed [%d MB] . %s sent ##\n", tot_size/1000000, filepath);
			// exit process
			_exit(0);
		}

		else {
			// deallocate all process resources of zombie child processes
		//	while (waitpid(-1, &status, WNOHANG)  < 0);
		}
			
	}

	

	return 0;
}
