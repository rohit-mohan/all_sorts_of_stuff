#include <stdio.h>
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
	Data d,*ptr;

	if((shmid = shmget(KEY, sizeof(Data), IPC_CREAT | PERM)) < 0){
		printf ("CANNOT CREATE SHARED MEMORY\n");
		return 1;
	}

	if((ptr = (Data *) shmat(shmid, 0, 0)) < 0){
		printf("CANNOT ATTACH PROCESS\n");
		return 1;
	}

	d.data = 0;
	d.flag = 1;
	d.exit = 0;
	*ptr = d; 

	while(1){
		
		if (ptr->exit == 1){
			printf("Child has terminated connection\n");
			break;
		}	
		
		if (ptr->flag == 1) {
			
			printf("do you want to continue  [1/0] :  ");
			scanf("%d",&ptr->exit);
			
			if (ptr->exit == 1) {
				printf("Closing connection\n");
				break;
			}
			
			printf("Enter value (parent): ");
			scanf("%d",&ptr->data);
			ptr->flag = 0;
		
		} 	
	}

	shmdt((void *)ptr);
	shmctl(shmid, IPC_RMID, 0);

	return 0;
}
