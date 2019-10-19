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

union semun {
	int val;
	struct semid_ds* buf;
	unsigned short* array;
	struct seminfo_t* __buf;
};

void sigint_handler (int signum)
{
	pthread_mutex_destroy (&ptr->m);
	
	shmdt ((void*) ptr);
	shmctl (shmid, IPC_RMID, NULL);

	semctl (semid, 0, IPC_RMID);

	
	_exit(10);
}

int main()
{
	pthread_mutexattr_t ma;
	struct sigaction sa;
	struct sembuf sb;
	union semun su;
	int ret;
	unsigned short arr[2] = {1,0};

	// shared memory creation and stuff
	if ((shmid = shmget (SHMKEY, sizeof(Data), IPC_CREAT | 0666)) < 0){
		printf ("shmget() failed \n");
		_exit(10);
	}
	ptr = (Data*) shmat (shmid, NULL, 0);

	// mutex and mutex attribute initialization and mutex creation
	pthread_mutexattr_init (&ma);
	pthread_mutexattr_setpshared (&ma, PTHREAD_PROCESS_SHARED); 
	
	pthread_mutex_init (&ptr->m, &ma);

	// register signalhandler for SIGINT with the OS
	sa.sa_handler = sigint_handler;
	sigaction (SIGINT, &sa, NULL);

	// semaphore creation and all its stuff
	semid = semget (SEMKEY, 2, IPC_CREAT | 0666);
	su.array = arr;
	semctl (semid, 0, SETALL, su);

	while (1) {
		
		// decrement write semaphore
		sb.sem_num = 0;
		sb.sem_op = -1;
		sb.sem_flg = SEM_UNDO;
		semop (semid, &sb, 1);

		// lock mutex
		if (pthread_mutex_lock(&ptr->m) != 0)
			_exit(20);
		
		printf ("Data	:	%d\n",(ptr->val = rand() % 100));
		
		
		// unlock mutex
		if (pthread_mutex_unlock(&ptr->m) != 0)
			_exit(0);
		
		// increment read semaphore
		sb.sem_num = 1;
		sb.sem_op = +1;
		sb.sem_flg = SEM_UNDO;
		ret = semop (semid, &sb, 1);
		
		if (ret < 0)
			kill (getpid(), SIGINT);

		
		sleep(1);

}	
	return 0;
}
