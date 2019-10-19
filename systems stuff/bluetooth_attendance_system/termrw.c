/*********************************************Header Section***************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <time.h>
#include <pthread.h>
#include <bcm2835.h>

//constants used for denoising the input from serial device
#define YES 1
#define NO 0

//PIN 11 used in the toggle_gpio() thread
#define PIN  RPI_BPLUS_GPIO_J8_11

/***********************************************Global Declarations*************************************************************/


//flag to exit loop in main
int flag = 1;

//the file i/o and serial device i/o file descriptors
int fd, fd_db, fd_nl, fd_final;

//signal handler for SIGINT[Ctrl-C] (way to terminate the program) 
void sigint_handler(int sig);

//used to toggle the output on PIN 11 on the Raspberry Pi GPIO
void *toggle_gpio(void *param);

//get system time and convert it into a string
void get_time_string(char *time);

//process the incoming Bluetooth address, filter out the noisy and unwanted part and save it in an output file in a required format 
void input_processing(int fd, char *input, int size);

//matching the Bluetooth addresses to the registered names
int database_match();

/*********************************************Main***************************************************************/


//get the  port to connect to as command-line argument
int main(int argc, char **argv)
{

/*********************************************Local Declarations***************************************************************/

	
	//terminal control and configuration structures
	struct termios told, tnew;
	//read buffer for reading from serial deivce
	char rbuffer[512];
	//pthread structure 
	pthread_t t; 
	
	//return value checking variable
	int res;
	//signal handling structure
	struct sigaction sa;

/*******************************************Configurations*****************************************************************/

	if (argc < 2) {
		printf("No arguments!\n");
		return 1;
	}

	//registering the signal handler for SIGINT
	memset(&sa, 0, sizeof(sa));
	sa.sa_handler = sigint_handler;
	if(sigaction(SIGINT, &sa, NULL) < 0) 
		perror("sigaction");


	//open the file and serial device file
	fd_final = open("final.db", O_CREAT | O_WRONLY, 0666);
	fd_nl = open("name_list.db", O_RDONLY);
	fd_db = open("database.db", O_CREAT | O_RDWR | O_TRUNC, 0666);
	fd = open(argv[1], O_RDWR);
	

	//get current terminal settings
	tcgetattr(fd, &told);


	memset(&tnew, 0, sizeof(struct termios));
	//back-up curent settings
	tnew = told;
	

	//set baud-rate for communcation with the serial device
	cfsetospeed(&tnew, B38400);
	cfsetispeed(&tnew, B38400);


	//apply the terminal settings
	tcsetattr(fd, TCSAFLUSH, &tnew);

/********************************************Thread Creation****************************************************************/	

	if(pthread_create(&t, NULL, toggle_gpio, NULL)) {
		perror("pthread_create");
		return 1;
	}

/***********************************************Data Processing*************************************************************/	

	//continuously read the serial device and save the output into the output file.
	//process the file into required format.
	while(flag == 1) {

		read(fd, rbuffer, sizeof(rbuffer));
//		printf("%s", rbuffer); 
		input_processing(fd_db, rbuffer, sizeof(rbuffer));
	} //exits only when sigint _handler is called due to occurance of SIGINT signal	
	
/***********************************************Clean Up*************************************************************/


	//cancel the toggle_gpio thread
	if(pthread_cancel(t)) 
		perror("pthread_cancel");

	if(pthread_join(t, (void *)&res))
		perror("pthread_join");
	
	if(res != PTHREAD_CANCELED)
		printf("Thread not cancelled\n");  	


	//make sure the GPIO 11 pin is LOW
	bcm2835_gpio_write(PIN, LOW);
	

	//restore old terminal settings
	tcsetattr(fd, TCSAFLUSH, &told);

	//close files
	close(fd);
	close(fd_db);


/**********************************************Termination**************************************************************/	


	return 0;
}

/************************************************************************************************************/


//signal handler for SIGINT signal
void sigint_handler(int sig)
{
	flag = 0;	
}


/************************************************************************************************************/


