#ifndef FILET_HNDLR
#define FILET_HNDLR

#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <sys/shm.h>
#include <sys/msg.h>
#include <unistd.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/sem.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>


#define MSGKEY 0x2345
#define SHMKEY 0x1234
#define SEMKEY 0x3456
#define SERVER 30


union semun {
               int val;    
               struct semid_ds *buf;    
               unsigned short  *array;  
               struct seminfo  *__buf;  
};


typedef struct msgbuf {
	long type;
	char filepath[512];
}msgbuf_t;

typedef struct shm_data {
	int spid;
	char pipe_name [512];
}Data;

#endif /*FILET_HNDLR*/
