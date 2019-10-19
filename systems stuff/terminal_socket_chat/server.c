#include "head.h"


int shmid, semid, sockfd;
struct Broadcast {
	int ofd;
	char msg[1024];
};

struct Broadcast broadcast;
int user_table[10];

// signal handler for SIGINT
void sigint_handler(int signum)
{
	// closing everything gracefully
	printf("\nclosing all connections...");
	close(sockfd);
	printf("DONE\n");

	_exit(0);
}


void* reader(void* parameter);
void* writer(void* parameter);

int main(int argc, char* argv[])
{

/**********************************DECLARATION*******************************************************/

	// Socket and R/W Related Declarations
	struct addrinfo hints, *res;
	struct sockaddr_in in;
	struct sigaction sa;
	char ip4[INET_ADDRSTRLEN];
	int newfd;
	long nf_long;	
	int count, i;
	int yes = 1;
	socklen_t in_size;

	// Thread Creation Related Declaration
	pthread_t thread;
	pthread_attr_t tattr;
	

	// Semaphore related Declaration
	union semun su;
	struct sembuf sb[2];
	unsigned short arr[3] = {0, 1, 1};	
	
	// Error Checking
	int ret; 		

	// Registering Sig Handler for SIGINT to the O.S
	sa.sa_handler = sigint_handler;
	sigaction(SIGINT, &sa, NULL);

	// initialize user table and print
	memset(user_table, 0, sizeof(user_table));

	for (i = 0; i < 10; i++)
			printf ("%d ", user_table[i]);
		printf("\n");
		
/****************************************SEMAPHORE INIT***********************************************/


	// creating a semaphore with 3 counters : 0 - read, 1 - write, 2 - mutual exclusion
	semid = semget(SEMKEY, 3, IPC_CREAT | 0666);	
	// initialize the semaphore counters
	su.array = arr;
	semctl(semid, 0, SETALL, su);
	
	

/***********************************SOCKET INIT AND FUNCTION*******************************************/ 
	

	memset (&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = AI_PASSIVE;
	
	printf ("resolving...\n");	
	if ((ret = getaddrinfo(NULL, PORT, &hints, &res) ) != 0) {
		fprintf(stderr, "getaddrinfo() : %s\n", gai_strerror(ret));
		return ret;
	}

	printf("creating connection...\n");	
	if ((sockfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol)) < 0) {
		perror("socket()");
		return sockfd;
	}

	if ((ret = setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int))) < 0) {
		perror("sockopt()");
		return ret;
	}
	

	printf("connecting...\n");
	if ((ret = bind(sockfd, res->ai_addr, res->ai_addrlen)) < 0) {
		perror("bind()");
		return ret;
	}

	

	printf("**Server Ready**\n"); 

	freeaddrinfo(res);

/****************************************THREAD ATTRIB AND WRITER THREAD CREATION********************************************************/

	ret = pthread_attr_init(&tattr);
	if (ret != 0) {
		perror("pthread_attr_init()");
		return ret;
	}

	ret = pthread_create(&thread, &tattr, writer, (void *) NULL);
	if (ret != 0) {
		perror("pthread_create()");
		return ret;
	}
	
		// infinite listening loop
	while(1) {
			
		
	
		// printf("waiting for client...\n");
		if ((ret = listen(sockfd, 5)) < 0) {
			perror("listen()");
			return ret;
		}

		in_size = sizeof(in);	
		// printf("accepting client request...\n");
		if ((newfd = accept(sockfd, (struct sockaddr *) &in, &in_size)) < 0){
			perror("accept()");
			return newfd;
		}

		

		//	printf ("New Socket FD : %d\n", newfd);

/***************************************READER THREAD CREATION******************************************************/
		nf_long = (long) newfd;

		

		ret = pthread_create(&thread, &tattr, reader, (void *) nf_long);
		if (ret != 0) {
			perror("pthread_create()");
			return ret;
		}

/***********************************************************************************************************************/	

		
	}
	
	

	return 0;
}

/********************************************READER THREAD**************************************************************/

