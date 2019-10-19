#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <signal.h>

#define SHMKEY 0x1234
#define SEMKEY 0x2345

typedef struct shm_data {
	pthread_mutex_t m;
	int val;
}Data;

int shmid, semid;
Data* ptr;

void sigint_handler (int signum)
{
	pthread_mutex_destroy (&ptr->m);
	
	shmdt ((void*) ptr);
	shmctl (shmid, IPC_RMID, NULL);
	printf ("shared memory deleted\n");

	semctl (semid, 0, IPC_RMID);
	printf ("semaphore deleted\n");

	
	printf ("Consumer exiting\n");
	_exit(10);
}

int main()
{
	struct sigaction sa;
	struct sembuf sb;
	int ret;

	// register signalhandler for SIGINT with the OS
	sa.sa_handler = sigint_handler;
	sigaction (SIGINT, &sa, NULL);

	// shared memory creation and stuff
 	if ((shmid = shmget (SHMKEY, sizeof(Data), 0)) < 0)
		_exit(1);
	
	if ((ptr = (Data*) shmat (shmid, NULL, 0)) < 0)
		_exit(1);
	
	// semaphore creation and all its stuff
	if ((semid = semget (SEMKEY, 2, 0)) < 0)
		_exit(1);
	getchar();
	printf ("hi\n");
	while (1) {
		printf ("Print : ");


		
		// decrement read semaphore
		sb.sem_num = 1;
		sb.sem_op = -1;
		sb.sem_flg = SEM_UNDO;
		semop (semid, &sb, 1);

		// lock mutex
		if (pthread_mutex_lock(&ptr->m) != 0)
			_exit(20);
		
		printf ("%d\n",ptr->val);

		// unlock mutex
		if (pthread_mutex_unlock(&ptr->m) != 0)
			_exit(0);

		// increment write semaphore
		sb.sem_num = 0;
		sb.sem_op = +1;
		sb.sem_flg = SEM_UNDO;
		ret = semop (semid, &sb, 1);
	
		if (ret < 0)
			kill (getpid(), SIGINT);
	


		sleep(1);

}		
	return 0;
}
