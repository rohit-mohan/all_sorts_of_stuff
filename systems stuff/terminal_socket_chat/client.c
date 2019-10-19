#include "head.h"

int flag, sockfd;
char wrbuffer[1024];
char rdbuffer[1024];

void* writer(void* parameter);
void* reader(void* parameter);

int main(int argc, char* argv[]) 
{
	char hostname[30];
	char portnum[30];
	char name[30];
	char strbuffer[128];

	struct addrinfo hints, *res;
	struct sockaddr_in in;
	int ret, count;

	// Thread Creation Related Declaration
	pthread_t thread;
	pthread_attr_t tattr;
	
	if (argc < 4) {
		printf("Tell Us Who You Are. Usage : ./client [username]\n");
		return 1;
	}
	
	strcpy(hostname, argv[1]);
	strcpy(portnum, argv[2]);
	strcpy(name, argv[3]);

	printf("GROUP CHAT APPLICATION \n\n"); 	

/*******************************************SOCKET INIT AND CONNECTION************************************/

	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	
	printf("Probing server...");
	if ((ret = getaddrinfo(hostname, portnum, &hints, &res)) != 0) {
		fprintf(stderr, "getaddrinfo : %s\n", gai_strerror(ret));
		return ret; 
	} 
	printf("DONE\n");
	
	printf("Creating connection...");	
	if ((sockfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol)) < 0) {
		perror("socket()");
		return sockfd;
	}
	printf("DONE\n");

	printf("Connecting...");
	if ((ret = connect(sockfd, res->ai_addr, res->ai_addrlen)) < 0) {
		perror("connect()");
		return ret;
	}
	printf("DONE\n");


/****************************************************************************************************/
	
	sprintf(strbuffer, "%s has joined the chat\n", name);	
	write(sockfd, strbuffer, strlen(strbuffer)); 	
	
	count = read(sockfd, strbuffer, strlen(strbuffer));
	strbuffer[count] = '\0';
	printf("%s", strbuffer);
	printf("\n\n________________________________________________________________\n\n");

/***************************************THREAD ATTRIB AND CREATION******************************************************/

		ret = pthread_attr_init(&tattr);
		if (ret != 0) {
			perror("pthread_attr_init()");
			return ret;
		}

		ret = pthread_create(&thread, &tattr, writer, (void *)NULL);
		if (ret != 0) {
			perror("pthread_create()");
			return ret;
		}

			
		ret = pthread_create(&thread, &tattr, reader, (void *) NULL);
		if (ret != 0) {
			perror("pthread_create()");
			return ret;
		}
			

		
		
/***********************************************************************************************************************/
	flag = 0;

	while(flag == 0);
	
	close(sockfd);
	freeaddrinfo(res);

	return 0;
}

void* writer(void* parameter)
{

	while (1) {
		
		fgets(wrbuffer, sizeof(wrbuffer), stdin);
		write(sockfd, wrbuffer, strlen(wrbuffer));
		if(!(strncmp(wrbuffer, "exit", 4))) 
			break;
	}

	close(sockfd);
	printf ("Exiting chat!!\n");
	printf("\n________________________________________________________________\n");
	_exit(0);

}

void* reader(void* parameter)
{
	int count;
	int len;
	
	while (1) {
		count = 0;
		read(sockfd, rdbuffer, sizeof(rdbuffer));
		while(rdbuffer[count] != '\n')
			count ++;

		rdbuffer[count] = '\0';
	
		printf("%s\n", rdbuffer);
		
	}

}
