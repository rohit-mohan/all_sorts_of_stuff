#include <stdio.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#define KEY 0X000000FF
#define PERM 0666

typedef struct data_sm {
	int data;
	int flag;
	int exit;
}Data;

int main()
{
	int shmid;
	Data *ptr;

	if((shmid = shmget(KEY, sizeof(Data), 0)) < 0) {
		printf("CANNOT CREATE SHARED MEMORY\n");
		return 1;
	}

	if((ptr = (Data *) shmat(shmid, 0, 0)) < 0) {
		printf("CANNOT ATTACH PROCESS\n");
		return 1;
	}

	while(1) {
		
		if (ptr->exit == 1){
			printf("Parent has terminated connection\n");
			break;
		}
			
		if (ptr->flag == 0) {
			
			printf ("\nData	:	%d\n", ptr->data);
			printf ("Do you want to continue [1/0] : ");
			scanf("%d",&ptr->exit);
			
			if (ptr->exit == 1) {
				printf("Closing connection\n");
				break;
			}
			
			ptr->flag = 1;
		}	
	}

	shmdt((void*) ptr);
	shmctl(shmid, IPC_RMID, 0);
	
	return 0;
}