//toggle the GPIO 11 to inquire nearby Bluetooth devices periodically 
void *toggle_gpio(void *param)
{
	int ret= 1;

	if (!bcm2835_init())
		return 1;

	bcm2835_gpio_fsel(PIN, BCM2835_GPIO_FSEL_OUTP);

	while(1) {
		bcm2835_gpio_write(PIN, HIGH);
		delay(60000);
		bcm2835_gpio_write(PIN, LOW);
		
		ret = database_match();
		if (ret == 0) 
			printf("Database updated\n");

		delay(60000);

		pthread_testcancel();
	}
	
	return NULL;
}


/************************************************************************************************************/


//denoising and formatting the input recieved from serial deivce
void input_processing(int fd,  char *input, int size)
{	
     	char c;
	int i = 0;
	char time[60], fetch[50];
	static int wr_flag = NO;
	
	
	while (i < size) {

		//read input character by character
		c = input[i];

		//filter out unwanted and noisy input
		if (c == 'Q'){
			wr_flag = YES;
			i++;
			continue;
		}


		//formatting the useful input
		if ((c == ',' || c == '\n') && wr_flag == YES) {

/*
			get_time_string(fetch);
			sprintf(time, "\t%s\n", fetch);
			write(fd, time, strlen(time));
*/
			c = '\n';
			write(fd, &c, 1);
			wr_flag = NO;
		}

		if (wr_flag == YES){
			write(fd, &c, 1);
		}
		i++;
	}

	return;
}


/************************************************************************************************************/


//get system time and convert it into string (time_str is an output parameter)
void get_time_string(char *time_str)
{
	time_t t;
	char *str;
	
	//get system time
	t = time(NULL);
	//convert to string
	str = ctime(&t);
	//copy to output parameter
	strcpy(time_str, str);

	return;
}

/************************************************************************************************************/

//match names registered in the name_list.db to the Bluetooth device addresses in database.db and compile a final list 
int database_match()
{
	int i, eof_nl = 1, eof_db = 1; 	
	char c, name[50], address[50], database[50], time[30], wbuffer[110];

	fd_db = open("database.db", O_RDONLY);
	if (fd_db <= 0)
		return 100;
	fd_nl = open("name_list.db", O_RDONLY);
	if (fd_nl <= 0)
		return 101;
	fd_final = open("final.db", O_CREAT | O_WRONLY | O_TRUNC, 0666);	
	if (fd_final <= 0)
		return 102;


	get_time_string(time);	

	do {

		//get address from name_list
		i = 0;		
		do {
			if ((eof_nl = read(fd_nl, &c, 1)) < 0) {
				fprintf(stderr, "Read error in name_list read(1)\n");
				return 103;
			}
			
			else if(eof_nl == 0)
				break;

			address[i] = c;
			i++;	
		}while(c != '\t');
		address[i - 1] = '\0';	
		
		if (eof_nl == 0)
			break;				

		//get name from name_list
		i = 0;
		do {
			if ((eof_nl = read(fd_nl, &c, 1)) <= 0) {
				fprintf(stderr, "Read error in name_list read(2) %d\n", eof_nl);
				return 104;
			}
			
			name[i] = c;					
			i++;
		}while (c != '\n');
		name[i - 1] = '\0'; 

		do {
			//get database entry from database file
			i = 0;
			do {
				if ((eof_db = read(fd_db, &c, 1)) < 0) {
					fprintf(stderr, "Read error in databaase read\n");
					return 105;
				}
				else if (eof_db == 0){
					lseek(fd_db, 0, SEEK_SET);				
					break;
				}
				database[i] = c;
				i++;
			}while (c != '\n');
			database[i -1] = '\0';
			
			if (eof_db == 0)
				break;
		
			if (!strcmp(address, database)) {
				printf("%s PRESENT\n", name);
				sprintf(wbuffer, "%s\t%s", name, time);
				write(fd_final, wbuffer, strlen(wbuffer));
				lseek(fd_db, 0, SEEK_SET);
				break; 
			}
				

		}while(1);

	}while (1);			
	
	close(fd_db);
	fd_db = open("database.db", O_RDWR | O_TRUNC);
	return 0;
}

/************************************************************************************************************/
