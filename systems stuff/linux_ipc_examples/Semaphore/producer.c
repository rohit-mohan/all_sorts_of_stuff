#include <stdio.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <signal.h>
#include <unistd.h>
#include <signal.h>

#define SHMKEY 0x1234
#define SEMKEY 0x2345

int shmid, semid;

typedef struct shm_data {
	int val;
}Data;

Data* ptr;

union semun {
	int val;
	struct semid_ds* buf;
	unsigned short* array;
	struct seminfo* __buf;
};

void sigchld_handler (int signum)
{
	semctl (semid, 0, IPC_RMID);
	shmdt ((void *) ptr);
	shmctl (shmid, IPC_RMID, NULL);

	_exit(1);
}

int main()
{
	struct sigaction sa;
	union semun su;
	struct sembuf sb[2]; 
	unsigned short arr[3] = {1,1,0}; 

	sa.sa_handler = sigchld_handler;
	sigaction (SIGINT, &sa, NULL);

	shmid = shmget (SHMKEY, sizeof(Data), IPC_CREAT | 0666);
	ptr = (Data*) shmat (shmid, NULL, 0);
	
	semid = semget (SEMKEY, 3, IPC_CREAT | 0666);
	su.array = arr;
	semctl (semid, 0, SETALL, su);

	while(1) {
	
		sb[0].sem_num = 0;
		sb[0].sem_op = -1;
		sb[0].sem_flg = 0;

		sb[1].sem_num = 1;
		sb[1].sem_op = -1;
		sb[1].sem_flg = 0;

		semop (semid, sb, 2);

		ptr->val = rand() % 100;
		printf ("Data : %d\n",ptr->val);
//		scanf("%d",&ptr->val);
		

		sb[0].sem_num = 2;
		sb[0].sem_op = +1;
		sb[0].sem_flg = 0;
	
		sb[1].sem_num = 0;
		sb[1].sem_op = +1;
		sb[1].sem_flg = 0;
		
		semop (semid, sb, 2);

		usleep(100000);
	}
	
	return 0;
}
