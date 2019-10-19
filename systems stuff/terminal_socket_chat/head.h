#ifndef HEAD_H
#define HEAD_H

#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <string.h>
#include <signal.h>

#define SEMKEY 0x3456
#define SHMKEY 0x2345
#define PORT "2048"
#define SERVER "127.0.0.1"

typedef struct shm_data {
	int user_table[100];
	char broadcast[512];
}Data;

union semun {
	int val;
	struct semid_ds *buf;
	unsigned short *array;
	struct seminfo *__buf;	
};

typedef struct user_det {
	int fd;
	char name[10];
}User;
#endif /*HEAD_H*/