void* reader(void* parameter) 
{
	struct sembuf sb[2];
	int count, i, len;
	long fd_long = (long) parameter; 
	int fd = (int) fd_long;
	char *ptr;
	char temp[1024];
	char gbuffer[1024];
	User u;
	u.fd = fd;

	user_table[fd] = 1;

	for (i = 0; i < 10; i++)
			printf ("%d ", user_table[i]);
		printf("\n");

	read (fd, gbuffer, sizeof(gbuffer));
		
		sb[0].sem_num = 0;
		sb[0].sem_op = -1;
		sb[0].sem_flg = SEM_UNDO;
		sb[1].sem_num = 2;
		sb[1].sem_op = -1;
		sb[1].sem_flg = SEM_UNDO;
		semop(semid, sb, 2);	
		
		len = strlen(gbuffer);
		broadcast.ofd = u.fd;
		strcpy(broadcast.msg, gbuffer);
		broadcast.msg[len] = '\0'; 

		sb[0].sem_num = 2;
		sb[0].sem_op = +1;
		sb[0].sem_flg = SEM_UNDO;
		sb[1].sem_num = 1;
		sb[1].sem_op = +1;
		sb[1].sem_flg = SEM_UNDO;
		semop(semid, sb, 2);
	printf ("%s", gbuffer);
	strncpy (u.name, gbuffer, sizeof(u.name));
	
	ptr = strtok(u.name, " ");
	strcpy(u.name, ptr);
				
	sprintf(gbuffer, "Hello %s\n", u.name);
	write(fd, gbuffer, strlen(gbuffer));

	while (1) {
		
		count = read(fd, gbuffer, sizeof(gbuffer));
		
		len = strlen(gbuffer);
		
		if (count <= 0) 
			break;

		gbuffer[count] = '\0';
		printf("%-10s [%d] :\t%s",u.name, u.fd, gbuffer);
	//	sprintf(temp,"%-10s  :\t%s",u.name, gbuffer);

		if (!(strncmp(gbuffer, "exit", 4))) {
		
			user_table[fd] = 0;
			sb[0].sem_num = 0;
			sb[0].sem_op = -1;
			sb[0].sem_flg = SEM_UNDO;
			sb[1].sem_num = 2;
			sb[1].sem_op = -1;
			sb[1].sem_flg = SEM_UNDO;
			semop(semid, sb, 2);	
		
			broadcast.ofd = u.fd;
			sprintf(broadcast.msg,"**%s has left the chat**\n", u.name); 
			
	
			sb[0].sem_num = 2;
			sb[0].sem_op = +1;
			sb[0].sem_flg = SEM_UNDO;
			sb[1].sem_num = 1;
			sb[1].sem_op = +1;
			sb[1].sem_flg = SEM_UNDO;
			semop(semid, sb, 2);


			user_table[fd] = 0;		
			for (i = 0; i < 10; i++)
				printf ("%d ", user_table[i]);
			printf("\n");
			printf ("%s left chat!\n", u.name);
			close(fd);			
			break;
		
		}
	
		sb[0].sem_num = 0;
		sb[0].sem_op = -1;
		sb[0].sem_flg = SEM_UNDO;
		sb[1].sem_num = 2;
		sb[1].sem_op = -1;
		sb[1].sem_flg = SEM_UNDO;
		semop(semid, sb, 2);	
		
		broadcast.ofd = u.fd;
		sprintf(broadcast.msg,"%-10s:\t%s\0", u.name, gbuffer);
		 

		sb[0].sem_num = 2;
		sb[0].sem_op = +1;
		sb[0].sem_flg = SEM_UNDO;
		sb[1].sem_num = 1;
		sb[1].sem_op = +1;
		sb[1].sem_flg = SEM_UNDO;
		semop(semid, sb, 2);

	}

	
}

/*******************************************************WRITER THREAD***************************************/

void* writer(void* parameter)
{
	struct sembuf sb[2];	
	char fdstr [3];
	int rfd, i, len;
	
	while(1) {
		sb[0].sem_num = 1;
		sb[0].sem_op = -1;
		sb[0].sem_flg = SEM_UNDO;
		sb[1].sem_num = 2;
		sb[1].sem_op = -1;
		sb[1].sem_flg = SEM_UNDO;
		semop(semid, sb, 2);	
		
		len = strlen(broadcast.msg);
		for (i = 3; i < 10; i++)
			if (user_table[i] != 0 && broadcast.ofd != i)	{
		//		broadcast.msg [len] = '\0';
		//		printf("in server : %s\n", broadcast.msg);		
				write(i, broadcast.msg, strlen(broadcast.msg));
			}	

		sb[0].sem_num = 2;
		sb[0].sem_op = +1;
		sb[0].sem_flg = SEM_UNDO;
		sb[1].sem_num = 0;
		sb[1].sem_op = +1;
		sb[1].sem_flg = SEM_UNDO;
		semop(semid, sb, 2);	
	}
		
}
